#!/usr/bin/env python3
"""Dimensionamiento de un sistema fotovoltaico conectado a red, a nivel de perfil o prefactibilidad (skill proyectos-er).

Calcula: kWp requeridos para cubrir un consumo, número de módulos, energía anual (E = Pp·H·PR), producción específica,
PR a partir de una medición, relación DC/AC con alertas, módulos en serie máximos y mínimos por temperatura,
strings por MPPT, P50/P90 e inclinación recomendada.

Fuentes del método:
- Guías del curso 06 (M1 p.56–69 y M2 p.36–117, nivel N2). Forma estándar de las fórmulas que en la guía están como imagen
  (brecha B-ER10).
- Curso 05 (SOL p.24, N4): β_opt = 3,7 + 0,69·|φ| con un mínimo de 15° para autolimpieza.
- Casos de prueba: informe PVsyst del Lote 10 (N5) y ejemplo de Manizales (M2 p.116–117).

Esto NO es ingeniería de detalle: los planos, las memorias y el cumplimiento del RETIE los firma un profesional matriculado.
El modo aislado (baterías, autonomía) no está cubierto (brecha B-ER2).

Uso:
    python fv_dimensionamiento.py --ejemplo
    python fv_dimensionamiento.py --consumo-mes 300 --hsp 4.8 --pr 0.78 --wp 590
    python fv_dimensionamiento.py --strings --voc 49.5 --beta-voc -0.0028 --tmin 10 --vmax 1500 \
        --vmp 41.5 --beta-vmp -0.0035 --tcel 69 --vmppt-min 500 --imp 13.36 --imax-mppt 40
"""
from __future__ import annotations

import argparse
import math

Z_P90 = 1.2816   # cuantil normal estándar para una excedencia del 90 %
Z = {"P75": 0.6745, "P90": 1.2816, "P95": 1.6449, "P99": 2.3263}


# --------------------------------------------------------------------------------------------------- energía


def energia_anual(p_kwp: float, h_plano_kwh_m2: float, pr: float) -> float:
    """E (kWh/periodo) = Pp (kWp) × H en el plano (kWh/m²·periodo, numéricamente = horas de sol pico) × PR."""
    _validar_pr(pr)
    if p_kwp < 0 or h_plano_kwh_m2 < 0:
        raise ValueError("potencia e irradiación deben ser ≥ 0")
    return p_kwp * h_plano_kwh_m2 * pr


def produccion_especifica(energia_kwh: float, p_kwp: float) -> float:
    """kWh/kWp en el periodo de la energía."""
    return energia_kwh / p_kwp


def pr_medido(energia_kwh: float, p_kwp: float, h_plano_kwh_m2: float) -> float:
    """PR = E real / (Pp × H plano) (IEC 61724-1:2021, forma simplificada sin corrección de temperatura)."""
    pr = energia_kwh / (p_kwp * h_plano_kwh_m2)
    if pr > 1:
        raise ValueError(f"PR = {pr:.3f} > 1: los datos no cierran (revise la energía, la potencia o la irradiación en el plano)")
    return pr


def kwp_requerido(consumo_kwh_ano: float, h_plano_kwh_m2_ano: float, pr: float, cobertura: float = 1.0) -> float:
    """kWp para cubrir una fracción del consumo anual (balance anual: no dice cuánto es autoconsumo y cuánto excedente)."""
    _validar_pr(pr)
    if not 0 < cobertura <= 1.5:
        raise ValueError("cobertura fuera de rango (0–1,5)")
    return consumo_kwh_ano * cobertura / (h_plano_kwh_m2_ano * pr)


def numero_modulos(p_kwp: float, wp_modulo: float) -> int:
    return math.ceil(p_kwp * 1000 / wp_modulo - 1e-9)


def potencia_modulo(vmp: float, imp: float) -> float:
    """Wp = Vmp × Imp (STC)."""
    return vmp * imp


def _validar_pr(pr: float) -> None:
    if not 0 < pr <= 1:
        raise ValueError(f"PR = {pr} fuera de rango (0–1]")
    # rangos de referencia del curso: 0,70–0,85 típico; < 0,70 indica deficiencias


def evaluar_pr(pr: float) -> str:
    """Clasificación del curso 06 (M1 p.56–61)."""
    if pr < 0.70:
        return "deficiente (< 70 %): revisar diseño, construcción u O&M"
    if pr < 0.78:
        return "bajo (70–78 %)"
    if pr <= 0.80:
        return "aceptable (78–80 %)"
    if pr <= 0.92:
        return "bueno o excelente (> 80 %)"
    return "sospechoso (> 92 %): verificar la irradiación de referencia"


# ------------------------------------------------------------------------------------------------- DC/AC


def dc_ac(p_dc_kwp: float, p_ac_kw: float) -> tuple[float, str]:
    """Relación DC/AC y alerta. Guía del curso: 1,2 (clima frío) a 1,4 (clima cálido); los fabricantes admiten 1,2–1,4."""
    r = p_dc_kwp / p_ac_kw
    if r > 1.5:
        alerta = "ALERTA FUERTE: > 1,5, con clipping y estrés térmico altos; confirmar con el fabricante y simular"
    elif r > 1.4:
        alerta = "por encima de 1,4: revisar el clipping en la simulación y el límite del fabricante"
    elif r < 1.0:
        alerta = "< 1,0: inversor sobredimensionado (sobrecosto)"
    elif r < 1.2:
        alerta = "por debajo de 1,2: válido, pero el inversor queda subutilizado"
    else:
        alerta = "dentro de la guía 1,2–1,4"
    return r, alerta


# ---------------------------------------------------------------------------------------------- strings


def v_a_temperatura(v_stc: float, beta_por_c: float, t_c: float) -> float:
    """V(T) = V_STC · [1 + β·(T − 25)], con β en fracción/°C (p. ej. −0,0028 = −0,28 %/°C) de la ficha técnica."""
    if not -0.01 < beta_por_c < 0:
        raise ValueError(f"β = {beta_por_c}: debe ser negativo y en fracción/°C (−0,28 %/°C → −0.0028)")
    return v_stc * (1 + beta_por_c * (t_c - 25))


def n_serie_max(v_max_inversor: float, voc_stc: float, beta_voc: float, t_min: float) -> int:
    """Máximo de módulos en serie: la Voc a la temperatura mínima histórica no debe superar la tensión máxima del inversor."""
    return math.floor(v_max_inversor / v_a_temperatura(voc_stc, beta_voc, t_min) + 1e-9)


def n_serie_min(v_mppt_min: float, vmp_stc: float, beta_vmp: float, t_cel_max: float) -> int:
    """Mínimo de módulos en serie: la Vmp a la temperatura máxima de celda debe quedar por encima del mínimo del MPPT."""
    return math.ceil(v_mppt_min / v_a_temperatura(vmp_stc, beta_vmp, t_cel_max) - 1e-9)


def strings_por_mppt(i_max_mppt: float, imp: float, isc: float | None = None, isc_max_mppt: float | None = None) -> int:
    """Strings en paralelo por MPPT limitados por la corriente de entrada (y la Isc admisible, si se conoce)."""
    n = math.floor(i_max_mppt / imp + 1e-9)
    if isc is not None and isc_max_mppt is not None:
        n = min(n, math.floor(isc_max_mppt / isc + 1e-9))
    return n


def ventana_serie(v_max_inversor, voc_stc, beta_voc, t_min, v_mppt_min, vmp_stc, beta_vmp, t_cel_max,
                  v_mppt_max: float | None = None) -> dict:
    """Ventana de módulos en serie. Con `v_mppt_max`, limita además n para que Vmp a la temperatura mínima quede
    dentro del rango MPPT (si no, el inversor no sigue el punto de máxima potencia en mañanas frías)."""
    nmax = n_serie_max(v_max_inversor, voc_stc, beta_voc, t_min)
    nmin = n_serie_min(v_mppt_min, vmp_stc, beta_vmp, t_cel_max)
    vmp_tmin = v_a_temperatura(vmp_stc, beta_vmp, t_min)
    nmax_mppt = math.floor(v_mppt_max / vmp_tmin + 1e-9) if v_mppt_max else None
    n_tope = min(nmax, nmax_mppt) if nmax_mppt is not None else nmax
    return {"n_min": nmin, "n_max": n_tope, "n_max_por_voc": nmax, "n_max_por_mppt": nmax_mppt,
            "factible": nmin <= n_tope, "voc_tmin": v_a_temperatura(voc_stc, beta_voc, t_min),
            "vmp_tmax": v_a_temperatura(vmp_stc, beta_vmp, t_cel_max), "vmp_tmin": vmp_tmin}


# ------------------------------------------------------------------------------------------- incertidumbre


def sigma_combinada(*incertidumbres: float) -> float:
    """σ total = raíz de la suma de cuadrados (incertidumbres independientes, en fracción)."""
    return math.sqrt(sum(u * u for u in incertidumbres))


def p_excedencia(p50: float, sigma: float, nivel: str = "P90") -> float:
    """P_x = P50 · (1 − z·σ), con una distribución normal. P90 = la energía que se supera 9 de cada 10 años."""
    if not 0 <= sigma < 1 / Z[nivel]:
        raise ValueError(f"σ = {sigma} fuera de rango (fracción entre 0 y {1 / Z[nivel]:.2f})")
    return p50 * (1 - Z[nivel] * sigma)


# ------------------------------------------------------------------------------------------------ geometría


def inclinacion_recomendada(latitud: float) -> float:
    """β_opt = 3,7 + 0,69·|φ| (curso 05), con un mínimo de 15° para autolimpieza. En Colombia casi siempre manda el 15°."""
    return max(3.7 + 0.69 * abs(latitud), 15.0)


def distancia_entre_filas(altura_obstaculo_m: float, elevacion_solar_deg: float,
                          azimut_solar_deg: float = 0.0, azimut_panel_deg: float = 0.0) -> float:
    """d = h / tan(α) · cos(γ_sol − γ_panel). Se evalúa con la elevación solar más baja entre 9 y 15 h (carta solar)."""
    if elevacion_solar_deg <= 0:
        raise ValueError("la elevación solar debe ser > 0")
    # con el sol detrás del plano (|Δγ| > 90°) la fila no sombrea: distancia 0
    return max(0.0, altura_obstaculo_m / math.tan(math.radians(elevacion_solar_deg)) * math.cos(
        math.radians(azimut_solar_deg - azimut_panel_deg)))


# ----------------------------------------------------------------------------------------------------- CLI


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ejemplo", action="store_true", help="verifica el caso Lote 10 (Mérida) y el ejemplo de Manizales")
    ap.add_argument("--consumo-mes", type=float, help="kWh/mes a cubrir")
    ap.add_argument("--hsp", type=float, help="irradiación en el plano, kWh/m²·día (= horas de sol pico)")
    ap.add_argument("--pr", type=float, help="performance ratio; si se omite se usa 0,78 marcado como SUPUESTO no aprobado")
    ap.add_argument("--vmppt-max", type=float, help="tensión máxima del rango MPPT (V)")
    ap.add_argument("--isc", type=float, help="Isc del módulo (A)")
    ap.add_argument("--isc-max", type=float, help="Isc máxima admisible por MPPT (A)")
    ap.add_argument("--wp", type=float, help="potencia del módulo (Wp)")
    ap.add_argument("--cobertura", type=float, default=1.0)
    ap.add_argument("--pac", type=float, help="potencia AC del inversor (kW) para calcular DC/AC")
    ap.add_argument("--strings", action="store_true", help="calcular la ventana de módulos en serie")
    for nombre in ("voc", "beta-voc", "tmin", "vmax", "vmp", "beta-vmp", "tcel", "vmppt-min", "imp", "imax-mppt"):
        ap.add_argument(f"--{nombre}", type=float)
    a = ap.parse_args(argv)

    if a.ejemplo:
        p = 4032 * 670 / 1000
        h = 1798 * 1.023
        e = 4_284_800
        print("Caso Lote 10 (Mérida, Santander; PVsyst, N5):")
        print(f"  potencia DC = {p:,.1f} kWp | DC/AC = {dc_ac(p, 1980)[0]:.3f} ({dc_ac(p, 1980)[1]})")
        print(f"  producción específica = {produccion_especifica(e, p):,.0f} kWh/kWp·año | PR = {pr_medido(e, p, h):.3f}")
        print(f"  P90 = {p_excedencia(4285, 0.031):,.0f} MWh/año (σ = 3,1 %) → 9 de cada 10 años se producen al menos esos MWh")
        print("Ejemplo de Manizales (M2 p.116): 1 000 × 620 Wp con 5 inversores de 100 kW →",
              f"DC/AC = {dc_ac(620, 500)[0]:.2f}")
        return 0
    if a.strings:
        req = [a.voc, a.beta_voc, a.tmin, a.vmax, a.vmp, a.beta_vmp, a.tcel, a.vmppt_min]
        if any(v is None for v in req):
            ap.error("--strings requiere --voc --beta-voc --tmin --vmax --vmp --beta-vmp --tcel --vmppt-min")
        v = ventana_serie(a.vmax, a.voc, a.beta_voc, a.tmin, a.vmppt_min, a.vmp, a.beta_vmp, a.tcel, a.vmppt_max)
        print(f"Voc(Tmin) = {v['voc_tmin']:.2f} V | Vmp(Tcel,max) = {v['vmp_tmax']:.2f} V | Vmp(Tmin) = {v['vmp_tmin']:.2f} V")
        print(f"Módulos en serie: mínimo {v['n_min']} y máximo {v['n_max']}" + ("" if v["factible"] else " → NO FACTIBLE"))
        if a.vmppt_max is None:
            print("  (sin --vmppt-max no se verificó que Vmp a Tmin quede dentro del MPPT)")
        if a.imp and a.imax_mppt:
            print(f"Strings por MPPT ≤ {strings_por_mppt(a.imax_mppt, a.imp, a.isc, a.isc_max)}"
                  + ("" if a.isc and a.isc_max else " (Isc no verificada: indique --isc y --isc-max)"))
        return 0
    if a.consumo_mes is None or a.hsp is None:
        ap.error("indique --consumo-mes y --hsp (o use --ejemplo / --strings)")
    if a.pr is None:
        a.pr = 0.78
        print("PR = 0,78 por defecto → SUPUESTO NO APROBADO: confirmarlo en el Registro de Supuestos.")
    kwp = kwp_requerido(a.consumo_mes * 12, a.hsp * 365, a.pr, a.cobertura)
    print(f"Potencia requerida = {kwp:,.2f} kWp para {a.cobertura:.0%} de {a.consumo_mes:,.0f} kWh/mes "
          f"(H = {a.hsp} kWh/m²·día, PR = {a.pr}) — nivel PERFIL")
    if a.wp:
        n = numero_modulos(kwp, a.wp)
        print(f"Módulos de {a.wp:.0f} Wp: {n} → {n * a.wp / 1000:,.2f} kWp instalados; "
              f"energía ≈ {energia_anual(n * a.wp / 1000, a.hsp * 365, a.pr):,.0f} kWh/año")
    if a.pac:
        r, alerta = dc_ac(kwp, a.pac)
        print(f"DC/AC = {r:.2f}: {alerta}")
    print("Supuestos a confirmar: H en el plano (atlas/IDEAM, con fecha), PR, sombras, área disponible y perfil horario "
          "(autoconsumo vs. excedentes).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
