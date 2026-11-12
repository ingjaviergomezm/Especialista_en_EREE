# Verificación de alta fiabilidad: skills v0.9 (2026-11-12)

## 1. Pruebas automáticas
| Skill | Pruebas | Resultado |
|---|---|---|
| proyectos-er | 63 | todas pasan |
| gestion-energetica | 61 | todas pasan |
| mercado-electrico-co | 25 | todas pasan |

- Siguen reproduciéndose exactamente los ejercicios de los profesores: Excel de VPN, TIR, FV e Hidro; Lote 10 en PVsyst; G3; microrred de 307 188,54.
- Hay 27 pruebas nuevas, una por cada corrección de esta ronda.

## 2. Trazabilidad
- Todas las rutas que cita cada SKILL.md existen, y todo script está citado en su SKILL.md.
- `normativa-vigente.md` tiene `fecha_corte: 2026-11` en las tres skills.
- Las cifras del curso sin fuente primaria quedaron marcadas SUPUESTO:
  - USE por sector;
  - penalidad de PR en un EPC;
  - factores ENFICC y de energía ofertable.

## 3. Disparadores
Ver `verificacion_disparadores.md`.
- Las 10 peticiones de prueba llegan a la skill correcta.
- Hubo que acortar las tres `description` para que entren en el límite de 1 024 caracteres de claude.ai.
- Se agregó una regla común de traspaso:
  - reducir consumo → gestion-energetica;
  - precio, tarifa o contrato → mercado-electrico-co;
  - generación nueva → proyectos-er.

## 4. Simulación con el humano en el ciclo (subagente)
**Casos:**
- A: FV para una vivienda en Tauramena, con un usuario apurado y sin facturas.
- B: planta de lácteos en Boyacá con 8 meses de datos.

**Resultado:** las dos skills entrevistaron en bloques de 4 o 5 preguntas, se detuvieron en la Ficha y no inventaron en silencio.

**Fallas que encontró, todas corregidas:**
| # | Falla | Corrección |
|---|---|---|
| 1 | `evaluacion_financiera.py --help` fallaba por un `%` | Corregido, con prueba |
| 2 | No sabía qué hacer si el usuario daba $/mes y no kWh, ni con estrato y subsidio | Regla en el modo rápido, en `metodo-financiero.md` y en la entrevista |
| 3 | "¿Cuánto vale?" obligaba a inventar un CAPEX | Nueva función `capex_max_para_payback` (CLI `--payback-objetivo`): da el CAPEX máximo que cumple el plazo del cliente |
| 4 | Modo rápido sin límite | Nunca recomienda comprar; si el usuario pregunta "¿compro?" → Fase 0 |
| 5 | HSP horizontal vs. en el plano | Nota en `metodo-fv.md` y en el modo rápido |
| 6 | Todo se valoraba como autoconsumo | Fracción autoconsumida declarada; excedentes con la regla CREG |
| 7 | Prueba de cierre circular | Se contrasta con el PVOUT independiente del atlas |
| 8 | Línea meta calculada con menos de 12 meses | Bloqueada (LBEn PROVISIONAL); además exige ≥ 6 periodos bajo la LB |
| 9 | Periodos de energía y producción que no coinciden | Regla en `metodo-linea-base.md`; el balance se rotula "kWh del periodo" |
| 10 | El balance mostraba porcentajes aunque no cerrara | Ya no los muestra (código 2); `--forzar` solo para uso interno |
| 11 | LBEn por energético o total | Una por energético, más una total si sirve |
| 12 | La entrevista solo preguntaba por gas natural | Agregados GLP, diésel y carbón: unidad de compra y PCI |

## 5. Red team (subagente revisor independiente)
| Severidad | Hallazgo | Corrección |
|---|---|---|
| ALTO | Exc1 y Exc2 tenían un solo precio | `energia_exc1_kwh`/`precio_exc1` separados de Exc2; el precio de Exc2 escala aparte, no sigue al CU |
| ALTO | "Precio por zona", que en Colombia no existe | Rotulado como didáctico, con la explicación de bolsa única nacional, el adicional sobre el marginal y que la congestión va al componente R; `precio_escasez` con alerta de OEF; el nodal también rotulado como didáctico |
| ALTO | Línea base sin filtro de calidad | Advertencia si R² < 0,75 (SUPUESTO) o si la pendiente es ≤ 0, sin línea meta; el CLI marca los meses que extrapolan |
| ALTO | Reactiva calculada con totales mensuales | `reactiva_en_exceso_horaria` hora a hora, con la capacitiva; advertencia si el FP objetivo es > 0,98 |
| ALTO | Valores por defecto ocultos (tasa 12 %, 25 años, PR 0,78) | `--tasa` y `--anos` obligatorios; el CLI imprime todos los supuestos; un PR por defecto se marca como "SUPUESTO NO APROBADO" |
| ALTO | Formas de saltarse las compuertas | Sello "PERFIL — no apto para decidir" y el mismo mínimo innegociable en las tres skills: Ficha + supuestos críticos + normas con su vigencia |
| MEDIO | Payback contaba el primer cruce | Ahora cuenta el último; reposiciones deducibles; nota cuando la TIR queda fuera de rango; `beneficios_tributarios` para la Ley 1715 |
| MEDIO | Strings FV | Valida el signo y la unidad de β; Vmp(Tmin) frente al máximo del MPPT; Isc en el CLI |
| MEDIO | Densidad del aire ISA | Opción p/(R·T) con presión y temperatura del sitio; altitud validada |
| MEDIO | Despacho sin validaciones | Demanda negativa, zona inexistente o en otra capitalización, generación negativa en dos nodos, pico 0 |
| MEDIO | Cifras sin fuente | Marcadas SUPUESTO |
| MEDIO | Regulación dudosa | "Auditoría tipo 1/2/3" → ASHRAE I–III; PCH técnica frente a plantas menores < 20 MW (regulatoria); factor M, permanencia de 3 años y medición ENFICC marcados `[verificar en vivo]`; mínimo técnico como fracción de Q_d |
| MEDIO | Informe para la gerencia | Se agregaron la decisión solicitada con su umbral, la precisión del CAPEX por nivel, el costo de no actuar, el cronograma y los desembolsos, la financiación, la matriz de riesgos y el plan de M&V |
| BAJO | Casos borde | Validaciones en balance, `ahorro_pct`, P90, distancia entre filas, geotermia, pesos negativos, `priorizar` (ya no se cae entera) y `numpy.int64` |
| BAJO | Mantenimiento | "FP × 8 760" aclarado como factor de utilización; docstring `gas_kwh` corregido; prueba de que las dos copias de `evaluacion_financiera.py` siguen idénticas |
| — | Pague lo contratado | Limitación documentada: el riesgo de volumen se calcula como escenario aparte |

## 6. Queda abierto para el piloto (v1.0)
- Verificar en vivo los puntos marcados `[verificar]`:
  - factor M y CREG 101 035/2024;
  - permanencia del usuario no regulado;
  - umbral de plantas menores;
  - protocolo CNO de medición para la ENFICC.
- La simulación usó un usuario inventado. El piloto con un caso real de Javier es lo que da la v1.0.
