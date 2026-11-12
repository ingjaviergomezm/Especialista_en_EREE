"""Pruebas de balance_energetico.py y medidas_ahorro.py (curso 03, cálculos a mano, casos borde)."""
import pytest

from balance_energetico import (EJEMPLO, Equipo, balance, combustible_a_kwh, flujos_sankey, gas_a_kwh,
                                usos_significativos)
from medidas_ahorro import (Medida, ahorro_cogeneracion, ahorro_fugas, ahorro_iluminacion, ahorro_motor,
                            ahorro_reduccion_presion, compensacion_kvar, factor_potencia, priorizar, reactiva_en_exceso)


# ---------------------------------------------------------------- balance

def _eqs():
    return [Equipo("a", "x", "electricidad", 10, 10, 100), Equipo("b", "y", "gas", 20, 5, 100, 0.5),
            Equipo("c", "y", "electricidad", 1, 10, 100)]


def test_balance_cierra_y_suma():
    r = balance(_eqs(), {"electricidad": 11_000, "gas": 5_000})
    assert r["total_kwh"] == pytest.approx(16_000) and r["cierra"]
    assert sum(r["pct_energia_equipo"].values()) == pytest.approx(1)


def test_balance_no_cierra():
    r = balance(_eqs(), {"electricidad": 20_000, "gas": 5_000})
    assert not r["cierra"] and not r["cierre"]["electricidad"]["cierra"]


def test_energetico_sin_factura_no_cierra():
    assert not balance(_eqs(), {"electricidad": 11_000})["cierra"]


def test_energia_y_costo_separados():
    # leccion GE Act 2: el gas puede ser mayoría en energía y minoría en costo
    r = balance(_eqs(), {"electricidad": 11_000, "gas": 5_000}, {"electricidad": 1000, "gas": 100})
    assert r["pct_energia_equipo"]["b"] == pytest.approx(5000 / 16000)
    assert r["pct_costo_equipo"]["b"] == pytest.approx(500_000 / 11_500_000)


def test_sankey_suma_igual_que_balance():
    flujos = flujos_sankey(EJEMPLO)
    total = sum(e.kwh_ano for e in EJEMPLO)
    primer_nivel = sum(v for o, d, v in flujos if o in {"gas", "electricidad"})
    assert primer_nivel == pytest.approx(total)


def test_use_pareto():
    use = usos_significativos({"a": 50, "b": 30, "c": 15, "d": 5})
    assert [u["equipo"] for u in use if u["use"]] == ["a", "b"]  # a=50 %, b lleva a 80 % → c ya no
    use2 = usos_significativos({"a": 50, "b": 30, "c": 15, "d": 5}, adicionales=["d"])
    assert [u["equipo"] for u in use2 if u["use"]] == ["a", "b", "d"]


def test_gas_conversion():
    assert gas_a_kwh(1000, pci_mj_m3=36) == pytest.approx(10_000)
    assert gas_a_kwh(1000, pci_mj_kg=48.88164, densidad_kg_m3=0.75) == pytest.approx(1000 * 0.75 * 48.88164 / 3.6)
    with pytest.raises(ValueError, match="implausible"):
        gas_a_kwh(1000, pci_mj_kg=48.88164, densidad_kg_m3=16.38)   # dato sospechoso del ejercicio C1
    assert combustible_a_kwh(10, 36) == pytest.approx(100)


def test_equipo_imposible():
    with pytest.raises(ValueError):
        balance([Equipo("x", "a", "e", 1, 30, 1)], {"e": 1})
    with pytest.raises(ValueError):
        balance([Equipo("x", "a", "e", 1, 1, 1, 1.5)], {"e": 1})


# ---------------------------------------------------------------- medidas

def test_iluminacion_curso_u3():
    assert ahorro_iluminacion(100, 80, 35, 3000) == pytest.approx(13_500)
    assert ahorro_iluminacion(100, 80, 35, 3000) * 0.15 == pytest.approx(2025)
    assert ahorro_iluminacion(100, 80, 35, 3000, 0.20) == pytest.approx(15_600)


def test_fp_y_compensacion():
    assert factor_potencia(100, 125) == pytest.approx(0.8)
    assert factor_potencia(80, kvar=60) == pytest.approx(0.8)
    assert compensacion_kvar(100, 0.8, 0.95) == pytest.approx(100 * (0.75 - 0.328684), abs=0.01)


def test_reactiva_exceso():
    assert reactiva_en_exceso(1000, 600) == pytest.approx(100)
    assert reactiva_en_exceso(1000, 400) == 0


def test_motor_a_mano():
    assert ahorro_motor(15, 6000, 0.75, 0.88, 0.93) == pytest.approx(67500 * (1 / 0.88 - 1 / 0.93))


def test_aire_y_chp():
    assert ahorro_fugas(75, 0.30, 4000) == pytest.approx(90_000)
    assert ahorro_reduccion_presion(100_000, 1) == pytest.approx(7_000)
    assert ahorro_cogeneracion(1000, 0.56, 0.80) == pytest.approx(1000 / 0.56 - 1000 / 0.80)


def test_payback_auditoria_u2_via_medida():
    d = Medida("x", 50_000, 1.0, 120_000, 10).evaluar()
    assert d["payback"] == pytest.approx(2.4)


def test_priorizar_por_vpn():
    # grande: 10 000/año × 5,6502 (anualidad 12 %, 10 años) = 56 502 < 70 000 → VPN negativo
    r = priorizar([Medida("chica", 1000, 1, 500, 10), Medida("grande", 10_000, 1, 70_000, 10)])
    assert r[0]["medida"] == "chica" and r[1]["vpn"] < 0


# ---------- bordes

def test_bordes_medidas():
    with pytest.raises(ValueError):
        ahorro_iluminacion(10, 35, 80, 1000)
    with pytest.raises(ValueError):
        ahorro_motor(10, 1000, 1, 0.95, 0.90)
    with pytest.raises(ValueError):
        compensacion_kvar(100, 0.95, 0.9)
    with pytest.raises(ValueError):
        factor_potencia(100, 90)


def test_cli_balance_no_cierra_oculta_porcentajes(tmp_path, capsys):
    import balance_energetico as be
    csvf = tmp_path / "eq.csv"
    csvf.write_text("equipo,area,energetico,kw,horas_dia,dias_ano,factor_carga\nmotor,planta,electricidad,10,8,300,0.8\n",
                    encoding="utf-8")
    rc = be.main(["--equipos", str(csvf), "--factura", "electricidad=100000"])
    out = capsys.readouterr().out
    assert rc == 2 and "NO CIERRA" in out and "% energía" not in out


def test_reactiva_horaria_no_se_diluye():
    from medidas_ahorro import reactiva_en_exceso_horaria
    r = reactiva_en_exceso_horaria([100, 100], [100, 0], [0, 10])
    assert r["exceso_inductivo_kvarh"] == pytest.approx(50)
    assert r["exceso_si_se_usara_total_mensual"] == pytest.approx(0)
    assert r["capacitiva_kvarh"] == 10 and r["horas_con_capacitiva"] == 1


def test_fp_objetivo_unitario_advierte():
    from medidas_ahorro import compensacion_kvar
    with pytest.warns(UserWarning, match="CAPACITIVA"):
        compensacion_kvar(100, 0.8, 1.0)
