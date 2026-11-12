# Brechas: lo que estas skills NO saben (o el material cubre mal)

Este archivo es común a las 3 skills. Revisa primero tu sección y luego la transversal.

**Regla.** Cuando el caso toca una brecha, dilo explícitamente ("esto está fuera del alcance verificado de la skill") y
acuerda con el usuario uno de estos tratamientos:
- **PREGUNTAR**: el usuario o el cliente aporta el dato.
- **BUSCAR EN VIVO**: se consulta una fuente oficial con fecha. Nunca se buscan datos del cliente.
- **SUPUESTO ESTÁNDAR**: se usa un método o valor reconocido, declarado en el Registro de Supuestos, con sensibilidad.
- **FUERA DE ALCANCE**: se remite a un especialista o a otra herramienta.

Nunca se rellena una brecha por analogía en silencio.

Estado actualizado con la verificación normativa del 2026-11-12.

## proyectos-er
| ID | Brecha | Tratamiento |
|---|---|---|
| B-ER1 | El curso solo trae el **LCOE no descontado** | SUPUESTO ESTÁNDAR: LCOE descontado = Σ costos_t/(1+i)^t ÷ Σ E_t/(1+i)^t (`evaluacion_financiera.lcoe`) |
| B-ER2 | **FV aislado** (baterías, autonomía, profundidad de descarga, LOLP) sin método | FUERA DE ALCANCE verificado. Perfil con supuestos declarados o remitir a HOMER Pro (lo cita el curso 06). Para el despacho con batería existe `microrred_soc` en `mercado-electrico-co` |
| B-ER3 | Oceánica solo conceptual; geotermia solo con un modelo 0D | Oceánica FUERA DE ALCANCE; geotermia solo a nivel de PERFIL (`recursos_0d.potencia_geotermica`) |
| B-ER4 | **RETIE aplicado a FV** (protecciones, puesta a tierra, certificación) | BUSCAR EN VIVO (RETIE compilado 2026) + remitir a un profesional matriculado |
| B-ER5 | **Trámite de conexión** con el operador de red | BUSCAR EN VIVO (CREG 174/2021 modificada, 101 099/2026) + PREGUNTAR qué respondió el OR |
| B-ER6 | Trámite de incentivos UPME/DIAN | **Parcialmente cerrada:** el trámite lo rige la Res. UPME 563/2026. Los requisitos de detalle se BUSCAN EN VIVO |
| B-ER7 | Errores del Excel del curso: impuesto fijo `$C$27`; "$/kW" que debe ser $/kWh | Corregido en el script, con prueba que documenta la diferencia |
| B-ER8 | Tarifa tomada de una fuente no oficial (GlobalPetrolPrices) | Usar la factura del cliente, el comercializador o el SUI |
| B-ER9 | Imprevistos (13 % → 28 %) sin método | SUPUESTO declarado con rango y sensibilidad |
| B-ER10 | Fórmulas de strings y de sombras que en el material estaban en imagen | SUPUESTO ESTÁNDAR (forma IEC y de fabricante), implementado en `fv_dimensionamiento.py` |
| B-ER11 | η de turbina de biomasa "0,55–0,90" (no es eficiencia del ciclo) | No hay valor por defecto: PREGUNTAR la eficiencia eléctrica neta al fabricante |
| B-ER12 | El ejemplo de PCH de 6 MW no se puede reproducir | No es prueba del script |
| B-ER13 | Citas "ISO 15921-5" (por 15927-4) y "Acuerdo 1042 de 2020" | BUSCAR EN VIVO. **El Acuerdo CNO 1937/2025 no es el protocolo solar** |
| B-ER14 | Degradación, O&M y limpieza sin método de costos | PREGUNTAR o SUPUESTO con sensibilidad (degradación de referencia 0,4–0,5 %/año, declarada) |
| B-ER15 | Impuesto al carbono colombiano | **Parcialmente cerrada:** tarifa 2026 de $29 070,49/t CO₂e. La no causación con certificados se BUSCA EN VIVO |
| B-ER16 | Consulta previa: procedimiento | **Cerrada:** Directiva 08/2020, 5 etapas, a cargo de la DANCP. Los plazos reales se PREGUNTAN o se BUSCAN EN VIVO |

## gestion-energetica
| ID | Brecha | Tratamiento |
|---|---|---|
| B-GE1 | Método de la **línea meta** no formalizado | SUPUESTO ESTÁNDAR: regresión con los periodos bajo la LB y verificación meta ≤ LB (`linea_base.linea_meta`) |
| B-GE2 | **CUSUM** sin fórmula correcta en el material | SUPUESTO ESTÁNDAR Σ(real − modelo) (`linea_base.cusum`) |
| B-GE3 | **M&V** (ISO 50015, IPMVP opciones A–D) sin método | SUPUESTO ESTÁNDAR citado; la ISO 50015:2014 está vigente. Para contratos de desempeño se remite a un profesional certificado en M&V |
| B-GE4 | **Benchmarks** sectoriales sin cifras ni año | PREGUNTAR o BUSCAR EN VIVO; si no hay fuente con año, no se compara |
| B-GE5 | Cobro de energía reactiva | **Parcialmente cerrada:** CREG 015/2018 cap. 12 (FP 0,9; factor M). El límite exacto y la CREG 101 035/2024 se BUSCAN EN VIVO |
| B-GE6 | Reglamentación de la Ley 2407/2024 | **Parcialmente cerrada:** obliga a las entidades públicas (PGEE y gestor). Para privados no se encontró obligación: no afirmarla |
| B-GE7 | Densidad del gas "16,38 kg/m³" en un ejercicio | No usar: PCI y densidad del comercializador. El script rechaza densidades implausibles |
| B-GE8 | Ejercicio de turbina 30 kW × 2 200 h ≠ 100 000 kWh | No se usa como prueba |
| B-GE9 | **Mediciones de campo** (analizador, seguridad eléctrica) | PREGUNTAR. La skill no da instrucciones para intervenir tableros |
| B-GE10 | El cuestionario del curso puntúa N/A = 100 | La plantilla excluye las N/A del promedio |

## mercado-electrico-co
| ID | Brecha | Tratamiento |
|---|---|---|
| B-MC1 | Fórmula vigente del **CU** y valores de sus componentes | **Parcialmente cerrada:** CREG 119/2007 + COT (101 028/2023). Los valores salen de la factura o del comercializador |
| B-MC2 | Criterio oficial de **condición hidrológica** | BUSCAR EN VIVO (XM: aportes como % de la media, embalse agregado; pronóstico ENSO del IDEAM/NOAA). Los umbrales 40/60 % de mi entregable no tienen fuente: no se usan |
| B-MC3 | **Autogeneración y excedentes** | **Parcialmente cerrada:** CREG 174/2021 + 101 072/2025 + 101 087/2025 + 101 099/2026. La liquidación de detalle se BUSCA EN VIVO |
| B-MC4 | Batería sin estado de carga en el ejercicio del curso | Cerrada: `microrred_soc` |
| B-MC5 | Valor de la **energía no suministrada** | PREGUNTAR o BUSCAR EN VIVO (costo de racionamiento UPME); nunca 1 000 $/kWh por defecto |
| B-MC6 | Precios de bolsa, escasez, CERE, OEF e IPC/IPP del material (fotos 2024–2026) | Siempre EN VIVO (XM, CREG, DANE), con fecha |
| B-MC7 | Comunidades energéticas | **Parcialmente cerrada:** Decreto 2236/2023, CREG 101 072/2025 y 101 087/2025, UPME 501/2024 |

## Transversales
| ID | Brecha | Tratamiento |
|---|---|---|
| B-T1 | El material cita la "Ley 1517/2014" | Es la Ley 1715/2014. Cerrada |
| B-T2 | Tarifas, TRM, precios de equipos y de gas del material (2024–2025) | Se piden al cliente o se buscan en vivo con fecha |
| B-T3 | Normas ISO e IEC de pago | Se citan por número y edición. El contenido de detalle se confirma con el texto que tenga el usuario o el cliente |
