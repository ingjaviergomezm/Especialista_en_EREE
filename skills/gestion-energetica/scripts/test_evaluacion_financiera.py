"""Pruebas de evaluacion_financiera.py: ejercicios del curso 05 (N3), cálculos a mano y casos borde.

Correr:  python -m pytest -q  (desde la carpeta scripts/)
"""
import math

import pytest

from evaluacion_financiera import (Proyecto, cierre_energia, factor_planta_implicito, flujo_caja, lcoe, payback,
                                   payback_simple, punto_equilibrio, tir, tornado, verificar_cierre, vpn)

PRECIOS_HIDRO = [235.06959106677417, 239.93208478927312, 245.95221297615623, 263.8159448395255, 278.041209553019,
                 292.45646926233564, 321.4472140035999, 326.11619912079, 345.4894791021281, 362.4180450954469,
                 384.43554259362145, 391.5027803760796, 420.95219837291637, 440.4583531527697, 475.8414057352829,
                 497.4082818417189, 536.3360141803051, 578.4561374789371, 619.5480900967615, 633.9536302781819,
                 646.5869526010833, 705.6075465412328, 715.6092817109177, 724.0151765121867, 732.1810115082915]


# ---------- ejercicios del curso (Excel del profesor, hojas VPN, TIR, Fotovoltaica, Hidro)

def test_vpn_hoja_vpn():
    assert vpn([-6500, 2000, 2300, 2700, 3000, 4200, 4600, 4800], 0.35) == pytest.approx(527.998, abs=1e-3)


def test_tir_hoja_tir_flujo_invertido():
    assert tir([200, -80, -100, -120]) == pytest.approx(0.216478, abs=1e-6)


def test_fv_5kw_curso():
    p = Proyecto(capex=21_500_000, anos=20, tasa=0.12, energia_autoconsumo_kwh=7000, tarifa=600, om_anual=500_000,
                 reposiciones={10: 3_000_000, 20: 3_000_000})
    r = flujo_caja(p)
    assert r["vpn"] == pytest.approx(4_860_021.405, abs=1)
    assert r["tir"] == pytest.approx(0.15638312637504526, abs=1e-8)
    assert 5 < r["payback"] < 6  # el acumulado se vuelve positivo en el año 6


def test_hidro_reproduce_error_del_curso_y_lo_corrige():
    base = dict(capex=2_950_000 * 1200, anos=25, tasa=0.12, energia_autoconsumo_kwh=1200 * 6500, tarifa=PRECIOS_HIDRO,
                om_pct_capex=0.08, inflacion_costos=0.04, otros_costos_kwh=15, otros_ingresos_kwh=10,
                tasa_impuesto=0.35)
    curso = flujo_caja(Proyecto(**base, impuesto_fijo_ano1=True))
    assert curso["vpn"] == pytest.approx(10_259_539_186.096, rel=1e-9)
    assert curso["tir"] == pytest.approx(0.3536214932382511, abs=1e-8)
    corregido = flujo_caja(Proyecto(**base))
    # con el impuesto año a año el VPN baja: la renta crece con el precio y el curso la congeló en el año 1
    assert corregido["vpn"] < curso["vpn"]
    assert corregido["vpn"] == pytest.approx(vpn(corregido["flujos"], 0.12))


# ---------- propiedades y cálculos a mano

def test_vpn_en_la_tir_es_cero():
    flujos = [-1000, 300, 400, 500, 200]
    assert vpn(flujos, tir(flujos)) == pytest.approx(0, abs=1e-6)


def test_payback_simple_auditoria_u2():
    assert payback_simple(120_000, 50_000) == pytest.approx(2.4)


def test_payback_interpolado():
    assert payback([-100, 40, 40, 40]) == pytest.approx(2.5)


def test_lcoe_descontado_a_mano():
    # 1000 de inversión, 100/año de O&M, 1000 kWh/año, 2 años, 10 %
    costos, energia = [1000, 100, 100], [0, 1000, 1000]
    num = 1000 + 100 / 1.1 + 100 / 1.21
    den = 1000 / 1.1 + 1000 / 1.21
    assert lcoe(costos, energia, 0.10) == pytest.approx(num / den)


def test_excedentes_se_valoran_aparte():
    p = Proyecto(capex=0, anos=1, tasa=0.1, energia_autoconsumo_kwh=1000, tarifa=800,
                 energia_excedente_kwh=500, precio_excedente=300)
    f = flujo_caja(p)["filas"][1]
    assert f["ingreso_autoconsumo"] == 800_000 and f["ingreso_excedentes"] == 150_000


def test_degradacion_compuesta():
    p = Proyecto(capex=1, anos=3, tasa=0.1, energia_autoconsumo_kwh=1000, tarifa=1, degradacion=0.005)
    e = [f["energia_kwh"] for f in flujo_caja(p)["filas"][1:]]
    assert e == pytest.approx([1000, 995, 990.025])


# ---------- prueba de cierre (lecciones L2/L3 del curso 04)

def test_cierre_carbon_1_6_gw():
    assert cierre_energia(1.6e6, 8760, 0.8) / 1e9 == pytest.approx(11.2128)  # TWh, no 1,6


def test_cierre_fncer_5_6_gw():
    assert cierre_energia(5.6e6, 8760, 0.16) / 1e9 == pytest.approx(7.849, abs=1e-3)  # no 17 TWh


def test_verificar_cierre_detecta_cifra_imposible():
    r = verificar_cierre(17e9, 5.6e6, 0.14, 0.18)
    assert not r["cierra"] and factor_planta_implicito(17e9, 5.6e6) == pytest.approx(0.3466, abs=1e-3)


# ---------- casos borde

def test_tir_no_existe_sin_cambio_de_signo():
    assert tir([100, 200, 300]) is None and tir([-100, -1]) is None


def test_tir_multiple_lanza_error():
    with pytest.raises(ValueError):
        tir([-100, 230, -132])  # raíces en 10 % y 20 %


def test_payback_no_se_recupera():
    assert payback([-1000, 10, 10]) is None


def test_payback_simple_ahorro_cero():
    with pytest.raises(ValueError):
        payback_simple(100, 0)


def test_factor_planta_fuera_de_rango():
    with pytest.raises(ValueError):
        cierre_energia(100, 8760, 1.2)


def test_serie_de_largo_incorrecto():
    with pytest.raises(ValueError):
        flujo_caja(Proyecto(capex=1, anos=3, tasa=0.1, energia_autoconsumo_kwh=1, tarifa=[1, 2]))


def test_tornado_ordena_por_amplitud_y_equilibrio():
    p = Proyecto(capex=21_500_000, anos=20, tasa=0.12, energia_autoconsumo_kwh=7000, tarifa=600, om_anual=500_000)
    t = tornado(p, {"tarifa": (0.8, 1.2), "om_anual": (0.8, 1.2)})
    assert t[0]["variable"] == "tarifa"
    tarifa_min = punto_equilibrio(p, "tarifa", 1, 2000)
    assert flujo_caja(Proyecto(**{**p.__dict__, "tarifa": tarifa_min}))["vpn"] == pytest.approx(0, abs=1)


def test_capex_max_para_payback():
    from evaluacion_financiera import capex_max_para_payback
    p = Proyecto(capex=10_000, anos=20, tasa=0.1, energia_autoconsumo_kwh=1000, tarifa=1)  # 1 000 $/año
    assert capex_max_para_payback(p, 5) == pytest.approx(5000, rel=1e-6)


def test_cli_help_no_falla(capsys):
    import evaluacion_financiera as ef
    with pytest.raises(SystemExit) as e:
        ef.main(["--help"])
    assert e.value.code == 0


def test_payback_cuenta_el_ultimo_cruce():
    assert payback([-100, 60, 60, -200, 100, 100, 100]) == pytest.approx(4.8)
    assert payback([-100, 60, 60, -200]) is None


def test_exc1_exc2_y_escalamiento_separado():
    import numpy as np
    p = Proyecto(capex=1000, anos=10, tasa=0.1, tarifa=np.int64(1), escalamiento_tarifa=0.1,
                 energia_exc1_kwh=100, precio_exc1=0.8, energia_excedente_kwh=100, precio_excedente=0.5)
    f = flujo_caja(p)["filas"]
    assert f[1]["ingreso_excedentes"] == pytest.approx(100 * 0.8 + 100 * 0.5)
    assert f[10]["ingreso_excedentes"] == pytest.approx(100 * 0.8 * 1.1 ** 9 + 100 * 0.5)  # Exc2 no sigue al CU


def test_tir_fuera_de_rango_tiene_nota():
    r = flujo_caja(Proyecto(capex=1, anos=5, tasa=0.1, energia_autoconsumo_kwh=1000, tarifa=1))
    assert r["tir"] is None and "fuera del rango" in r["nota_tir"]


def test_cli_exige_tasa_y_horizonte():
    import evaluacion_financiera as ef
    with pytest.raises(SystemExit):
        ef.main(["--capex", "1000", "--energia", "100", "--tarifa", "1"])


def test_copia_identica_a_proyectos_er():
    """evaluacion_financiera.py está duplicado en dos skills: si existe la otra copia, deben ser idénticas."""
    import os
    aqui = os.path.dirname(os.path.abspath(__file__))
    otra = os.path.join(aqui, "..", "..", "proyectos-er" if "gestion" in aqui else "gestion-energetica",
                        "scripts", "evaluacion_financiera.py")
    if not os.path.exists(otra):
        pytest.skip("la otra skill no está instalada al lado")
    assert open(os.path.join(aqui, "evaluacion_financiera.py"), "rb").read() == open(otra, "rb").read()
