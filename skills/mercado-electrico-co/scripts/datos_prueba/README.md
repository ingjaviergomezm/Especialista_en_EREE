# Datos de prueba

| Archivo | Qué es | Origen |
|---|---|---|
| `g3_ofertas.csv` | 80 plantas con zona, precio de oferta, tipo y disponibilidad horaria (h0–h23) | Ejercicio académico G3 del curso *Mercados y Regulación* de la Especialización EVEREE, Universidad Autónoma de Manizales |
| `g3_demanda.csv` | Demanda horaria Nacional, Interior y Costa del mismo ejercicio | Ídem |

**Uso exclusivo:** pruebas de regresión. `test_despacho_economico.py` verifica que `merito()` reproduce exactamente la corrección de la docente; por ejemplo, Nacional H23 → Betania a 1 015 $/kWh.

**No son datos vigentes del mercado colombiano.** Para un análisis real, el precio de bolsa, la disponibilidad y la demanda se descargan de XM (Sinergox / SIMEM) con la fecha de corte.

Las series `PRECIOS_HIDRO` (en `test_evaluacion_financiera.py`) y `SOLAR_CURSO`/`DEMANDA_CURSO` (en `despacho_economico.py`) tienen el mismo origen académico y el mismo uso.

**Licencia:** estos datos no son obra del autor del repositorio y quedan **excluidos** de la licencia del proyecto.
