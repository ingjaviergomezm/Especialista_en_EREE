#!/usr/bin/env python3
"""Balance energético de una instalación con prueba de cierre, USE por Pareto y datos para Sankey (skill gestion-energetica).

Por qué existe: el peor resultado del curso (curso 03 Act 2) fue un balance donde los porcentajes por área, por energético
y por equipo no cerraban, el Sankey no sumaba y se confundió energía con costo. Este script hace imposible ese error:
- convierte todo energético a kWh con un factor DECLARADO (el PCI y la densidad del gas vienen del comercializador o del
  cliente, nunca de un ejercicio académico; brecha B-GE7);
- estima el consumo de cada equipo como kW × horas × días × factor de carga (la potencia de placa no es el consumo);
- compara la suma por equipos contra la factura y declara si CIERRA dentro de una tolerancia;
- reporta el % de energía y el % de costo POR SEPARADO;
- marca los USE como los equipos que acumulan el umbral de Pareto (80 % por defecto, SUPUESTO declarado) y permite
  agregar USE por potencial de mejora (ISO 50001 6.3);
- genera los flujos del Sankey (energético → área → equipo) desde la misma tabla, de modo que el Sankey suma por
  construcción.

Entrada CSV de equipos: `equipo,area,energetico,kw,horas_dia,dias_ano,factor_carga`.

Uso:
    python balance_energetico.py --ejemplo
    python balance_energetico.py --equipos equipos.csv --factura electricidad=120000 --factura gas=80000
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Equipo:
    nombre: str
    area: str
    energetico: str
    kw: float
    horas_dia: float
    dias_ano: float
    factor_carga: float = 1.0

    @property
    def kwh_ano(self) -> float:
        if not 0 < self.factor_carga <= 1:
            raise ValueError(f"{self.nombre}: factor de carga {self.factor_carga} fuera de (0, 1]")
        if not 0 <= self.horas_dia <= 24:
            raise ValueError(f"{self.nombre}: {self.horas_dia} h/día no es posible")
        if self.kw < 0 or not 0 <= self.dias_ano <= 366:
            raise ValueError(f"{self.nombre}: kW negativo o días fuera de 0–366")
        return self.kw * self.horas_dia * self.dias_ano * self.factor_carga


# ------------------------------------------------------------------------------------------------- conversiones


def gas_a_kwh(m3: float, pci_mj_m3: float | None = None, pci_mj_kg: float | None = None,
              densidad_kg_m3: float | None = None) -> float:
    """kWh = m³ × PCI (MJ/m³) / 3,6, o m³ × ρ × PCI (MJ/kg) / 3,6. La densidad del gas natural es ≈ 0,7–0,8 kg/m³; si
    alguien entrega ~16 kg/m³ hay un error de unidades (caso del ejercicio C1 del curso)."""
    if pci_mj_m3 is not None:
        return m3 * pci_mj_m3 / 3.6
    if pci_mj_kg is None or densidad_kg_m3 is None:
        raise ValueError("indique pci_mj_m3, o bien pci_mj_kg y densidad_kg_m3")
    if not 0.5 <= densidad_kg_m3 <= 1.2:
        raise ValueError(f"densidad del gas {densidad_kg_m3} kg/m³ implausible para gas natural (≈ 0,7–0,8): verificar unidades")
    return m3 * densidad_kg_m3 * pci_mj_kg / 3.6


def combustible_a_kwh(cantidad: float, pci_mj_por_unidad: float) -> float:
    """Para GLP, diésel, carbón y biomasa: cantidad (kg, gal, L) × PCI declarado (MJ por esa unidad) / 3,6."""
    return cantidad * pci_mj_por_unidad / 3.6


# ------------------------------------------------------------------------------------------------------ balance


def balance(equipos: list[Equipo], factura_kwh: dict[str, float], tarifas: dict[str, float] | None = None,
            tolerancia: float = 0.10) -> dict:
    """Agrega por energético, por área y por equipo, prueba el cierre contra la factura y separa energía de costo."""
    por_energetico: dict[str, float] = defaultdict(float)
    por_area: dict[str, float] = defaultdict(float)
    por_equipo: dict[str, float] = {}
    for eq in equipos:
        k = eq.kwh_ano
        if eq.nombre in por_equipo:
            raise ValueError(f"equipo repetido: {eq.nombre}")
        por_equipo[eq.nombre] = k
        por_energetico[eq.energetico] += k
        por_area[eq.area] += k

    cierre = {}
    for en, fact in factura_kwh.items():
        est = por_energetico.get(en, 0.0)
        dif = (est - fact) / fact if fact else float("inf")
        cierre[en] = {"factura_kwh": fact, "estimado_kwh": est, "diferencia": dif, "cierra": abs(dif) <= tolerancia}
    sin_factura = set(por_energetico) - set(factura_kwh)
    total = sum(por_equipo.values())
    if total <= 0:
        raise ValueError("el inventario suma 0 kWh: no hay balance que calcular")
    resultado = {
        "por_equipo": dict(sorted(por_equipo.items(), key=lambda x: -x[1])),
        "por_area": dict(por_area), "por_energetico": dict(por_energetico), "total_kwh": total,
        "pct_energia_equipo": {k: v / total for k, v in por_equipo.items()},
        "cierre": cierre, "energeticos_sin_factura": sorted(sin_factura),
        "cierra": all(c["cierra"] for c in cierre.values()) and not sin_factura, "tolerancia": tolerancia,
    }
    if tarifas:
        costo_equipo = {}
        for eq in equipos:
            if eq.energetico not in tarifas:
                raise ValueError(f"falta la tarifa de {eq.energetico}")
            costo_equipo[eq.nombre] = por_equipo[eq.nombre] * tarifas[eq.energetico]
        ct = sum(costo_equipo.values())
        resultado["costo_equipo"] = costo_equipo
        resultado["pct_costo_equipo"] = {k: v / ct for k, v in costo_equipo.items()}
        resultado["costo_total"] = ct
    _verificar_sumas(resultado)
    return resultado


def _verificar_sumas(r: dict) -> None:
    """Prueba de cierre interna: las tres desagregaciones suman lo mismo y los % suman 100 %."""
    t = r["total_kwh"]
    for clave in ("por_area", "por_energetico"):
        if abs(sum(r[clave].values()) - t) > 1e-6 * max(t, 1):
            raise AssertionError(f"{clave} no suma el total")
    if abs(sum(r["pct_energia_equipo"].values()) - 1) > 1e-9:
        raise AssertionError("los % de energía no suman 100 %")


def usos_significativos(por_equipo: dict[str, float], umbral: float = 0.80, adicionales: list[str] | None = None) -> list[dict]:
    """USE = los equipos que, ordenados de mayor a menor, acumulan hasta cruzar el umbral (incluye el que lo cruza),
    más los `adicionales` declarados por potencial de mejora. El criterio se declara en el informe."""
    total = sum(por_equipo.values())
    acumulado, salida = 0.0, []
    for nombre, kwh in sorted(por_equipo.items(), key=lambda x: -x[1]):
        previo = acumulado
        acumulado += kwh / total
        es_use = previo < umbral or nombre in (adicionales or [])
        salida.append({"equipo": nombre, "kwh": kwh, "pct": kwh / total, "acumulado": acumulado, "use": es_use,
                       "criterio": ("Pareto" if previo < umbral else "potencial de mejora") if es_use else ""})
    return salida


def flujos_sankey(equipos: list[Equipo]) -> list[tuple[str, str, float]]:
    """Flujos (origen, destino, kWh) energético → área → equipo, construidos desde la misma tabla del balance."""
    ea: dict[tuple[str, str], float] = defaultdict(float)
    flujos = []
    for eq in equipos:
        ea[(eq.energetico, eq.area)] += eq.kwh_ano
        flujos.append((eq.area, eq.nombre, eq.kwh_ano))
    return [(a, b, v) for (a, b), v in ea.items()] + flujos


def leer_equipos(ruta: str) -> list[Equipo]:
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        return [Equipo(r["equipo"], r["area"], r["energetico"], float(r["kw"]), float(r["horas_dia"]),
                       float(r["dias_ano"]), float(r.get("factor_carga") or 1)) for r in csv.DictReader(f)]


EJEMPLO = [
    Equipo("freidora", "cocina", "gas", 18, 8, 360, 0.6),
    Equipo("estufa", "cocina", "gas", 12, 6, 360, 0.5),
    Equipo("nevera", "cocina", "electricidad", 0.8, 24, 365, 0.45),
    Equipo("aire_acondicionado", "salon", "electricidad", 3.5, 10, 360, 0.7),
    Equipo("iluminacion", "salon", "electricidad", 1.2, 12, 360, 1.0),
]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ejemplo", action="store_true", help="restaurante ficticio (datos ilustrativos, no reales)")
    ap.add_argument("--equipos")
    ap.add_argument("--factura", action="append", default=[], help="ENERGETICO=kWh facturados en el MISMO periodo que los días de uso de los equipos (repetible)")
    ap.add_argument("--tarifa", action="append", default=[], help="ENERGETICO=$/kWh (repetible)")
    ap.add_argument("--tolerancia", type=float, default=0.10)
    ap.add_argument("--forzar", action="store_true", help="muestra porcentajes aunque el balance no cierre (uso interno)")
    a = ap.parse_args(argv)
    if a.ejemplo:
        eqs = EJEMPLO
        factura = {"gas": 45_000, "electricidad": 16_500}
        tarifas = {"gas": 350, "electricidad": 900}
    elif a.equipos:
        eqs = leer_equipos(a.equipos)
        factura = {k: float(v) for k, v in (x.split("=") for x in a.factura)}
        tarifas = {k: float(v) for k, v in (x.split("=") for x in a.tarifa)} or None
    else:
        ap.error("use --ejemplo o --equipos")
    r = balance(eqs, factura, tarifas, a.tolerancia)
    print("Cierre contra la factura:")
    for en, c in r["cierre"].items():
        print(f"  {en:<14} factura {c['factura_kwh']:>10,.0f} | estimado {c['estimado_kwh']:>10,.0f} | "
              f"{c['diferencia']:+.1%} → {'CIERRA' if c['cierra'] else 'NO CIERRA: revisar horas, factor de carga o equipos faltantes'}")
    if not r["cierra"] and not a.forzar:
        print("\n⚠ El balance no cierra: no se muestran porcentajes ni USE. Conciliar con la factura "
              "(equipos faltantes, horas, factor de carga) y volver a correr. --forzar solo para diagnóstico interno.")
        return 2
    print(f"\n{'equipo':<22} {'kWh periodo':>12} {'% energía':>10}" + (f" {'% costo':>9}" if tarifas else ""))
    for k, v in r["por_equipo"].items():
        print(f"{k:<22} {v:>12,.0f} {r['pct_energia_equipo'][k]:>10.1%}" + (f" {r['pct_costo_equipo'][k]:>9.1%}" if tarifas else ""))
    print("\nUSE (Pareto 80 %, SUPUESTO declarado):", [u["equipo"] for u in usos_significativos(r["por_equipo"]) if u["use"]])
    if not r["cierra"]:
        print("\n⚠ --forzar: el balance NO cierra; estos porcentajes no se presentan al cliente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
