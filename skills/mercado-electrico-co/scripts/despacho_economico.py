#!/usr/bin/env python3
"""Mercado eléctrico colombiano: despacho por orden de mérito, precio nodal, microrred, contratos vs. bolsa, proyección
de demanda y prueba de cierre (skill mercado-electrico-co).

Fuentes del método (curso 08):
- Diapositivas MEC p.56–69 (N4) y código de operación CREG 025/1995: predespacho ideal por orden de mérito; precio
  único de oferta para las 24 h; disponibilidad hora a hora.
- Datos G3 (N3) para la prueba: Nacional H23 → Betania 1 015 $/kWh; Interior H0 → Urrá 1 020 $/kWh (coinciden con la
  corrección de la docente). El predespacho de una zona usa SOLO las plantas de esa zona, y la zona es la que declara el
  archivo de datos.
- Dos nodos: MEC p.64–68 (π = 24,33 sin congestión; 19/35 con congestión; renta de 6 400).
- Microrred: ejercicio JuMP de la docente (N3), resuelto aquí con scipy linprog. Objetivo: 307 188,54. Ese modelo trata
  la batería como un generador SIN estado de carga (defecto de método, brecha B-MC4). `microrred_soc` es el modelo que la
  skill recomienda.
- Contratos y bolsa: MEC p.6–37 (taller de subastas: 95 / 107 / 87 M y 15,7 / 12,3 / 13,7 M).
- Proyección compuesta: curso 04 (una sola tasa por escenario, con fuente citada).

Ningún precio de este archivo es un dato vigente. Los precios reales se consultan en XM (Sinergox/SIMEM) con fecha.

Uso:
    python despacho_economico.py --ejemplo
    python despacho_economico.py --ofertas ofertas.csv --demanda demanda.csv --hora 19 --zona Nacional
"""
from __future__ import annotations

import argparse
import csv
import math
import os
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Sequence

AQUI = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------------------------------------ orden de mérito


@dataclass
class Oferta:
    planta: str
    zona: str
    precio: float                      # $/kWh, precio único para las 24 h
    tipo: str
    disponibilidad: list[float]        # kWh por hora (24 valores)


def leer_ofertas(ruta: str) -> list[Oferta]:
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        return [Oferta(r["planta"], r["zona"], float(r["precio"]), r.get("tipo", ""),
                       [float(r[f"h{h}"] or 0) for h in range(24)]) for r in csv.DictReader(f)]


def leer_demanda(ruta: str) -> dict[str, list[float]]:
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        return {r["zona"]: [float(r[f"h{h}"]) for h in range(24)] for r in csv.DictReader(f)}


@dataclass
class ResultadoMerito:
    hora: int
    zona: str
    demanda: float
    planta_marginal: str | None
    precio: float | None
    empatadas: list[str] = field(default_factory=list)
    despachadas: list[tuple[str, float]] = field(default_factory=list)
    por_tipo: dict[str, float] = field(default_factory=dict)
    deficit: float = 0.0
    alerta: str = ""


def merito(ofertas: Sequence[Oferta], demanda: float, hora: int, zona: str = "Nacional",
           precio_escasez: float | None = None) -> ResultadoMerito:
    """Predespacho ideal SIMPLIFICADO de una hora (ejercicio didáctico del curso 08): ordena por precio de oferta y
    acumula disponibilidad hasta cubrir la demanda.

    Diferencias con el precio de bolsa real (se declaran en todo informe): en Colombia el precio de bolsa es UNO
    nacional, sale del despacho ideal de XM con solo las plantas flexibles marcando precio, e incluye un adicional
    (ΔI) sobre el precio marginal. Las "zonas" del ejercicio NO tienen precio propio: la congestión entre áreas se
    paga como restricciones (componente R del CU). Para un precio real se consulta XM.

    zona = "Nacional" usa todas las plantas; cualquier otra zona usa solo las plantas declaradas en esa zona.
    Si hay empate de precio en la planta marginal, se reportan todas las empatadas. Con `precio_escasez`, se alerta
    cuando el marginal lo supera (se activan las OEF del cargo por confiabilidad).
    """
    if not 0 <= hora <= 23:
        raise ValueError("hora fuera de 0–23")
    if demanda < 0:
        raise ValueError("la demanda no puede ser negativa")
    zonas = {o.zona.casefold() for o in ofertas}
    nacional = zona.casefold() == "nacional"
    if not nacional and zona.casefold() not in zonas:
        raise ValueError(f"zona '{zona}' no está en los datos ({sorted(zonas)}) ni es 'Nacional'")
    pool = [o for o in ofertas if (nacional or o.zona.casefold() == zona.casefold()) and o.disponibilidad[hora] > 0]
    pool.sort(key=lambda o: o.precio)            # orden estable: ante empate conserva el orden del archivo
    acumulado, despachadas = 0.0, []
    por_tipo: dict[str, float] = defaultdict(float)
    for o in pool:
        disp = o.disponibilidad[hora]
        toma = min(disp, demanda - acumulado)
        acumulado += toma
        despachadas.append((o.planta, toma))
        por_tipo[o.tipo] += toma
        if acumulado >= demanda - 1e-9:
            empatadas = [x.planta for x in pool if x.precio == o.precio]
            alerta = ""
            if precio_escasez is not None and o.precio > precio_escasez:
                alerta = (f"precio marginal {o.precio:g} > precio de escasez {precio_escasez:g}: se activan las OEF; "
                          "el precio para la demanda cubierta queda acotado")
            return ResultadoMerito(hora, zona, demanda, o.planta, o.precio, empatadas if len(empatadas) > 1 else [],
                                   despachadas, dict(por_tipo), alerta=alerta)
    return ResultadoMerito(hora, zona, demanda, None, None, [], despachadas, dict(por_tipo), deficit=demanda - acumulado)


def predespacho(ofertas: Sequence[Oferta], demanda_por_zona: dict[str, list[float]]) -> list[ResultadoMerito]:
    return [merito(ofertas, d[h], h, z) for z, d in demanda_por_zona.items() for h in range(24)]


# ------------------------------------------------------------------------------------------------------ dos nodos


def dos_nodos(a_a: float, b_a: float, d_a: float, a_b: float, b_b: float, d_b: float, limite: float) -> dict:
    """Dos nodos con oferta lineal π = a + b·P. Devuelve los precios, generaciones, flujo de A a B y la renta de congestión.
    Modelo didáctico de precio nodal: Colombia NO liquida precios nodales (precio de bolsa único nacional)."""
    if min(b_a, b_b) <= 0 or min(d_a, d_b) < 0 or limite < 0:
        raise ValueError("pendientes > 0, demandas ≥ 0 y límite ≥ 0")
    pi = (d_a + d_b + a_a / b_a + a_b / b_b) / (1 / b_a + 1 / b_b)
    p_a, p_b = (pi - a_a) / b_a, (pi - a_b) / b_b
    flujo = p_a - d_a
    if abs(flujo) <= limite:
        if p_a < 0 or p_b < 0:
            raise ValueError("generación negativa en un nodo: revisar datos")
        return {"congestion": False, "pi_a": pi, "pi_b": pi, "p_a": p_a, "p_b": p_b, "flujo": flujo, "renta": 0.0}
    f = math.copysign(limite, flujo)
    p_a, p_b = d_a + f, d_b - f
    if p_a < 0 or p_b < 0:
        raise ValueError("generación negativa en un nodo: el caso no es factible con oferta lineal sin límites de "
                         "capacidad; revisar datos")
    pi_a, pi_b = a_a + b_a * p_a, a_b + b_b * p_b
    return {"congestion": True, "pi_a": pi_a, "pi_b": pi_b, "p_a": p_a, "p_b": p_b, "flujo": f,
            "renta": abs(pi_b - pi_a) * limite, "uninodal": {"pi": pi, "flujo": flujo}}


# ----------------------------------------------------------------------------------------------------- microrred

SOLAR_CURSO = [0, 0, 0, 0, 0, 0, 0.5, 3, 8, 14, 20, 24, 26, 26, 24, 19, 13, 7, 2, 0, 0, 0, 0, 0]
DEMANDA_CURSO = [20.2195, 19.075, 18.312, 17.549, 17.549, 17.549, 20.601, 22.89, 26.235, 27.468, 27.8495, 29.3755,
                 29.757, 28.6125, 25.942, 25.179, 24.7975, 25.179, 31.283, 38.15, 37.0055, 32.809, 27.8495, 22.89]


def microrred_curso(solar=SOLAR_CURSO, demanda=DEMANDA_CURSO, c1=197, c2=344, c3=769, c4=1000,
                    p2_max=8.56, p3_max=10) -> dict:
    """Reproducción del ejercicio de la docente (batería SIN estado de carga). Solo para validar el solver."""
    from scipy.optimize import linprog
    T = len(demanda)
    # variables: p2[0..T), p3[0..T), x[0..T)
    c = [c2] * T + [c3] * T + [c4] * T
    a_ub, b_ub = [], []
    for t in range(T):            # −(p2 + p3 + x) ≤ −(D − p1)
        fila = [0.0] * (3 * T)
        fila[t] = fila[T + t] = fila[2 * T + t] = -1
        a_ub.append(fila)
        b_ub.append(-(demanda[t] - solar[t]))
    bounds = [(0, p2_max)] * T + [(0, p3_max)] * T + [(0, None)] * T
    r = linprog(c, A_ub=a_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if not r.success:
        raise RuntimeError(r.message)
    fijo = c1 * sum(solar)
    x = list(r.x[2 * T:])
    return {"objetivo": r.fun + fijo, "costo_solar": fijo, "diesel": list(r.x[:T]), "bateria": list(r.x[T:2 * T]),
            "no_atendida": x, "costo_sin_penalidad": r.fun + fijo - c4 * sum(x)}


def microrred_soc(solar: Sequence[float], demanda: Sequence[float], c_diesel: float, p_diesel_max: float,
                  e_bat_kwh: float, p_bat_kw: float, voll: float, soc0: float = 0.5, soc_min: float = 0.1,
                  eta_c: float = 0.95, eta_d: float = 0.95, c_degradacion: float = 0.0, dt: float = 1.0) -> dict:
    """Despacho de microrred con batería y balance de estado de carga (SOC):
    SOC_t = SOC_{t−1} + η_c·carga_t·dt − descarga_t·dt/η_d;  SOC_min·E ≤ SOC_t ≤ E;  SOC_final ≥ SOC_0 (no "regala" energía).
    Balance: solar + diésel + descarga − carga − vertimiento + no_atendida = demanda.
    voll = valor de la energía no suministrada ($/kWh): es un DATO a pedir o un SUPUESTO declarado (brecha B-MC5).
    """
    from scipy.optimize import linprog
    T = len(demanda)
    if len(solar) != T:
        raise ValueError("solar y demanda deben tener la misma longitud")
    # variables por hora: diesel, carga, descarga, soc, vertimiento, no_atendida → 6T
    D, C, S, E, V, X = (k * T for k in range(6))
    n = 6 * T
    cost = [0.0] * n
    for t in range(T):
        cost[D + t] = c_diesel * dt
        cost[S + t] = c_degradacion * dt
        cost[X + t] = voll * dt
    a_eq, b_eq = [], []
    for t in range(T):
        fila = [0.0] * n
        fila[D + t], fila[S + t], fila[C + t], fila[V + t], fila[X + t] = 1, 1, -1, -1, 1
        a_eq.append(fila)
        b_eq.append(demanda[t] - solar[t])
        fila = [0.0] * n                                   # SOC_t − SOC_{t−1} − η_c·c·dt + d·dt/η_d = 0
        fila[E + t] = 1
        fila[C + t] = -eta_c * dt
        fila[S + t] = dt / eta_d
        if t > 0:
            fila[E + t - 1] = -1
            b_eq.append(0.0)
        else:
            b_eq.append(soc0 * e_bat_kwh)
        a_eq.append(fila)
    a_ub = [[0.0] * n]
    a_ub[0][E + T - 1] = -1                                # −SOC_final ≤ −SOC_0
    b_ub = [-soc0 * e_bat_kwh]
    bounds = ([(0, p_diesel_max)] * T + [(0, p_bat_kw)] * T + [(0, p_bat_kw)] * T
              + [(soc_min * e_bat_kwh, e_bat_kwh)] * T + [(0, None)] * T + [(0, None)] * T)
    r = linprog(cost, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if not r.success:
        raise RuntimeError(r.message)
    v = r.x
    return {"costo": r.fun, "diesel": list(v[D:D + T]), "carga": list(v[C:C + T]), "descarga": list(v[S:S + T]),
            "soc": list(v[E:E + T]), "vertimiento": list(v[V:V + T]), "no_atendida": list(v[X:X + T])}


# ------------------------------------------------------------------------------------------- contratos y bolsa


def costo_mezcla(energia_kwh: float, frac_contrato: float, p_contrato: float, p_bolsa: float) -> float:
    """Costo de cubrir `energia_kwh` con una fracción en contrato (precio fijo) y el resto en bolsa."""
    if not 0 <= frac_contrato <= 1:
        raise ValueError("fracción de contrato fuera de [0, 1]")
    return energia_kwh * (frac_contrato * p_contrato + (1 - frac_contrato) * p_bolsa)


def contrato_vs_bolsa(energia_kwh: float, fracciones: Sequence[float], p_contrato: float,
                      escenarios_bolsa: dict[str, float]) -> list[dict]:
    """Matriz de costos por fracción contratada × escenario de bolsa (Niño / normal / Niña)."""
    return [{"frac_contrato": f, **{esc: costo_mezcla(energia_kwh, f, p_contrato, pb) for esc, pb in escenarios_bolsa.items()}}
            for f in fracciones]


def precio_bandas(p_bolsa: float, piso: float, techo: float, prima: float = 0.0) -> float:
    """Contrato de bolsa con bandas: techo si bolsa > techo; piso si bolsa < piso; bolsa + K si está en medio."""
    if piso > techo:
        raise ValueError("piso > techo")
    if p_bolsa > techo:
        return techo
    if p_bolsa < piso:
        return piso
    return p_bolsa + prima


def usuario_no_regulado(consumo_kwh_6m: Sequence[float], demanda_kw_6m: Sequence[float]) -> dict:
    """CREG 131/1998: es no regulado si el promedio de los últimos 6 meses supera 55 MWh/mes o 0,1 MW, en un solo sitio de
    entrega. Umbral confirmado en un concepto CREG de 2025; se verifica en vivo."""
    if len(consumo_kwh_6m) != 6 or len(demanda_kw_6m) != 6:
        raise ValueError("se requieren exactamente 6 meses")
    e = sum(consumo_kwh_6m) / 6
    p = sum(demanda_kw_6m) / 6
    return {"consumo_promedio_kwh": e, "demanda_promedio_kw": p, "cumple": e >= 55_000 or p > 100}


# ------------------------------------------------------------------------------------- planeamiento y cierre


def proyeccion(e0: float, tasas: dict[str, float], anos: int) -> dict[str, list[float]]:
    """E_t = E_0·(1+g)^t para cada escenario (una sola tasa por escenario, con su fuente citada)."""
    return {esc: [e0 * (1 + g) ** t for t in range(anos + 1)] for esc, g in tasas.items()}


def cierre_energia(potencia_kw: float, horas: float, factor_planta: float) -> float:
    """E = P·h·FP. ENFICC ≠ FP: la ENFICC es la energía firme en hidrología crítica, el FP es el promedio."""
    if not 0 <= factor_planta <= 1:
        raise ValueError("el factor de planta debe estar entre 0 y 1")
    return potencia_kw * horas * factor_planta


def margen_reserva(capacidad_mw: float, demanda_pico_mw: float, base: str) -> float:
    """(capacidad − pico)/pico. `base` debe declararse: "nominal" o "firme" (ENFICC). En Colombia lo relevante es la firme."""
    if base not in ("nominal", "firme"):
        raise ValueError('declare base = "nominal" o "firme"')
    if demanda_pico_mw <= 0:
        raise ValueError("la demanda pico debe ser > 0")
    return (capacidad_mw - demanda_pico_mw) / demanda_pico_mw


# ------------------------------------------------------------------------------------------------------------ CLI


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ejemplo", action="store_true", help="G3 del curso, dos nodos y microrred")
    ap.add_argument("--ofertas")
    ap.add_argument("--demanda")
    ap.add_argument("--hora", type=int)
    ap.add_argument("--zona", default=None)
    a = ap.parse_args(argv)
    if a.ejemplo:
        a.ofertas = os.path.join(AQUI, "datos_prueba", "g3_ofertas.csv")
        a.demanda = os.path.join(AQUI, "datos_prueba", "g3_demanda.csv")
    if not (a.ofertas and a.demanda):
        ap.error("use --ejemplo o --ofertas y --demanda")
    ofertas, dem = leer_ofertas(a.ofertas), leer_demanda(a.demanda)
    zonas = [a.zona] if a.zona else list(dem)
    horas = [a.hora] if a.hora is not None else range(24)
    print(f"{'zona':<10} {'hora':>4} {'planta marginal':<24} {'precio $/kWh':>12}")
    for z in zonas:
        for h in horas:
            r = merito(ofertas, dem[z][h], h, z)
            nombre = r.planta_marginal or f"DÉFICIT {r.deficit:,.0f} kWh"
            extra = f" (empate: {', '.join(r.empatadas)})" if r.empatadas else ""
            print(f"{z:<10} {h:>4} {nombre:<24} {r.precio if r.precio is not None else '-':>12}{extra}")
    if a.ejemplo:
        n = dos_nodos(10, 0.01, 500, 13, 0.02, 1500, 400)
        print(f"\nDos nodos (MEC p.64): sin límite π = {n['uninodal']['pi']:.2f}; con 400 MW → π_A = {n['pi_a']:.0f}, "
              f"π_B = {n['pi_b']:.0f}, renta = {n['renta']:,.0f} $/h")
        m = microrred_curso()
        print(f"Microrred del curso (sin SOC): objetivo = {m['objetivo']:,.2f}; no atendida = {sum(m['no_atendida']):.1f} kWh "
              "→ la batería entrega energía que nunca cargó (defecto B-MC4)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
