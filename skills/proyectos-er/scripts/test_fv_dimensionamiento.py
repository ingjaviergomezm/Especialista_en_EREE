"""Pruebas de fv_dimensionamiento.py: Lote 10 (PVsyst, N5), Manizales (M2, N2), Jinko (M2), cálculo a mano y casos borde."""
import pytest

from fv_dimensionamiento import (dc_ac, distancia_entre_filas, energia_anual, evaluar_pr, inclinacion_recomendada,
                                 kwp_requerido, n_serie_max, n_serie_min, numero_modulos, p_excedencia,
                                 potencia_modulo, pr_medido, produccion_especifica, sigma_combinada, strings_por_mppt,
                                 ventana_serie)

P_L10 = 4032 * 0.670          # kWp
H_L10 = 1798 * 1.023          # kWh/m²·año en el plano (GHI + 2,3 % por transposición)
E_L10 = 4_284_800             # kWh/año


def test_lote10_potencia_y_dcac():
    assert P_L10 == pytest.approx(2701.44)
    assert dc_ac(P_L10, 6 * 330)[0] == pytest.approx(1.364, abs=1e-3)


def test_lote10_produccion_especifica_y_pr():
    assert produccion_especifica(E_L10, P_L10) == pytest.approx(1586, abs=1)
    assert pr_medido(E_L10, P_L10, H_L10) == pytest.approx(0.862, abs=1e-3)


def test_lote10_p90():
    assert p_excedencia(4285, 0.031) == pytest.approx(4115, abs=1)
    # informe PVsyst: 4 068; la forma normal da 4 066,5 (σ redondeado a 3,1 % en el informe) → tolerancia 2 MWh
    assert p_excedencia(4285, 0.031, "P95") == pytest.approx(4068, abs=2)


def test_lote10_energia_ida_y_vuelta():
    pr = pr_medido(E_L10, P_L10, H_L10)
    assert energia_anual(P_L10, H_L10, pr) == pytest.approx(E_L10)


def test_manizales_dcac():
    r, alerta = dc_ac(1000 * 0.620, 5 * 100)
    assert r == pytest.approx(1.24) and "1,2–1,4" in alerta


def test_jinko_590wp():
    assert potencia_modulo(44.17, 13.36) == pytest.approx(590.1, abs=0.1)


def test_strings_a_mano():
    # Voc 49,5 V; β −0,28 %/°C; Tmin 10 °C → 49,5·(1 + 0,0028·15) = 51,579 V; 1500/51,579 = 29,08 → 29
    assert n_serie_max(1500, 49.5, -0.0028, 10) == 29
    # Vmp 41,5 V; β −0,35 %/°C; Tcel 69 °C → 35,11 V; 500/35,11 = 14,24 → 15
    assert n_serie_min(500, 41.5, -0.0035, 69) == 15
    assert strings_por_mppt(40, 13.36) == 2


def test_ventana_no_factible():
    v = ventana_serie(600, 49.5, -0.0028, 10, 550, 41.5, -0.0035, 69)
    assert not v["factible"]


def test_frio_extremo_reduce_la_serie():
    assert n_serie_max(1500, 49.5, -0.0028, -5) < n_serie_max(1500, 49.5, -0.0028, 25)


def test_calculo_puntual_300_kwh_mes():
    kwp = kwp_requerido(300 * 12, 4.8 * 365, 0.78)
    assert kwp == pytest.approx(3600 / (1752 * 0.78))
    assert numero_modulos(kwp, 590) == 5          # 2,634 kWp / 0,59 = 4,46 → 5


def test_sigma_combinada():
    assert sigma_combinada(0.03, 0.04) == pytest.approx(0.05)


def test_inclinacion_colombia_manda_15_grados():
    assert inclinacion_recomendada(5.3) == 15.0
    assert inclinacion_recomendada(-40) == pytest.approx(31.3)


def test_distancia_filas_sol_al_frente():
    assert distancia_entre_filas(1.0, 45) == pytest.approx(1.0)


# ---------- casos borde

def test_pr_mayor_que_uno_es_error():
    with pytest.raises(ValueError):
        pr_medido(5_000_000, P_L10, H_L10)
    with pytest.raises(ValueError):
        energia_anual(10, 1800, 1.2)


def test_dcac_alertas():
    assert "ALERTA FUERTE" in dc_ac(160, 100)[1]
    assert "1,4" in dc_ac(145, 100)[1]
    assert "sobredimensionado" in dc_ac(90, 100)[1]


def test_evaluar_pr():
    assert "deficiente" in evaluar_pr(0.65) and "bueno" in evaluar_pr(0.862)


def test_elevacion_cero():
    with pytest.raises(ValueError):
        distancia_entre_filas(1, 0)


def test_beta_mal_signo_o_unidad():
    from fv_dimensionamiento import v_a_temperatura
    with pytest.raises(ValueError):
        v_a_temperatura(49.5, 0.0028, 10)
    with pytest.raises(ValueError):
        v_a_temperatura(49.5, -0.28, 10)


def test_vmp_tmin_limita_por_mppt():
    from fv_dimensionamiento import ventana_serie
    v = ventana_serie(1500, 49.5, -0.0028, 10, 500, 41.0, -0.0035, 70, v_mppt_max=1000)
    assert v["n_max"] == v["n_max_por_mppt"] < v["n_max_por_voc"]
