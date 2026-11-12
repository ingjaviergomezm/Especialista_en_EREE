#!/usr/bin/env python3
"""Evaluación financiera de proyectos de energía (skills proyectos-er y gestion-energetica).

Método: flujo de caja anual explícito año a año → VPN, TIR, payback simple y descontado, LCOE descontado,
sensibilidad tipo tornado y prueba de cierre de energía E = P·h·FP.

Fuentes del método:
- Ejercicios del profesor, `09 Evaluación de proyecto_ejercicio limpio.xlsx` (curso 05, nivel N3): estructura del flujo
  (ingresos − O&M − T&D − impuesto; la depreciación solo reduce la base gravable).
- Corrección documentada (brecha B-ER7): en el Excel del curso el impuesto de TODOS los años usa la renta del año 1
  (referencia absoluta $C$27). Aquí el impuesto se calcula año a año; el parámetro `impuesto_fijo_ano1=True` reproduce
  el resultado del curso solo para la prueba de regresión.
- LCOE descontado: SUPUESTO estándar (brecha B-ER1): LCOE = Σ costos_t/(1+i)^t ÷ Σ E_t/(1+i)^t.

Convenciones: el año 0 es la inversión; los flujos son de fin de año. El dinero va en la moneda y el año que declare el
usuario. Los excedentes y el autoconsumo se valoran por separado: la regla CREG vigente cambia el precio de los
excedentes (CREG 174/2021, modificada por las 101 072/2025 y 101 087/2025).

Uso:
    python evaluacion_financiera.py --ejemplo
    python evaluacion_financiera.py --capex 21500000 --om 500000 --energia 7000 --tarifa 600 --anos 20 --tasa 0.12
"""
from __future__ import annotations

import argparse
import json
import math
import numbers
from dataclasses import dataclass, field
from typing import Callable, Sequence

# ----------------------------------------------------------------------------------------------- indicadores básicos


def vpn(flujos: Sequence[float], tasa: float) -> float:
    """Valor presente neto. flujos[0] corresponde al año 0 (sin descontar)."""
    if tasa <= -1:
        raise ValueError("la tasa debe ser > -100 %")
    return sum(f / (1 + tasa) ** t for t, f in enumerate(flujos))


def tir(flujos: Sequence[float], tol: float = 1e-10) -> float | None:
    """Tasa interna de retorno.

    Devuelve None si los flujos no cambian de signo (la TIR no existe). Si hay varias raíces (flujos no convencionales),
    lanza ValueError con todas ellas: en ese caso la TIR no sirve para decidir y se usa el VPN.
    """
    signos = [f for f in flujos if f != 0]
    if not signos or all(f > 0 for f in signos) or all(f < 0 for f in signos):
        return None
    # barrido de tasas buscando cambios de signo del VPN y bisección en cada intervalo
    rejilla = [-0.99 + k * 0.005 for k in range(int((10 + 0.99) / 0.005) + 1)]
    raices: list[float] = []
    previo_r, previo_v = rejilla[0], vpn(flujos, rejilla[0])
    for r in rejilla[1:]:
        v = vpn(flujos, r)
        if previo_v == 0:
            raices.append(previo_r)
        elif previo_v * v < 0:
            a, b, fa = previo_r, r, previo_v
            for _ in range(200):
                m = (a + b) / 2
                fm = vpn(flujos, m)
                if fa * fm <= 0:
                    b = m
                else:
                    a, fa = m, fm
                if b - a < tol:
                    break
            raices.append((a + b) / 2)
        previo_r, previo_v = r, v
    if not raices:
        return None
    if len(raices) > 1:
        raise ValueError(f"flujos no convencionales: varias TIR {[round(x, 6) for x in raices]}; decidir con el VPN")
    return raices[0]


def payback(flujos: Sequence[float], tasa: float | None = None) -> float | None:
    """Años hasta recuperar la inversión (interpolación lineal dentro del año). Con `tasa`, payback descontado.

    Devuelve None si el acumulado termina negativo. Si una reposición posterior vuelve negativo el acumulado, cuenta
    el ÚLTIMO cruce a positivo (recuperación definitiva), no el primero.
    """
    acumulado, cruce = 0.0, None
    for t, f in enumerate(flujos):
        ft = f / (1 + tasa) ** t if tasa is not None else f
        anterior = acumulado
        acumulado += ft
        if t > 0 and anterior < 0 <= acumulado:
            cruce = (t - 1) + (-anterior / ft if ft else 0)
    return cruce if acumulado >= 0 else None


def payback_simple(inversion: float, ahorro_anual: float) -> float:
    """Retorno simple = inversión / ahorro anual (para medidas de eficiencia)."""
    if ahorro_anual <= 0:
        raise ValueError("el ahorro anual debe ser positivo; con ahorro ≤ 0 la medida no se recupera")
    return inversion / ahorro_anual


def lcoe(costos: Sequence[float], energia: Sequence[float], tasa: float) -> float:
    """LCOE descontado = Σ costos_t/(1+i)^t / Σ E_t/(1+i)^t (costos incluye la inversión en t=0)."""
    num = sum(c / (1 + tasa) ** t for t, c in enumerate(costos))
    den = sum(e / (1 + tasa) ** t for t, e in enumerate(energia))
    if den <= 0:
        raise ValueError("la energía descontada debe ser positiva")
    return num / den


def lcoe_no_descontado(costos: Sequence[float], energia: Sequence[float]) -> float:
    """Versión del curso 05 (HID p.49): Σ costos / Σ energía. Solo como referencia; para decidir se usa la descontada."""
    return sum(costos) / sum(energia)


# --------------------------------------------------------------------------------------------- prueba de cierre


def cierre_energia(potencia_kw: float, horas: float, factor_planta: float) -> float:
    """Energía (kWh) = P (kW) × horas × FP. Sirve para validar cualquier cifra de energía reportada."""
    if not 0 <= factor_planta <= 1:
        raise ValueError("el factor de planta debe estar entre 0 y 1")
    return potencia_kw * horas * factor_planta


def factor_planta_implicito(energia_kwh: float, potencia_kw: float, horas: float = 8760) -> float:
    """FP implícito de una energía reportada. Si da > 1, la cifra no cierra."""
    return energia_kwh / (potencia_kw * horas)


def verificar_cierre(energia_kwh: float, potencia_kw: float, fp_min: float, fp_max: float,
                     horas: float = 8760) -> dict:
    """Comprueba que una energía reportada sea coherente con un rango de FP declarado."""
    fp = factor_planta_implicito(energia_kwh, potencia_kw, horas)
    return {"fp_implicito": fp, "cierra": fp_min <= fp <= fp_max and fp <= 1,
            "rango_kwh": (cierre_energia(potencia_kw, horas, fp_min), cierre_energia(potencia_kw, horas, fp_max))}


# ------------------------------------------------------------------------------------------------ flujo de caja


def _serie(valor: float | Sequence[float], n: int, crecimiento: float = 0.0) -> list[float]:
    """Convierte un escalar en serie de n años (año 1..n) con crecimiento compuesto; una lista se usa tal cual."""
    if isinstance(valor, numbers.Real):
        return [valor * (1 + crecimiento) ** (t - 1) for t in range(1, n + 1)]
    serie = list(valor)
    if len(serie) != n:
        raise ValueError(f"la serie tiene {len(serie)} años y el horizonte es {n}")
    return serie


@dataclass
class Proyecto:
    """Entradas del flujo de caja. Todo valor monetario en la misma moneda y año base declarados."""
    capex: float                                  # inversión en el año 0 (positiva)
    anos: int                                     # horizonte de evaluación
    tasa: float                                   # tasa de descuento (fracción)
    energia_autoconsumo_kwh: float | Sequence[float] = 0.0   # energía que reemplaza compra (año 1 o serie)
    tarifa: float | Sequence[float] = 0.0         # $/kWh evitado (escalar o serie)
    energia_excedente_kwh: float | Sequence[float] = 0.0     # Exc2: exportación que SUPERA la importación del periodo
    precio_excedente: float | Sequence[float] = 0.0          # $/kWh de Exc2 según regla CREG vigente (Mc o bolsa)
    energia_exc1_kwh: float | Sequence[float] = 0.0          # Exc1: exportación hasta la importación (permuta/crédito)
    precio_exc1: float | Sequence[float] = 0.0               # $/kWh de Exc1 según regla vigente (tarifa − comercialización)
    degradacion: float = 0.0                      # pérdida anual compuesta de producción (fracción)
    escalamiento_tarifa: float = 0.0              # crecimiento anual de la tarifa y de precio_exc1 (si son escalares)
    escalamiento_excedente: float = 0.0           # crecimiento anual de precio_excedente (Exc2): NO sigue al CU
    om_anual: float = 0.0                         # O&M año 1 (positivo)
    om_pct_capex: float = 0.0                     # alternativa: O&M como fracción del CAPEX
    otros_costos_kwh: float = 0.0                 # $/kWh de costos variables (p. ej. T&D)
    otros_ingresos_kwh: float = 0.0               # $/kWh de ingresos adicionales (p. ej. garantías)
    inflacion_costos: float = 0.0                 # crecimiento anual de O&M, T&D y garantías
    reposiciones: dict[int, float] = field(default_factory=dict)  # {año: costo} p. ej. inversor (gasto deducible)
    beneficios_tributarios: dict[int, float] = field(default_factory=dict)  # {año: ahorro de impuesto} Ley 1715,
    #   calculado aparte con el contador (deducción ≤ 50 % de la renta líquida, depreciación acelerada); escenario aparte
    tasa_impuesto: float = 0.0                    # impuesto de renta (fracción); 0 = no aplica
    anos_depreciacion: int | None = None          # depreciación lineal (por defecto = anos)
    impuesto_fijo_ano1: bool = False              # SOLO para reproducir el error del Excel del curso (B-ER7)


def flujo_caja(p: Proyecto) -> dict:
    """Construye el flujo de caja año a año y devuelve las filas y los indicadores."""
    n = p.anos
    auto = _degradar(_serie(p.energia_autoconsumo_kwh, n), p.degradacion, isinstance(p.energia_autoconsumo_kwh, (int, float)))
    exc = _degradar(_serie(p.energia_excedente_kwh, n), p.degradacion, isinstance(p.energia_excedente_kwh, (int, float)))
    tarifa = _serie(p.tarifa, n, p.escalamiento_tarifa)
    pexc = _serie(p.precio_excedente, n, p.escalamiento_excedente)
    exc1 = _degradar(_serie(p.energia_exc1_kwh, n), p.degradacion, isinstance(p.energia_exc1_kwh, (int, float)))
    pexc1 = _serie(p.precio_exc1, n, p.escalamiento_tarifa)
    energia_total = [a + e + e1 for a, e, e1 in zip(auto, exc, exc1)]

    om_base = p.om_anual + p.om_pct_capex * p.capex
    om = [om_base * (1 + p.inflacion_costos) ** (t - 1) for t in range(1, n + 1)]
    # en el Excel del curso, T&D y garantías se calculan con la energía del año 1 y crecen con la inflación
    otros_c = [p.otros_costos_kwh * energia_total[0] * (1 + p.inflacion_costos) ** (t - 1) for t in range(1, n + 1)]
    otros_i = [p.otros_ingresos_kwh * energia_total[0] * (1 + p.inflacion_costos) ** (t - 1) for t in range(1, n + 1)]
    ingreso_auto = [a * t for a, t in zip(auto, tarifa)]
    ingreso_exc = [e * pe + e1 * pe1 for e, pe, e1, pe1 in zip(exc, pexc, exc1, pexc1)]
    repos = [p.reposiciones.get(t, 0.0) for t in range(1, n + 1)]
    benef = [p.beneficios_tributarios.get(t, 0.0) for t in range(1, n + 1)]
    nd = p.anos_depreciacion or n
    depre = [p.capex / nd if t <= nd else 0.0 for t in range(1, n + 1)]

    # la reposición se trata como gasto deducible del año (SUPUESTO simplificado; el contador puede capitalizarla)
    renta = [ia + ie + oi - o - oc - d - rp for ia, ie, oi, o, oc, d, rp in
             zip(ingreso_auto, ingreso_exc, otros_i, om, otros_c, depre, repos)]
    if p.impuesto_fijo_ano1:
        impuesto = [max(renta[0], 0) * p.tasa_impuesto] * n
    else:
        impuesto = [max(r, 0) * p.tasa_impuesto for r in renta]  # sin escudo por pérdidas: SUPUESTO conservador
    neto = [ia + ie + oi - o - oc - rp - im + b for ia, ie, oi, o, oc, rp, im, b in
            zip(ingreso_auto, ingreso_exc, otros_i, om, otros_c, repos, impuesto, benef)]
    flujos = [-p.capex] + neto
    costos_lcoe = [p.capex] + [o + oc + rp for o, oc, rp in zip(om, otros_c, repos)]

    acumulado, filas = 0.0, []
    for t in range(n + 1):
        acumulado += flujos[t]
        filas.append({"ano": t, "energia_kwh": 0.0 if t == 0 else energia_total[t - 1],
                      "ingreso_autoconsumo": 0.0 if t == 0 else ingreso_auto[t - 1],
                      "ingreso_excedentes": 0.0 if t == 0 else ingreso_exc[t - 1],
                      "otros_ingresos": 0.0 if t == 0 else otros_i[t - 1],
                      "om": 0.0 if t == 0 else om[t - 1], "otros_costos": 0.0 if t == 0 else otros_c[t - 1],
                      "reposicion": 0.0 if t == 0 else repos[t - 1], "impuesto": 0.0 if t == 0 else impuesto[t - 1],
                      "flujo": flujos[t], "acumulado": acumulado})
    try:
        tasa_interna = tir(flujos)
        nota_tir = None
        hay_signo = any(f > 0 for f in flujos) and any(f < 0 for f in flujos)
        if tasa_interna is None and hay_signo:
            nota_tir = "TIR fuera del rango buscado (−99 % a 1 000 %); revisar el CAPEX y decidir con el VPN"
    except ValueError as e:
        tasa_interna, nota_tir = None, str(e)
    return {"filas": filas, "flujos": flujos, "vpn": vpn(flujos, p.tasa), "tir": tasa_interna, "nota_tir": nota_tir,
            "payback": payback(flujos), "payback_descontado": payback(flujos, p.tasa),
            "lcoe": lcoe(costos_lcoe, [0.0] + energia_total, p.tasa) if sum(energia_total) > 0 else None}


def _degradar(serie: list[float], degradacion: float, aplicar: bool) -> list[float]:
    return [v * (1 - degradacion) ** t for t, v in enumerate(serie)] if aplicar else serie


# ------------------------------------------------------------------------------------------------- sensibilidad


def tornado(p: Proyecto, variaciones: dict[str, tuple[float, float]],
            metrica: Callable[[dict], float] = lambda r: r["vpn"]) -> list[dict]:
    """Sensibilidad uno a uno: para cada atributo de Proyecto aplica un factor bajo y alto (p. ej. 0.8, 1.2).

    Devuelve la lista ordenada por amplitud (la variable que más mueve el resultado primero).
    """
    base = metrica(flujo_caja(p))
    salida = []
    for attr, (f_bajo, f_alto) in variaciones.items():
        valores = []
        for f in (f_bajo, f_alto):
            original = getattr(p, attr)
            nuevo = [v * f for v in original] if isinstance(original, (list, tuple)) else original * f
            q = Proyecto(**{**p.__dict__, attr: nuevo})
            valores.append(metrica(flujo_caja(q)))
        salida.append({"variable": attr, "factor_bajo": f_bajo, "factor_alto": f_alto, "resultado_bajo": valores[0],
                       "resultado_alto": valores[1], "base": base, "amplitud": abs(valores[1] - valores[0])})
    return sorted(salida, key=lambda d: -d["amplitud"])


def punto_equilibrio(p: Proyecto, attr: str, lo: float, hi: float, metrica=lambda r: r["vpn"]) -> float | None:
    """Valor de `attr` (escalar) que hace la métrica = 0 (p. ej. tarifa mínima para VPN = 0). None si no cruza."""
    def g(x):
        return metrica(flujo_caja(Proyecto(**{**p.__dict__, attr: x})))
    a, b = lo, hi
    ga, gb = g(a), g(b)
    if ga * gb > 0:
        return None
    for _ in range(200):
        m = (a + b) / 2
        gm = g(m)
        if ga * gm <= 0:
            b, gb = m, gm
        else:
            a, ga = m, gm
    return (a + b) / 2


def capex_max_para_payback(p: Proyecto, anos_objetivo: float, descontado: bool = False) -> float | None:
    """CAPEX máximo con el que el proyecto se paga en `anos_objetivo` años (payback simple o descontado).

    Sirve para responder "¿cuánto puede costar?" sin inventar un precio: se compara contra cotizaciones reales.
    None si ni con CAPEX ≈ 0 se paga en ese plazo."""
    if anos_objetivo <= 0:
        raise ValueError("anos_objetivo debe ser > 0")
    clave = "payback_descontado" if descontado else "payback"

    def metrica(r):
        pb = r[clave]
        return anos_objetivo - (pb if pb is not None else p.anos + 1)

    hi = max(p.capex, 1.0)
    for _ in range(60):
        if metrica(flujo_caja(Proyecto(**{**p.__dict__, "capex": hi}))) < 0:
            break
        hi *= 2
    else:
        return None
    return punto_equilibrio(p, "capex", 1e-6, hi, metrica)


# ---------------------------------------------------------------------------------------------------------- CLI


def _imprimir(res: dict) -> None:
    print(f"{'año':>4} {'energía kWh':>14} {'flujo':>18} {'acumulado':>18}")
    for f in res["filas"]:
        print(f"{f['ano']:>4} {f['energia_kwh']:>14,.0f} {f['flujo']:>18,.0f} {f['acumulado']:>18,.0f}")
    tir_txt = f"{res['tir']:.2%}" if res["tir"] is not None else f"no existe ({res['nota_tir'] or 'sin cambio de signo'})"
    pb = f"{res['payback']:.1f} años" if res["payback"] is not None else "no se recupera en el horizonte"
    print(f"\nVPN = {res['vpn']:,.0f} | TIR = {tir_txt} | payback = {pb}"
          + (f" | LCOE = {res['lcoe']:,.2f} por kWh" if res["lcoe"] else ""))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ejemplo", action="store_true", help="corre el ejemplo FV 5 kW del curso 05 (VPN 4 860 021)")
    ap.add_argument("--capex", type=float)
    ap.add_argument("--anos", type=int, help="horizonte (años); OBLIGATORIO salvo --ejemplo")
    ap.add_argument("--tasa", type=float, help="tasa de descuento (fracción) aprobada por el cliente; OBLIGATORIA")
    ap.add_argument("--energia", type=float, default=0, help="kWh/año autoconsumidos (año 1)")
    ap.add_argument("--tarifa", type=float, default=0, help="$/kWh evitado")
    ap.add_argument("--excedentes", type=float, default=0, help="Exc2: kWh/año exportados por encima de la importación")
    ap.add_argument("--precio-excedentes", type=float, default=0, help="$/kWh de Exc2 según regla CREG vigente")
    ap.add_argument("--escalamiento-excedentes", type=float, default=0.0, help="crecimiento anual del precio de Exc2")
    ap.add_argument("--exc1", type=float, default=0, help="Exc1: kWh/año exportados hasta la importación")
    ap.add_argument("--precio-exc1", type=float, default=0, help="$/kWh de Exc1 según regla CREG vigente")
    ap.add_argument("--degradacion", type=float, default=0.0)
    ap.add_argument("--escalamiento", type=float, default=0.0)
    ap.add_argument("--om", type=float, default=0.0)
    ap.add_argument("--inflacion", type=float, default=0.0)
    ap.add_argument("--impuesto", type=float, default=0.0)
    ap.add_argument("--reposicion", action="append", default=[], help="AÑO:COSTO (repetible)")
    ap.add_argument("--tornado", action="store_true", help="sensibilidad ±20 %% en tarifa, energía, CAPEX y O&M")
    ap.add_argument("--payback-objetivo", type=float,
                    help="años: imprime el CAPEX máximo con el que el proyecto se paga en ese plazo")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.ejemplo:
        p = Proyecto(capex=21_500_000, anos=20, tasa=0.12, energia_autoconsumo_kwh=7000, tarifa=600,
                     om_anual=500_000, reposiciones={10: 3_000_000, 20: 3_000_000})
        print("Ejemplo del curso 05 (FV 5 kW, nivel N3). Supuestos del ejercicio, no datos vigentes.\n")
    else:
        if a.capex is None:
            ap.error("falta --capex (o use --ejemplo)")
        if a.tasa is None or a.anos is None:
            ap.error("--tasa y --anos son obligatorios: deben salir del Registro de Supuestos aprobado")
        repos = {int(k): float(v) for k, v in (r.split(":") for r in a.reposicion)}
        p = Proyecto(capex=a.capex, anos=a.anos, tasa=a.tasa, energia_autoconsumo_kwh=a.energia, tarifa=a.tarifa,
                     energia_excedente_kwh=a.excedentes, precio_excedente=a.precio_excedentes,
                     escalamiento_excedente=a.escalamiento_excedentes, energia_exc1_kwh=a.exc1,
                     precio_exc1=a.precio_exc1,
                     degradacion=a.degradacion, escalamiento_tarifa=a.escalamiento, om_anual=a.om,
                     inflacion_costos=a.inflacion, tasa_impuesto=a.impuesto, reposiciones=repos)
    if not a.json:
        print(f"Supuestos usados: tasa {p.tasa:.2%} · horizonte {p.anos} años · degradación {p.degradacion:.2%}/año · "
              f"escalamiento tarifa {p.escalamiento_tarifa:.2%} · O&M {p.om_anual:,.0f} · impuesto {p.tasa_impuesto:.0%} · "
              f"Exc1 {p.energia_exc1_kwh:,.0f} kWh a {p.precio_exc1:,.2f} · Exc2 {p.energia_excedente_kwh:,.0f} kWh a "
              f"{p.precio_excedente:,.2f} · sin incentivos Ley 1715 (escenario aparte)\n")
    res = flujo_caja(p)
    if a.json:
        print(json.dumps({k: v for k, v in res.items() if k != "filas"} | {"filas": res["filas"]}, ensure_ascii=False))
    else:
        _imprimir(res)
    if a.tornado:
        variaciones = {"tarifa": (0.8, 1.2), "energia_autoconsumo_kwh": (0.8, 1.2), "capex": (0.8, 1.2),
                       "om_anual": (0.8, 1.2)}
        print("\nSensibilidad del VPN (±20 %):")
        for d in tornado(p, variaciones):
            print(f"  {d['variable']:<26} {d['resultado_bajo']:>16,.0f} … {d['resultado_alto']:>16,.0f}")
    if a.payback_objetivo:
        cm = capex_max_para_payback(p, a.payback_objetivo)
        txt = f"{cm:,.0f}" if cm is not None else "no se alcanza ni con CAPEX ≈ 0"
        print(f"\nCAPEX máximo para pagarse en {a.payback_objetivo:g} años: {txt} "
              "(comparar contra cotizaciones reales; no es un precio de mercado)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
