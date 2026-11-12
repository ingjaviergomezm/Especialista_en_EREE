#!/usr/bin/env python3
"""Medidas de ahorro con costo-beneficio (skill gestion-energetica).

Cada medida devuelve: ahorro en kWh/año y en $/año, inversión, payback, VPN y TIR (estos tres con
evaluacion_financiera.py). Sin ROI la gerencia no puede priorizar (lección L4 del curso 03).

Fuentes del método (curso 03, guía U3, N2, salvo indicación):
- Iluminación: ahorro = n·(W_actual − W_nuevo)·h, más sensores como fracción del consumo nuevo. El ejemplo del curso es
  13 500 kWh/año y 15 600 con sensores. No se baja del nivel de lux que exige el RETILAP vigente.
- Factor de potencia: FP = kW/kVA; compensación Qc = P·(tan φ1 − tan φ2). Cobro de reactiva: CREG 015/2018 cap. 12
  (con modificaciones), con FP inductivo mínimo de 0,9. El límite de 50 % kVArh/kWh y el factor M se verifican en vivo
  `[verificar vigencia]`.
- Motores: ahorro = P_eje·h·carga·(1/η_actual − 1/η_nueva). Es la forma estándar, SUPUESTO declarado.
- Aire comprimido: solo el 10–15 % de la energía llega como trabajo útil; reducir la presión ahorra ≈ 7 % (cifra del
  material, que la literatura asocia a ~1 bar; SUPUESTO con sensibilidad). Fugas: kW × fracción de fugas × horas.
- Cogeneración: eficiencia global de ≈ 56 % en generación separada frente a 75–87 % en CHP (referencia del material).

Uso:
    python medidas_ahorro.py --ejemplo
"""
from __future__ import annotations

import argparse
import math
import warnings
import os
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # módulo hermano, también con `python -P`
from evaluacion_financiera import Proyecto, flujo_caja, payback_simple


@dataclass
class Medida:
    nombre: str
    ahorro_kwh: float
    tarifa: float
    inversion: float
    vida_util: int
    om_adicional: float = 0.0
    tasa: float = 0.12
    uso_significativo: str = ""

    def evaluar(self) -> dict:
        ahorro_pesos = self.ahorro_kwh * self.tarifa - self.om_adicional
        r = flujo_caja(Proyecto(capex=self.inversion, anos=self.vida_util, tasa=self.tasa,
                                energia_autoconsumo_kwh=self.ahorro_kwh, tarifa=self.tarifa, om_anual=self.om_adicional))
        return {"medida": self.nombre, "use": self.uso_significativo, "ahorro_kwh": self.ahorro_kwh,
                "ahorro_pesos": ahorro_pesos, "inversion": self.inversion,
                "payback": payback_simple(self.inversion, ahorro_pesos) if self.inversion > 0 else 0.0,
                "vpn": r["vpn"], "tir": r["tir"], "vida_util": self.vida_util}


def priorizar(medidas: list[Medida]) -> list[dict]:
    """Ordena por VPN (valor creado). El payback se reporta, pero no decide solo: ignora lo que pasa después del retorno.

    Una medida que no se puede evaluar (p. ej. ahorro neto ≤ 0) no tumba la lista: queda al final con su motivo."""
    evaluadas, descartadas = [], []
    for md in medidas:
        try:
            evaluadas.append(md.evaluar())
        except ValueError as err:
            descartadas.append({"nombre": getattr(md, "nombre", "?"), "vpn": float("-inf"), "descartada": str(err)})
    return sorted(evaluadas, key=lambda d: -d["vpn"]) + descartadas


# --------------------------------------------------------------------------------------------- iluminación


def ahorro_iluminacion(n: int, w_actual: float, w_nuevo: float, horas_ano: float, sensores_frac: float = 0.0) -> float:
    """kWh/año ahorrados por cambiar luminarias y, opcionalmente, agregar sensores sobre el consumo nuevo."""
    if w_nuevo > w_actual:
        raise ValueError("la luminaria nueva consume más que la actual")
    base = n * (w_actual - w_nuevo) * horas_ano / 1000
    return base + n * w_nuevo * horas_ano / 1000 * sensores_frac


# ------------------------------------------------------------------------------------------ factor de potencia


def factor_potencia(kw: float, kva: float | None = None, kvar: float | None = None) -> float:
    if kva is None:
        if kvar is None:
            raise ValueError("indique kVA o kVAr")
        kva = math.hypot(kw, kvar)
    if kva < kw:
        raise ValueError("kVA no puede ser menor que kW")
    return kw / kva


def compensacion_kvar(kw: float, fp_actual: float, fp_objetivo: float) -> float:
    """kVAr de condensadores para llevar el FP de fp_actual a fp_objetivo: Qc = P·(tan φ1 − tan φ2)."""
    if not 0 < fp_actual <= 1 or not 0 < fp_objetivo <= 1:
        raise ValueError("FP fuera de (0, 1]")
    if fp_objetivo < fp_actual:
        raise ValueError("el FP objetivo es menor que el actual")
    if fp_objetivo > 0.98:
        warnings.warn("FP objetivo > 0,98 con banco fijo: riesgo de reactiva CAPACITIVA en baja carga (también se cobra); "
                      "usar banco automático por pasos o un objetivo de 0,95–0,97")
    return kw * (math.tan(math.acos(fp_actual)) - math.tan(math.acos(fp_objetivo)))


def reactiva_en_exceso(kwh: float, kvarh: float, limite_frac: float = 0.5) -> float:
    """kVArh inductivos que superan el límite (por defecto el 50 % de la energía activa, equivalente a FP ≈ 0,894).
    `[verificar vigencia del límite y del factor M en la CREG 015/2018 y sus modificaciones]`"""
    return max(kvarh - limite_frac * kwh, 0.0)


def reactiva_en_exceso_horaria(kwh_h, kvarh_ind_h, kvarh_cap_h=None, limite_frac: float = 0.5) -> dict:
    """Evaluación HORA A HORA (como la hace la regulación): exceso inductivo por encima de limite_frac·kWh en cada
    hora, más toda la reactiva capacitiva registrada. Con totales mensuales el exceso se diluye y se subestima.
    `[verificar vigencia: CREG 015/2018 y modificaciones — límite, factor M y tratamiento de la capacitiva]`"""
    if len(kwh_h) != len(kvarh_ind_h) or (kvarh_cap_h is not None and len(kvarh_cap_h) != len(kwh_h)):
        raise ValueError("las series horarias deben tener la misma longitud")
    exceso = [max(q - limite_frac * p, 0.0) for p, q in zip(kwh_h, kvarh_ind_h)]
    cap = list(kvarh_cap_h) if kvarh_cap_h is not None else [0.0] * len(kwh_h)
    return {"exceso_inductivo_kvarh": sum(exceso), "capacitiva_kvarh": sum(cap),
            "horas_con_exceso": sum(1 for x in exceso if x > 0), "horas_con_capacitiva": sum(1 for c in cap if c > 0),
            "exceso_si_se_usara_total_mensual": reactiva_en_exceso(sum(kwh_h), sum(kvarh_ind_h), limite_frac)}


# ----------------------------------------------------------------------------------------------------- motores


def ahorro_motor(p_eje_kw: float, horas_ano: float, carga: float, eta_actual: float, eta_nueva: float) -> float:
    """kWh/año = P_eje·h·carga·(1/η_actual − 1/η_nueva)."""
    if not 0 < eta_actual < eta_nueva <= 1:
        raise ValueError("se requiere 0 < η_actual < η_nueva ≤ 1")
    return p_eje_kw * horas_ano * carga * (1 / eta_actual - 1 / eta_nueva)


# -------------------------------------------------------------------------------------------- aire comprimido


def ahorro_fugas(kw_compresor: float, fraccion_fugas: float, horas_ano: float, fraccion_reparable: float = 1.0) -> float:
    """kWh/año perdidos en fugas que se recuperan al repararlas. La fracción de fugas se mide (prueba en vacío)."""
    if not 0 <= fraccion_fugas < 1:
        raise ValueError("la fracción de fugas debe estar en [0, 1)")
    return kw_compresor * fraccion_fugas * fraccion_reparable * horas_ano


def ahorro_reduccion_presion(consumo_kwh_ano: float, bares: float, ahorro_por_bar: float = 0.07) -> float:
    """≈ 7 % por cada bar menos (SUPUESTO del material; confirmar con el fabricante del compresor)."""
    return consumo_kwh_ano * min(ahorro_por_bar * bares, 0.5)


# ------------------------------------------------------------------------------------------------ cogeneración


def ahorro_cogeneracion(energia_util_kwh: float, eta_separada: float = 0.56, eta_chp: float = 0.80) -> float:
    """Energía primaria ahorrada (kWh) al producir la misma energía útil con CHP en lugar de generación separada."""
    if not eta_separada < eta_chp <= 1:
        raise ValueError("la eficiencia CHP debe superar la de generación separada")
    return energia_util_kwh / eta_separada - energia_util_kwh / eta_chp


# --------------------------------------------------------------------------------------------------------- CLI


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ejemplo", action="store_true")
    a = ap.parse_args(argv)
    if not a.ejemplo:
        ap.print_help()
        return 0
    il = ahorro_iluminacion(100, 80, 35, 3000)
    print(f"Iluminación (curso 03, U3 p.32): {il:,.0f} kWh/año → {il * 0.15:,.0f} €/año a 0,15 €/kWh; "
          f"con sensores al 20 %: {ahorro_iluminacion(100, 80, 35, 3000, 0.20):,.0f} kWh/año")
    print(f"FP con 100 kW y 125 kVA = {factor_potencia(100, 125):.2f}; para llevarlo a 0,95 se requieren "
          f"{compensacion_kvar(100, 0.8, 0.95):.1f} kVAr")
    medidas = [Medida("LED 100 luminarias", il, 900, 9_000_000, 10, uso_significativo="iluminación"),
               Medida("motor IE3 15 kW", ahorro_motor(15, 6000, 0.75, 0.88, 0.93), 900, 12_000_000, 15,
                      uso_significativo="bombeo")]
    print(f"\n{'medida':<22} {'kWh/año':>10} {'$/año':>12} {'payback':>8} {'VPN':>14}")
    for d in priorizar(medidas):
        print(f"{d['medida']:<22} {d['ahorro_kwh']:>10,.0f} {d['ahorro_pesos']:>12,.0f} {d['payback']:>7.1f}a {d['vpn']:>14,.0f}")
    print("(tarifas e inversiones del ejemplo son ilustrativas, no datos vigentes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
