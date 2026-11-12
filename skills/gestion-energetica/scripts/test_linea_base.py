"""Pruebas de linea_base.py: ejemplos del curso 03 (U1, A4), cálculos a mano y casos borde."""
import warnings

import pytest

from linea_base import (Modelo, ahorro_pct, atipicos, cee, cusum, iee, linea_meta, potencial_buenas_practicas,
                        regresion, verificar_meta_bajo_base)

P = [100, 120, 90, 150, 130, 110, 160, 140, 95, 125, 135, 115]


def test_recupera_coeficientes_exactos():
    e = [1.6876 * x + 127.13 for x in P]
    m = regresion(P, e)
    assert m.m == pytest.approx(1.6876) and m.b == pytest.approx(127.13) and m.r2 == pytest.approx(1.0)


def test_cee_cemento_u1():
    assert cee(1_000_000, 500) == pytest.approx(2000)
    assert cee(1_000_000, 500) * 0.85 == pytest.approx(1700)


def test_iee_aire_acondicionado_u1():
    assert iee(12_000, 9_500) == pytest.approx(1.263, abs=1e-3)


def test_cusum_a_mano():
    assert cusum([105, 98, 95], [100, 100, 100]) == [5, 3, -2]


def test_signo_del_ahorro():
    assert ahorro_pct(100, 90) == pytest.approx(0.10)   # consumió menos → ahorro positivo
    assert ahorro_pct(100, 110) < 0


def test_leccion_l1_meta_por_encima_es_error():
    lb = Modelo(1.6876, 127.13, 0.9, 12, 90, 160, [], 1)
    meta_a4 = Modelo(1.7598, 136.94, 0.9, 6, 90, 160, [], 1)    # la de mi A4
    with pytest.raises(ValueError, match="POR ENCIMA"):
        verificar_meta_bajo_base(lb, meta_a4, 90, 160)


def test_linea_meta_queda_debajo():
    ruido = [6, -5, 4, -7, 3, -2, 5, -6, -3, 4, -4, 5]
    e = [1.6876 * x + 127.13 + r for x, r in zip(P, ruido)]
    lb = regresion(P, e)
    meta = linea_meta(P, e, lb)
    assert all(meta(x) <= lb(x) for x in (min(P), max(P)))
    assert potencial_buenas_practicas(lb, meta, P) > 0


def test_atipico_detectado():
    e = [1.6876 * x + 127.13 for x in P]
    e[3] += 200
    assert 3 in atipicos(regresion(P, e))


# ---------- casos borde

def test_variable_constante_es_error():
    with pytest.raises(ValueError, match="no varía"):
        regresion([100] * 12, list(range(12)))


def test_menos_de_12_periodos_advierte():
    with pytest.warns(UserWarning):
        regresion([1, 2, 3, 4], [2, 4, 6, 8.5])


def test_extrapolacion_bloqueada():
    m = regresion(P, [2 * x for x in P])
    with pytest.raises(ValueError, match="fuera del rango"):
        m.predecir(500)
    assert m.predecir(500, permitir_extrapolar=True) == pytest.approx(1000)


def test_meta_sin_puntos_suficientes():
    e = [2 * x for x in P]   # ajuste perfecto: ningún punto bajo la LB
    with pytest.raises(ValueError, match="menos de 6"):
        linea_meta(P, e)


def test_cee_produccion_cero():
    with pytest.raises(ValueError):
        cee(100, 0)


def test_meta_bloqueada_con_lb_provisional():
    p6 = P[:6]
    e6 = [2 * x + (5 if i % 2 else -5) for i, x in enumerate(p6)]
    with pytest.warns(UserWarning):
        lb = regresion(p6, e6)
    with pytest.raises(ValueError, match="PROVISIONAL"):
        linea_meta(p6, e6, lb)


def test_regresion_mala_advierte_y_bloquea_meta():
    import random
    rnd = random.Random(1)
    p = [100 + 10 * i for i in range(12)]
    e = [rnd.uniform(500, 1500) for _ in p]
    with pytest.warns(UserWarning, match="R²"):
        lb = regresion(p, e)
    with pytest.raises(ValueError, match="baja calidad"):
        linea_meta(p, e, lb)
