"""Pruebas de despacho_economico.py: datos G3, dos nodos, microrred JuMP, taller de subastas (curso 08) y casos borde."""
import os

import pytest

from despacho_economico import (DEMANDA_CURSO, SOLAR_CURSO, Oferta, cierre_energia, contrato_vs_bolsa, costo_mezcla,
                                dos_nodos, leer_demanda, leer_ofertas, margen_reserva, merito, microrred_curso,
                                microrred_soc, precio_bandas, proyeccion, usuario_no_regulado)

DATOS = os.path.join(os.path.dirname(__file__), "datos_prueba")


@pytest.fixture(scope="module")
def g3():
    return leer_ofertas(os.path.join(DATOS, "g3_ofertas.csv")), leer_demanda(os.path.join(DATOS, "g3_demanda.csv"))


# ---------- G3: corrección de la docente

def test_nacional_h23_betania(g3):
    of, dem = g3
    r = merito(of, dem["Nacional"][23], 23, "Nacional")
    assert r.planta_marginal.upper().startswith("BETANIA") and r.precio == pytest.approx(1015)


def test_interior_h0_urra(g3):
    of, dem = g3
    r = merito(of, dem["Interior"][0], 0, "Interior")
    assert r.planta_marginal.upper().startswith("URR") and r.precio == pytest.approx(1020)


def test_nacional_h0_y_costa_h0(g3):
    of, dem = g3
    assert merito(of, dem["Nacional"][0], 0, "Nacional").precio == pytest.approx(1005)
    assert merito(of, dem["Costa"][0], 0, "Costa").precio == pytest.approx(479.476)


def test_despacho_cubre_exactamente_la_demanda(g3):
    of, dem = g3
    r = merito(of, dem["Nacional"][12], 12)
    assert sum(q for _, q in r.despachadas) == pytest.approx(dem["Nacional"][12])
    assert sum(r.por_tipo.values()) == pytest.approx(dem["Nacional"][12])


# ---------- mérito: bordes

def _o(nombre, precio, disp, zona="Z"):
    return Oferta(nombre, zona, precio, "T", [disp] * 24)


def test_deficit():
    r = merito([_o("a", 10, 5)], 8, 0)
    assert r.planta_marginal is None and r.deficit == pytest.approx(3)


def test_empate_reportado():
    r = merito([_o("a", 10, 5), _o("b", 20, 5), _o("c", 20, 5)], 7, 0)
    assert r.precio == 20 and set(r.empatadas) == {"b", "c"}


def test_zona_usa_solo_sus_plantas():
    of = [_o("barata", 1, 100, "Costa"), _o("cara", 50, 100, "Interior")]
    assert merito(of, 10, 0, "Interior").planta_marginal == "cara"
    assert merito(of, 10, 0, "Nacional").planta_marginal == "barata"


def test_disponibilidad_cero_no_marca_precio():
    of = [_o("cero", 1, 0), _o("ok", 5, 10)]
    assert merito(of, 5, 0).planta_marginal == "ok"


def test_hora_invalida():
    with pytest.raises(ValueError):
        merito([_o("a", 1, 1)], 1, 24)


# ---------- dos nodos (MEC p.64–68)

def test_dos_nodos_sin_y_con_congestion():
    libre = dos_nodos(10, 0.01, 500, 13, 0.02, 1500, 10_000)
    assert libre["pi_a"] == pytest.approx(24.333, abs=1e-3) and libre["p_a"] == pytest.approx(1433.33, abs=0.01)
    assert libre["flujo"] == pytest.approx(933.33, abs=0.01) and not libre["congestion"]
    c = dos_nodos(10, 0.01, 500, 13, 0.02, 1500, 400)
    assert c["pi_a"] == pytest.approx(19) and c["pi_b"] == pytest.approx(35) and c["renta"] == pytest.approx(6400)


# ---------- microrred

def test_microrred_reproduce_jump():
    m = microrred_curso()
    assert m["objetivo"] == pytest.approx(307_188.54, abs=0.01)
    assert m["costo_solar"] == pytest.approx(36_740.5)
    assert m["costo_sin_penalidad"] == pytest.approx(225_516.04, abs=0.01)
    assert max(m["no_atendida"]) == pytest.approx(19.6, abs=0.1)


def test_microrred_soc_balances():
    r = microrred_soc(SOLAR_CURSO, DEMANDA_CURSO, c_diesel=344, p_diesel_max=8.56, e_bat_kwh=40, p_bat_kw=10,
                      voll=1000)
    for t in range(24):
        oferta = SOLAR_CURSO[t] + r["diesel"][t] + r["descarga"][t] - r["carga"][t] - r["vertimiento"][t] + r["no_atendida"][t]
        assert oferta == pytest.approx(DEMANDA_CURSO[t], abs=1e-6)
    soc = [0.5 * 40] + r["soc"]
    for t in range(24):
        assert soc[t + 1] == pytest.approx(soc[t] + 0.95 * r["carga"][t] - r["descarga"][t] / 0.95, abs=1e-6)
    assert min(r["soc"]) >= 0.1 * 40 - 1e-9 and r["soc"][-1] >= 20 - 1e-6


def test_bateria_sin_energia_no_entrega():
    # sin sol y con la batería al mínimo y SOC final ≥ inicial: no puede aportar nada neto
    r = microrred_soc([0] * 4, [5] * 4, c_diesel=100, p_diesel_max=0, e_bat_kwh=10, p_bat_kw=5, voll=1000,
                      soc0=0.1, soc_min=0.1)
    assert sum(r["no_atendida"]) == pytest.approx(20)


# ---------- contratos y bolsa (taller de subastas MEC p.30–37)

def test_taller_comercializador():
    e = 500_000
    assert costo_mezcla(e, 1.0, 190, 250) == pytest.approx(95e6)
    assert costo_mezcla(e, 0.6, 190, 250) == pytest.approx(107e6)
    assert costo_mezcla(e, 0.6, 190, 150) == pytest.approx(87e6)


def test_taller_generador_solar():
    # 72 MWh/día: 38 en contrato a 190 y el resto en bolsa
    ingreso = lambda pb: 38_000 * 190 + 34_000 * pb
    assert ingreso(250) == pytest.approx(15.72e6) and ingreso(150) == pytest.approx(12.32e6)
    assert 72_000 * 190 == pytest.approx(13.68e6)


def test_matriz_escenarios():
    m = contrato_vs_bolsa(500_000, [1.0, 0.6], 190, {"nino": 250, "nina": 150})
    assert m[1]["nino"] > m[0]["nino"] and m[1]["nina"] < m[0]["nina"]   # la mejor estrategia depende de la hidrología


def test_bandas():
    assert precio_bandas(300, 150, 250) == 250 and precio_bandas(100, 150, 250) == 150
    assert precio_bandas(200, 150, 250, 5) == 205
    with pytest.raises(ValueError):
        precio_bandas(200, 300, 250)


def test_no_regulado():
    assert usuario_no_regulado([60_000] * 6, [80] * 6)["cumple"]
    assert usuario_no_regulado([40_000] * 6, [150] * 6)["cumple"]
    assert not usuario_no_regulado([40_000] * 6, [80] * 6)["cumple"]
    with pytest.raises(ValueError):
        usuario_no_regulado([1] * 5, [1] * 5)


# ---------- planeamiento y cierre (curso 04)

def test_proyeccion_compuesta():
    p = proyeccion(100, {"medio": 0.024}, 2)
    assert p["medio"] == pytest.approx([100, 102.4, 104.8576])


def test_cierre_lecciones_04():
    assert cierre_energia(1.6e6, 8760, 0.8) == pytest.approx(11.2128e9)
    assert cierre_energia(5.6e6, 8760, 0.16) == pytest.approx(7.849e9, rel=1e-3)


def test_margen_reserva_exige_base():
    assert margen_reserva(20_000, 12_000, "nominal") == pytest.approx(2 / 3)
    with pytest.raises(ValueError):
        margen_reserva(20_000, 12_000, "instalada")


# ---------- validaciones del red team

def test_zona_insensible_a_mayusculas_y_desconocida(g3):
    of, dem = g3
    assert merito(of, dem["Nacional"][23], 23, "nacional").precio == pytest.approx(1015)
    with pytest.raises(ValueError, match="no está en los datos"):
        merito(of, 100, 0, "Orinoquia")
    with pytest.raises(ValueError):
        merito(of, -5, 0)


def test_alerta_precio_escasez(g3):
    of, dem = g3
    r = merito(of, dem["Nacional"][23], 23, precio_escasez=900)
    assert "OEF" in r.alerta


def test_dos_nodos_rechaza_generacion_negativa():
    with pytest.raises(ValueError):
        dos_nodos(10, 0.01, 0, 13, 0.02, 10, 1000)


def test_margen_pico_cero():
    with pytest.raises(ValueError):
        margen_reserva(100, 0, "firme")
