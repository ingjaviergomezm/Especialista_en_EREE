#!/usr/bin/env python3
"""Línea base energética (LBEn), indicadores de desempeño (IDEn), línea meta y CUSUM (skill gestion-energetica).

Método:
- LBEn por regresión lineal E = m·P + b (E = energía del periodo; P = variable relevante: producción, grados-día,
  ocupación). b es el consumo fijo y m el consumo variable por unidad. Fuentes: curso 03, guías U3/U4 (N2). La
  regresión la validó la profesora en mi A4 (lógica N5).
- Requisitos: al menos 12 periodos sin cambios estructurales; se declaran R², n y el rango de validez (no se extrapola);
  los atípicos se señalan, no se borran. Es un SUPUESTO estándar alineado con ISO 50006:2023, verificado en vivo.
- CUSUM = Σ(E_real − E_modelo): la pendiente negativa indica ahorro. SUPUESTO estándar (brecha B-GE2: el material no
  trae la fórmula correcta).
- Ahorro % = (E_modelo − E_real) / E_modelo; positivo = ahorro (lección L3 del curso 03).
- Línea meta: la misma regresión, pero solo con los periodos que quedaron por debajo de la LB. DEBE quedar por debajo de
  la LB en todo el rango de P (lección L1: en mi A4 quedó por encima). SUPUESTO estándar (brecha B-GE1).

Entrada CSV: columnas `periodo,variable,energia_kwh` (y opcionalmente `fase` = base | reporte).

Uso:
    python linea_base.py --ejemplo
    python linea_base.py --csv consumos.csv
"""
from __future__ import annotations

import argparse
import csv
import math
import warnings
from dataclasses import dataclass
from typing import Sequence


@dataclass
class Modelo:
    m: float
    b: float
    r2: float
    n: int
    p_min: float
    p_max: float
    residuos: list[float]
    sigma: float

    def __call__(self, p: float) -> float:
        return self.m * p + self.b

    def predecir(self, p: float, permitir_extrapolar: bool = False) -> float:
        if not permitir_extrapolar and not (self.p_min <= p <= self.p_max):
            raise ValueError(f"P = {p} está fuera del rango de validez [{self.p_min}, {self.p_max}] de la línea base")
        return self(p)

    def texto(self) -> str:
        return f"E = {self.m:.4f}·P + {self.b:.2f}  (R² = {self.r2:.3f}, n = {self.n}, P ∈ [{self.p_min:g}, {self.p_max:g}])"


R2_MINIMO = 0.75   # SUPUESTO: umbral de práctica común para aceptar una LBEn de regresión; se declara en el informe


def regresion(p: Sequence[float], e: Sequence[float], minimo_periodos: int = 12) -> Modelo:
    """Mínimos cuadrados ordinarios. Error si la variable no varía; advertencia si hay menos de 12 periodos."""
    if len(p) != len(e):
        raise ValueError("P y E deben tener el mismo número de datos")
    n = len(p)
    if n < 3:
        raise ValueError("se necesitan al menos 3 periodos")
    if n < minimo_periodos:
        warnings.warn(f"solo {n} periodos (< {minimo_periodos}): la LBEn no capta la estacionalidad; declararlo")
    mp, me = sum(p) / n, sum(e) / n
    sxx = sum((x - mp) ** 2 for x in p)
    if sxx == 0:
        raise ValueError("la variable relevante no varía: la regresión es indefinida; use otro IDEn o otra variable")
    sxy = sum((x - mp) * (y - me) for x, y in zip(p, e))
    m = sxy / sxx
    b = me - m * mp
    res = [y - (m * x + b) for x, y in zip(p, e)]
    sst = sum((y - me) ** 2 for y in e)
    r2 = 1 - sum(r * r for r in res) / sst if sst else 1.0
    sigma = math.sqrt(sum(r * r for r in res) / (n - 2)) if n > 2 else 0.0
    if r2 < R2_MINIMO:
        warnings.warn(f"R² = {r2:.3f} < {R2_MINIMO} (umbral SUPUESTO de práctica común; ISO 50006 no fija uno): "
                      "la variable no explica el consumo; buscar otra variable o usar un IDEn de cociente/consumo medido")
    if m <= 0:
        warnings.warn(f"pendiente m = {m:.4g} ≤ 0: más producción con menos energía no es físico; revisar datos o variable")
    return Modelo(m, b, r2, n, min(p), max(p), res, sigma)


def atipicos(modelo: Modelo, k: float = 2.0) -> list[int]:
    """Índices de periodos con |residuo| > k·σ. Se explican con el cliente; no se borran en silencio."""
    return [i for i, r in enumerate(modelo.residuos) if modelo.sigma and abs(r) > k * modelo.sigma]


# ------------------------------------------------------------------------------------------------------- IDEn


def cee(energia: float, produccion: float) -> float:
    """Consumo específico = energía / unidad producida (p. ej. kWh/t)."""
    if produccion <= 0:
        raise ValueError("la producción debe ser > 0")
    return energia / produccion


def iee(energia_usada: float, energia_optima: float) -> float:
    """Índice de eficiencia = usada / óptima; > 1 indica sobreconsumo."""
    return energia_usada / energia_optima


def ahorro_pct(e_modelo: float, e_real: float) -> float:
    """(modelo − real)/modelo. Positivo = ahorro."""
    if e_modelo <= 0:
        raise ValueError("el consumo modelado debe ser > 0 para expresar el ahorro en %")
    return (e_modelo - e_real) / e_modelo


def cusum(e_real: Sequence[float], e_modelo: Sequence[float]) -> list[float]:
    """Suma acumulada de (real − modelo). Si baja, hay ahorro; un cambio de pendiente marca el periodo en que cambió el desempeño."""
    acumulado, salida = 0.0, []
    for r, m in zip(e_real, e_modelo):
        acumulado += r - m
        salida.append(acumulado)
    return salida


# --------------------------------------------------------------------------------------------------- línea meta


def verificar_meta_bajo_base(lb: Modelo, meta: Modelo, p_min: float, p_max: float) -> None:
    """Como ambas líneas son rectas, basta revisar los extremos del rango de P."""
    for p in (p_min, p_max):
        if meta(p) > lb(p) + 1e-9:
            raise ValueError(f"la línea meta queda POR ENCIMA de la línea base en P = {p:g} "
                             f"({meta(p):.1f} > {lb(p):.1f}): contradice su definición (lección L1)")


def linea_meta(p: Sequence[float], e: Sequence[float], lb: Modelo | None = None) -> Modelo:
    """Regresión solo con los periodos por debajo de la LB. Requiere al menos 3 de esos periodos."""
    lb = lb or regresion(p, e)
    if lb.r2 < R2_MINIMO or lb.m <= 0:
        raise ValueError(f"LBEn de baja calidad (R² = {lb.r2:.3f}, m = {lb.m:.4g}): no se calcula línea meta")
    if lb.n < 12:
        raise ValueError(f"LBEn PROVISIONAL (n = {lb.n} < 12): no se calcula línea meta; recalcular al completar 12 periodos")
    sel = [(x, y) for x, y in zip(p, e) if y < lb(x)]
    if len(sel) < 6:
        raise ValueError("menos de 6 periodos bajo la LB: no hay base para una línea meta; declarar la meta como % de la LB")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        meta = regresion([x for x, _ in sel], [y for _, y in sel], minimo_periodos=0)
    verificar_meta_bajo_base(lb, meta, lb.p_min, lb.p_max)
    return meta


def potencial_buenas_practicas(lb: Modelo, meta: Modelo, p: Sequence[float]) -> float:
    """kWh que se habrían ahorrado en los periodos dados si se hubiera operado siempre sobre la línea meta."""
    return sum(lb(x) - meta(x) for x in p)


# ---------------------------------------------------------------------------------------------------------- CLI


def _leer_csv(ruta: str):
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        filas = list(csv.DictReader(f))
    return filas


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ejemplo", action="store_true", help="datos sintéticos generados con E = 1,6876·P + 127,13")
    ap.add_argument("--csv")
    a = ap.parse_args(argv)
    if a.ejemplo:
        p = [100, 120, 90, 150, 130, 110, 160, 140, 95, 125, 135, 115]
        ruido = [6, -5, 4, -7, 3, -2, 5, -6, -3, 4, -4, 5]
        e = [1.6876 * x + 127.13 + r for x, r in zip(p, ruido)]
        filas = [{"periodo": f"M{i + 1}", "variable": x, "energia_kwh": y, "fase": "base"} for i, (x, y) in enumerate(zip(p, e))]
    elif a.csv:
        filas = _leer_csv(a.csv)
    else:
        ap.error("use --ejemplo o --csv")
    base = [f for f in filas if f.get("fase", "base") in ("base", "", None)]
    reporte = [f for f in filas if f.get("fase") == "reporte"]
    p = [float(f["variable"]) for f in base]
    e = [float(f["energia_kwh"]) for f in base]
    lb = regresion(p, e)
    print("Línea base:", lb.texto())
    if atipicos(lb):
        print("  Periodos atípicos (> 2σ), a explicar con el cliente:", [base[i]["periodo"] for i in atipicos(lb)])
    try:
        meta = linea_meta(p, e, lb)
        print("Línea meta:", meta.texto())
        print(f"  Potencial con buenas prácticas en el periodo base: {potencial_buenas_practicas(lb, meta, p):,.0f} kWh")
    except ValueError as err:
        print("Línea meta: no calculada —", err)
    if reporte:
        pr = [float(f["variable"]) for f in reporte]
        er = [float(f["energia_kwh"]) for f in reporte]
        mod = [lb.predecir(x, permitir_extrapolar=True) for x in pr]
        fuera = [not (lb.p_min <= x <= lb.p_max) for x in pr]
        cs = cusum(er, mod)
        print(f"{'periodo':>10} {'real':>10} {'modelo':>10} {'CUSUM':>10}")
        for f, r, m_, c, fu in zip(reporte, er, mod, cs, fuera):
            print(f"{f['periodo']:>10} {r:>10,.0f} {m_:>10,.0f} {c:>10,.0f}" + ("  * fuera del rango de la LB" if fu else ""))
        if any(fuera):
            print(f"* {sum(fuera)} periodo(s) fuera de [{lb.p_min:g}, {lb.p_max:g}]: el modelo extrapola; "
                  "declararlo o ajustar la LB (ISO 50006, criterios de ajuste).")
        print(f"Ahorro del periodo de reporte: {ahorro_pct(sum(mod), sum(er)):.1%} (positivo = ahorro)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
