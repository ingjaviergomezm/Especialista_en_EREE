"""Pruebas de recursos_0d.py: ejemplos de los cursos 05 y 06, cálculos a mano y casos borde."""
import math

import pytest

from recursos_0d import (BETZ, caudal_diseno, clasificar_hidro, curva_tabla, densidad_aire, energia_anual_eolica,
                         escorrentia_anual, factor_planta, horas_equivalentes, matriz_decision, potencia_biomasa,
                         potencia_geotermica, potencia_hidraulica, potencia_viento, sensibilidad_pesos,
                         v_equivalente_densidad, velocidad_a_altura, biomasa_disponible)


def test_factor_planta_y_horas_hid():
    assert factor_planta(648_000, 1_000, 720) == pytest.approx(0.90)       # HID p.45
    assert horas_equivalentes(108e6, 20e3) == pytest.approx(5400)          # HID p.47


def test_escorrentia_hid_p42():
    v = escorrentia_anual(2e6, 0.150, 0.4)
    q = v / (365 * 24 * 3600)
    assert v == pytest.approx(120_000) and q == pytest.approx(0.0038, abs=1e-4)
    assert potencia_hidraulica(q, 132, 0.8, g=9.8) / 1000 == pytest.approx(3.9, abs=0.05)


def test_geotermia_m1_p93():
    q, p = potencia_geotermica(50, 4.2, 160, 60, 0.15)
    assert q == pytest.approx(21_000) and p == pytest.approx(3_150)


def test_potencia_viento_a_mano():
    assert potencia_viento(10, 1.0) == pytest.approx(612.5)
    assert potencia_viento(10, 1.0, cp=BETZ) == pytest.approx(612.5 * 16 / 27)


def test_betz():
    with pytest.raises(ValueError):
        potencia_viento(10, 1, cp=0.62)


def test_densidad_y_correccion():
    assert densidad_aire(0) == pytest.approx(1.225)
    rho = densidad_aire(2150)
    assert 0.98 < rho < 1.0
    # a menor densidad, la velocidad equivalente para leer la curva es menor
    assert v_equivalente_densidad(8, rho) < 8


def test_perfil_vertical():
    assert velocidad_a_altura(5, 10, 80, 0.14) == pytest.approx(5 * 8 ** 0.14)


def test_energia_eolica_curva_constante():
    # curva de 1 kW constante entre 0 y 40 m/s → E ≈ 8 760 kWh (la integral de la Weibull es 1)
    e = energia_anual_eolica(lambda v: 1.0, k=2, c=7)
    assert e == pytest.approx(8760, rel=1e-3)


def test_curva_tabla():
    f = curva_tabla([(3, 0), (12, 2000), (25, 2000)])
    assert f(7.5) == pytest.approx(1000) and f(26) == 0 and f(2) == 0


def test_caudal_diseno_y_borde():
    assert caudal_diseno(10, 0.7, 3) == pytest.approx(4)
    with pytest.raises(ValueError):
        caudal_diseno(10, 0.4, 5)            # Q_e consume todo
    with pytest.raises(ValueError):
        caudal_diseno(10, 0.9, 1)            # f fuera del método


def test_clasificacion_hidro():
    assert clasificar_hidro(50) == "micro" and clasificar_hidro(6000) == "PCH"


def test_biomasa():
    b = biomasa_disponible(100, 4, 0.25, 0.6)
    assert b == pytest.approx(60)
    # 60 t × 15 MJ/kg = 900 000 MJ = 250 000 kWh térmicos × 0,2 = 50 000 kWh / 8 000 h = 6,25 kW
    assert potencia_biomasa(60, 15, 0.20) == pytest.approx(6.25)
    with pytest.raises(ValueError):
        potencia_biomasa(60, 15, 0.7)        # "η de turbina" del curso no es eficiencia neta


def test_matriz_leccion_curso_05():
    pesos = {"t": 0.4, "e": 0.3, "a": 0.2, "s": 0.1}
    cal = {"eolica": {"t": 3, "e": 3, "a": 2, "s": 3}, "solar": {"t": 5, "e": 5, "a": 4, "s": 5}}
    r = matriz_decision(pesos, cal)
    assert r[0] == ("solar", pytest.approx(4.8)) and r[1][1] == pytest.approx(2.8)


def test_matriz_pesos_y_escala():
    with pytest.raises(ValueError):
        matriz_decision({"a": 0.5, "b": 0.4}, {"x": {"a": 1, "b": 1}})
    with pytest.raises(ValueError):
        matriz_decision({"a": 1.0}, {"x": {"a": 7}})


def test_sensibilidad_pesos_detecta_empate_fragil():
    pesos = {"a": 0.5, "b": 0.5}
    cal = {"x": {"a": 5, "b": 1}, "y": {"a": 1, "b": 4.9}}
    assert sensibilidad_pesos(pesos, cal)  # mover ±10 % un peso cambia el ganador


def test_densidad_con_presion_y_temperatura():
    from recursos_0d import densidad_aire
    assert densidad_aire(2150, 785, 17) == pytest.approx(0.943, abs=0.002)
    with pytest.raises(ValueError):
        densidad_aire(90000)


def test_geotermia_y_pesos_invalidos():
    from recursos_0d import potencia_geotermica, matriz_decision
    with pytest.raises(ValueError):
        potencia_geotermica(10, 4.18, 80, 90, 0.15)
    with pytest.raises(ValueError):
        matriz_decision({"a": 1.5, "b": -0.5}, {"x": {"a": 3, "b": 3}})
