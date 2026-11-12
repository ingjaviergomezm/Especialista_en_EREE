#!/usr/bin/env python3
"""Modelos 0D de recursos y tecnologías distintas de la FV, más la matriz de decisión multicriterio (skill proyectos-er).

Nivel: PERFIL o PREFACTIBILIDAD. Responden a la pregunta "¿cuánta energía produce en promedio?". El diseño de dispositivos
(FEM/CFD) queda fuera de alcance. La oceánica también queda fuera, y la geotermia solo se trata a nivel de perfil (brecha B-ER3).

Fuentes del método:
- Curso 05 (EOL, HID, BIO, GEO e INT; nivel N4) y curso 06 (M1 p.70–95, nivel N2).
- Densidad del aire con la altitud: SUPUESTO estándar, atmósfera ISA, ρ = 1,225·(1 − 2,25577e-5·z)^4,2559.
- Matriz de factores ponderados: curso 08 (TEN, N3) y lección del curso 05: el total de la matriz siempre lo calcula
  un script.

Uso:
    python recursos_0d.py --ejemplo
"""
from __future__ import annotations

import argparse
import math
from typing import Callable, Sequence

RHO_STD = 1.225       # kg/m³ al nivel del mar, 15 °C
BETZ = 16 / 27
G = 9.81

# ------------------------------------------------------------------------------------------------ generales


def factor_planta(energia_kwh: float, potencia_kw: float, horas: float) -> float:
    """FP = energía real / (potencia nominal × horas del periodo)."""
    return energia_kwh / (potencia_kw * horas)


def horas_equivalentes(energia_kwh: float, potencia_kw: float) -> float:
    """Tiempo característico = energía anual / potencia instalada."""
    return energia_kwh / potencia_kw


# ------------------------------------------------------------------------------------------------------ eólica


def densidad_aire(altitud_m: float, presion_hpa: float | None = None, temp_c: float | None = None) -> float:
    """ρ (kg/m³). Con presión y temperatura del sitio: ρ = p/(R·T) (preferida). Sin ellas: atmósfera estándar ISA,
    que en clima templado de montaña sobrestima ρ (Manizales: 0,99 ISA vs. ≈ 0,94 con p y T) → declararlo."""
    if presion_hpa is not None and temp_c is not None:
        if presion_hpa <= 0 or temp_c <= -100:
            raise ValueError("presión o temperatura fuera de rango")
        return presion_hpa * 100 / (287.05 * (temp_c + 273.15))
    if not -500 <= altitud_m <= 6000:
        raise ValueError("altitud fuera de −500…6 000 m")
    return RHO_STD * (1 - 2.25577e-5 * altitud_m) ** 4.2559


def potencia_viento(v: float, area_m2: float, rho: float = RHO_STD, cp: float = 1.0) -> float:
    """P (W) = ½·ρ·A·v³·Cp. Con cp = 1 se obtiene la potencia disponible en el viento."""
    if cp > BETZ + 1e-9 and cp != 1.0:
        raise ValueError(f"Cp = {cp} supera el límite de Betz ({BETZ:.3f})")
    return 0.5 * rho * area_m2 * v ** 3 * cp


def velocidad_a_altura(v_ref: float, h_ref: float, h: float, beta: float) -> float:
    """Ley de potencia V = V₀·(H/H₀)^β. β: liso 0,10–0,13; rural 0,13–0,20; bosque 0,20–0,27; ciudad 0,27–0,40."""
    return v_ref * (h / h_ref) ** beta


def v_equivalente_densidad(v_sitio: float, rho_sitio: float, rho_std: float = RHO_STD, exponente: float = 1 / 3) -> float:
    """Velocidad equivalente para leer la curva de potencia (que vale para ρ_std): v_std = v_sitio·(ρ_sitio/ρ_std)^(1/3).

    El curso escribe v_sitio = v_std·(ρ_std/ρ_sitio)^(1/3), que es la misma relación despejada. El exponente pasa de 1/3 a
    2/3 entre 7–8 y 12–13 m/s (RENAC, M1 p.76–78). Aquí se usa 1/3 por defecto, como SUPUESTO declarado.
    """
    return v_sitio * (rho_sitio / rho_std) ** exponente


def weibull_pdf(v: float, k: float, c: float) -> float:
    if v < 0:
        return 0.0
    return (k / c) * (v / c) ** (k - 1) * math.exp(-((v / c) ** k))


def energia_anual_eolica(curva: Callable[[float], float], k: float, c: float, horas: float = 8760,
                         dv: float = 0.05, vmax: float = 40) -> float:
    """E = T·∫P(v)·f(v)dv (kWh si la curva está en kW). La curva de potencia es la del fabricante, medida según IEC 61400-12-1."""
    n = int(vmax / dv)
    return horas * sum(curva((i + 0.5) * dv) * weibull_pdf((i + 0.5) * dv, k, c) * dv for i in range(n))


def curva_tabla(puntos: Sequence[tuple[float, float]]) -> Callable[[float], float]:
    """Curva de potencia por interpolación lineal de una tabla (v, kW); 0 fuera del rango de la tabla."""
    pts = sorted(puntos)

    def f(v: float) -> float:
        if v < pts[0][0] or v > pts[-1][0]:
            return 0.0
        for (v0, p0), (v1, p1) in zip(pts, pts[1:]):
            if v0 <= v <= v1:
                return p0 + (p1 - p0) * (v - v0) / (v1 - v0)
        return pts[-1][1]
    return f


# --------------------------------------------------------------------------------------------------- hidráulica


def potencia_hidraulica(q_m3s: float, h_m: float, eta: float = 1.0, rho: float = 1000.0, g: float = G) -> float:
    """P (W) = ρ·g·Q·H·η. Con η = 1 da la potencia bruta. El rendimiento global típico del curso es 0,80–0,85."""
    if not 0 < eta <= 1:
        raise ValueError("η fuera de rango (0–1]")
    return rho * g * q_m3s * h_m * eta


def caudal_diseno(q_medio: float, f: float, q_ecologico: float) -> float:
    """Q_d = f·Q_m − Q_e. f entre 0,4 y 0,7 según la variabilidad del río; Q_e lo aprueba la autoridad ambiental."""
    if not 0.4 <= f <= 0.7:
        raise ValueError("f fuera del rango 0,4–0,7 del método")
    qd = f * q_medio - q_ecologico
    if qd <= 0:
        raise ValueError("el caudal de diseño resulta ≤ 0: el caudal ecológico no deja recurso aprovechable")
    return qd


MINIMO_TECNICO = {"pelton": 0.10, "kaplan": 0.25, "francis": 0.40}   # fracción del caudal de DISEÑO Q_d (curso 05, HID p.39)


def escorrentia_anual(area_m2: float, precipitacion_m: float, coef: float) -> float:
    """Volumen anual (m³) = A·P·C."""
    return area_m2 * precipitacion_m * coef


def clasificar_hidro(p_kw: float) -> str:
    """Clasificación TÉCNICA del curso 05. No es la regulatoria: en Colombia las "plantas menores" son < 20 MW
    (CREG 086/1996 y modificaciones) [verificar vigencia], y ese umbral define despacho y comercialización."""
    if p_kw < 1:
        return "pico"
    if p_kw < 100:
        return "micro"
    if p_kw <= 10_000:
        return "PCH"
    if p_kw <= 100_000:
        return "mediana"
    return "grande"


# ------------------------------------------------------------------------------------------------------ biomasa


def biomasa_disponible(area_ha: float, rendimiento_t_ha: float, f_residuo: float, f_recoleccion: float) -> float:
    """B (t/año) = A·Y·f_res·f_rec. Por ejemplo, f_res ≈ 0,25 para paja de cereal y f_rec entre 0,5 y 0,8."""
    return area_ha * rendimiento_t_ha * f_residuo * f_recoleccion


def potencia_biomasa(b_t_ano: float, pci_mj_kg: float, eta_electrica_neta: float, horas: float = 8000) -> float:
    """P eléctrica (kW) = B·PCI·η_neta / horas de operación.

    η_neta es la eficiencia eléctrica NETA de la planta (del fabricante). El rango 0,55–0,90 que da el curso para la
    "turbina" no es una eficiencia de ciclo (brecha B-ER11), por eso no hay valor por defecto.
    """
    if not 0 < eta_electrica_neta < 0.5:
        raise ValueError("η eléctrica neta fuera del rango plausible (0–0,5): pida el dato del fabricante")
    energia_kwh = b_t_ano * 1000 * pci_mj_kg / 3.6 * eta_electrica_neta
    return energia_kwh / horas


# ---------------------------------------------------------------------------------------------------- geotermia


def potencia_geotermica(m_kg_s: float, cp_kj_kgk: float, t_prod: float, t_rein: float, eta_ciclo: float) -> tuple[float, float]:
    """(Q térmica kW, P eléctrica kW) con Q = ṁ·cp·ΔT y P = Q·η_ciclo (η entre 0,10 y 0,20). Solo nivel PERFIL."""
    if not 0.05 <= eta_ciclo <= 0.25:
        raise ValueError("η de ciclo fuera de 0,05–0,25")
    if t_rein >= t_prod or m_kg_s <= 0:
        raise ValueError("se requiere T_producción > T_reinyección y caudal > 0")
    q = m_kg_s * cp_kj_kgk * (t_prod - t_rein)
    return q, q * eta_ciclo


# ------------------------------------------------------------------------------------------- matriz de decisión


def matriz_decision(pesos: dict[str, float], calificaciones: dict[str, dict[str, float]], escala: tuple[int, int] = (1, 5)) -> list[tuple[str, float]]:
    """Factores ponderados. Los pesos deben sumar 1 y cada criterio debe tener la escala ORIENTADA y declarada
    (p. ej. "5 = el menor costo"). Devuelve las alternativas ordenadas de mayor a menor total.
    """
    if any(w < 0 for w in pesos.values()):
        raise ValueError("los pesos no pueden ser negativos")
    if abs(sum(pesos.values()) - 1) > 1e-9:
        raise ValueError(f"los pesos suman {sum(pesos.values()):.4f}, no 1")
    resultado = []
    for alt, notas in calificaciones.items():
        faltan = set(pesos) - set(notas)
        if faltan:
            raise ValueError(f"{alt}: faltan calificaciones de {sorted(faltan)}")
        for c, v in notas.items():
            if not escala[0] <= v <= escala[1]:
                raise ValueError(f"{alt}/{c}: {v} fuera de la escala {escala}")
        resultado.append((alt, sum(pesos[c] * notas[c] for c in pesos)))
    return sorted(resultado, key=lambda x: -x[1])


def sensibilidad_pesos(pesos: dict[str, float], calificaciones: dict[str, dict[str, float]], delta: float = 0.10) -> list[dict]:
    """¿Cambia el ganador si un peso se mueve ±delta (relativo) y se renormaliza? Devuelve los casos que cambian el ganador."""
    ganador = matriz_decision(pesos, calificaciones)[0][0]
    cambios = []
    for c in pesos:
        for s in (-1, 1):
            p = dict(pesos)
            p[c] = p[c] * (1 + s * delta)
            tot = sum(p.values())
            p = {k: v / tot for k, v in p.items()}
            nuevo = matriz_decision(p, calificaciones)[0][0]
            if nuevo != ganador:
                cambios.append({"criterio": c, "variacion": s * delta, "nuevo_ganador": nuevo})
    return cambios


# ----------------------------------------------------------------------------------------------------------- CLI


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ejemplo", action="store_true")
    a = ap.parse_args(argv)
    if not a.ejemplo:
        ap.print_help()
        return 0
    v = escorrentia_anual(2e6, 0.150, 0.4)
    q = v / (365 * 24 * 3600)
    print(f"Escorrentía (curso 05, HID p.42): V = {v:,.0f} m³/año → Q = {q:.4f} m³/s; "
          f"P bruta = {potencia_hidraulica(q, 132, 1.0, g=9.8) / 1000:.2f} kW; con η = 0,8 → "
          f"{potencia_hidraulica(q, 132, 0.8, g=9.8) / 1000:.2f} kW")
    qt, pe = potencia_geotermica(50, 4.2, 160, 60, 0.15)
    print(f"Geotermia (curso 06, M1 p.93): Q = {qt / 1000:.0f} MWt → P = {pe / 1000:.2f} MWe (solo nivel perfil)")
    print(f"Densidad del aire a 2 150 m (Manizales): {densidad_aire(2150):.3f} kg/m³ (SUPUESTO ISA)")
    pesos = {"tecnico": 0.4, "economico": 0.3, "ambiental": 0.2, "social": 0.1}
    cal = {"eolica": {"tecnico": 3, "economico": 3, "ambiental": 2, "social": 3}}
    print(f"Matriz (lección del curso 05): eólica = {matriz_decision(pesos, cal)[0][1]:.1f} (el entregable decía 2,5)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
