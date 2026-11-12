---
fecha_corte: 2026-11
consultado: 2026-11-12
metodo: búsqueda en fuentes oficiales (CREG, MinEnergía, UPME, DIAN, Función Pública, Senado, MinInterior, MinAmbiente, CNO, ISO, IEC, UNFCCC)
---

# Normativa vigente — punto de partida para la Fase 2

**Cómo usar este archivo.** Es una foto con fecha de corte, no la verdad actual. En la Fase 2:
1. Toma solo las filas que aplican al caso.
2. Verifica cada una en la fuente oficial (columna URL o el buscador de la entidad).
3. Si el estado cambió respecto de este archivo, díselo al usuario. Si el cambio mueve la conclusión, detente (⛔).
4. Cita en el entregable la norma con su **fecha de consulta**.

Si no puedes verificar una norma, márcala `[verificar vigencia — corte 2026-11]` y no bases en ella una conclusión
crítica.

**Distinguir siempre:** una resolución **expedida** (rige) de un **proyecto de resolución** (en consulta: no rige).
En el Gestor Normativo de la CREG los proyectos van numerados 701 xxx; las resoluciones definitivas, 101 xxx.

**Columna "Skill":** ER = `proyectos-er` · GE = `gestion-energetica` · MC = `mercado-electrico-co`.

**Dónde verificar:**
- CREG: gestornormativo.creg.gov.co
- Leyes y decretos: funcionpublica.gov.co/eva/gestornormativo y secretariasenado.gov.co
- UPME: docs.upme.gov.co/Normatividad
- DIAN: normograma.dian.gov.co
- MinEnergía (RETIE, RETILAP): minenergia.gov.co → Reglamentos técnicos
- Consulta previa: mininterior.gov.co
- Normas técnicas: iso.org, webstore.iec.ch, icontec.org

## 1. Autogeneración, excedentes y comunidades energéticas

| Norma | Qué establece (lo que usa el método) | Estado al corte | Skill | URL |
|---|---|---|---|---|
| **CREG 174/2021** | AGPE/GD; procedimiento de conexión. ≤ 100 kW con ≤ 50 % de excedentes → sin estudio de conexión (lo valida un ingeniero electricista) | **MODIFICADA**. Los límites 100 kW / 50 % no tienen cambio confirmado `[verificar]` | ER, MC | https://gestornormativo.creg.gov.co |
| **CREG 101 072/2025** (06-abr-2025) | Los excedentes **Exc2** pasan de precio de bolsa a **costo promedio ponderado Mc**. Regula la autogeneración colectiva (AC) y la generación distribuida colectiva (GDC) | VIGENTE | ER, MC | https://gestornormativo.creg.gov.co/gestor/entorno/docs/resolucion_creg_101-72_2025.htm |
| **CREG 101 087/2025** (DO 10-dic-2025) | Sustituye el art. 24 de la 174 (liquidación en el ASIC y el LAC). Mientras se define el traslado a Mcm, se aplica el precio de bolsa (transición). Arts. 6–11 aplicables ≈ desde marzo de 2026 | VIGENTE | ER, MC | https://gestornormativo.creg.gov.co/gestor/entorno/docs/resolucion_creg_101-87_2025.htm |
| **CREG 101 099/2026** (feb-2026) | Autogeneración remota (AGFR) y productor marginal remoto. Extiende de forma transitoria el procedimiento de la 174 a recursos < 5 MW en el SDL | VIGENTE (vigencia del artículo transitorio `[verificar]`) | ER, MC | https://gestornormativo.creg.gov.co/gestor/entorno/docs/resolucion_creg_101-99_2026.htm |
| **Decreto 2236/2023** | Comunidades energéticas: crea la AC y la GDC (Título IX del Decreto 1073/2015) | VIGENTE | ER, MC | https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=227230 |
| UPME 501/2024 | Límites de potencia y dispersión de las comunidades energéticas | VIGENTE `[verificar]` | ER, MC | docs.upme.gov.co |
| Registro de comunidades energéticas (MinEnergía) | Res. 40136/2024 → 40509/2024 → **40332/2026** | VIGENTE la 40332/2026 `[verificar]` | ER, MC | minenergia.gov.co |

**Regla de cálculo:** autoconsumo y excedentes se valoran por separado. El precio de los excedentes es una ENTRADA
del flujo de caja, tomada de la regla vigente y de la oferta del comercializador. Nunca se asume la bolsa ni la tarifa.

## 2. Incentivos tributarios

| Norma | Qué establece | Estado al corte | Skill | URL |
|---|---|---|---|---|
| **Ley 1715/2014**, arts. 11–14 (modificados por la **Ley 2099/2021**) | Deducción en renta del **50 % de la inversión**, con tope del **50 % de la renta líquida**, hasta 15 años `[verificar el plazo]`; exclusión de IVA; exención arancelaria; depreciación acelerada. Cubre FNCE, **gestión eficiente de la energía** e hidrógeno | VIGENTE | ER, GE | https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=57353 · https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=166326 |
| **Decreto 895/2022** | Reglamenta los incentivos de la Ley 2099 | VIGENTE (lo citan normas UPME de 2025–2026) | ER, GE | https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=187366 |
| **Res. UPME 563/2026** (05-ago-2026) | Requisitos, procedimiento y tarifas del **certificado UPME**, requisito previo para el incentivo. **Derogó la 135/2025, la 736/2025, la 468/2022 y la 400/2026** | VIGENTE | ER, GE | https://docs.upme.gov.co/Normatividad/563_2026.pdf |
| Ley 2277/2022 (reforma tributaria) | Posibles topes a los beneficios tributarios | Interacción con la Ley 1715 `[no confirmada]` | ER, GE | — |

**Atención:** el material del curso cita "Ley 1517/2014", que es un error por la 1715. Un concepto DIAN de 2026 todavía
cita la Res. UPME 135/2025, que ya está derogada.

## 3. Reglamentos técnicos e instalaciones

| Norma | Qué establece | Estado al corte | Skill | URL |
|---|---|---|---|---|
| **RETIE**: Res. 40117/2024, modificada por la 40304/2025 y la **40284/2026** (23-jun-2026, libros compilados) | Instalaciones eléctricas, incluidas las FV. La transición terminó el 31-dic-2025 | VIGENTE (versión compilada 2026) | ER, GE | https://www.minenergia.gov.co/documents/15918/Resolucion-40284-23-06-2026-RETIE-libros-compilados.pdf |
| NTC 2050 (2.ª actualización) | Código eléctrico. El RETIE no la hace obligatoria en bloque | Relación con el RETIE 2026 `[verificar]` | ER | icontec.org |
| **RETILAP**: Res. 40150/2024, modificada por la 40318/2025 y la **40286/2026** | Iluminación: niveles de lux y eficacia. La transición de productos terminó el 31-dic-2025 | VIGENTE (compilado 2026) | GE | https://www.minenergia.gov.co/documents/15917/Resoluci%C3%B3n_Modificatoria_RETILAP_2026_Versi%C3%B3n_Final_Numerada_Compilada.pdf |
| NSR-10 | Estructuras (soportes FV en cubierta o suelo) | VIGENTE `[verificar]` | ER | — |
| RETIQ | Etiquetado de eficiencia de equipos | `[verificar]` | GE | minenergia.gov.co |

## 4. Normas técnicas internacionales

| Norma | Uso | Estado al corte | Skill |
|---|---|---|---|
| **IEC 61724-1:2021** | PR y monitoreo FV (2.ª ed.: elimina la clase C y agrega bifaciales) | VIGENTE | ER |
| IEC TS 61724-2:2025 | Evaluación de capacidad FV | publicada | ER |
| **IEC 62446-1:2016+AMD1:2018** | Documentación, puesta en servicio e inspección FV (reemplaza la IEC 62446:2009 que cita el material) | VIGENTE | ER |
| IEC 61400-12-1 | Curva de potencia eólica | `[verificar edición]` | ER |
| ISO 15927-4 | Año meteorológico típico (TMY). El material la cita mal como "15921-5" | `[verificar]` | ER |
| **ISO 50001:2018 + Amd 1:2024** | SGE. La enmienda agrega el cambio climático a las cláusulas 4.1 y 4.2 | VIGENTE | GE |
| **ISO 50002-1:2025** (+ partes 2 edificios y 3 procesos) | Auditorías energéticas. **Reemplaza la ISO 50002:2014** | VIGENTE | GE |
| **ISO 50006:2023** | LBEn e IDEn. Reemplaza la 2014 | VIGENTE | GE |
| ISO 50015:2014 | Medición y verificación (M&V) | VIGENTE (confirmada) | GE |
| ISO 26000 | Responsabilidad social (7 materias) | guía, no certificable | ER |

## 5. Mercado mayorista y tarifa

| Norma | Qué establece | Estado al corte | Skill | URL |
|---|---|---|---|---|
| Leyes 142 y 143/1994 | Servicios públicos; Ley Eléctrica | VIGENTES | MC | funcionpublica.gov.co |
| **CREG 119/2007** + **101 028/2023** | Fórmula del CU. La 101 028 agrega el término **COT** (recuperación del saldo de la opción tarifaria) | VIGENTE y MODIFICADA | MC | https://gestornormativo.creg.gov.co/gestor/entorno/docs/resolucion_creg_0119_2007.htm |
| **CREG 131/1998** (mod. 038/2010 y 186/2010) | Usuario no regulado: > 0,1 MW o ≥ 55 MWh/mes, promedio de 6 meses, un solo sitio. Si vuelve al regulado, permanece 3 años | VIGENTE (concepto CREG de 2025) | MC | https://gestornormativo.creg.gov.co/gestor/entorno/docs/concepto_creg_0014534_2025.htm |
| CREG 024/1995 y 025/1995 | Reglas del MEM y código de operación (despacho) | `[verificar modificaciones]` | MC | gestornormativo.creg.gov.co |
| CREG 071/2006 → 140/2017 → **101 066/2024** → **101 102/2026** | Cargo por confiabilidad. Precio de escasez **inferior** (referencia 359 $/kWh, 2024) y marginal. La 101 102/2026 abre una nueva ventana para acogerse al inferior. Hay un proyecto de precio de escasez superior (701 148/2026) | VIGENTE | MC | https://gestornormativo.creg.gov.co/gestor/entorno/docs/resolucion_creg_101-102_2026.htm |
| CREG 101 079/2025 | Subastas de reconfiguración y de expansión del cargo | `[verificar]` | MC | — |
| Res. MME 40590/2019 + modificaciones | Subastas de FNCER de largo plazo | `[verificar subastas posteriores a 2021]` | MC | minenergia.gov.co |
| **CREG 015/2018**, cap. 12 (mod. 199/2019, 195/2020) | Cobro por transporte de energía reactiva. FP inductivo mínimo de 0,9. Factor M = 1 durante los primeros 12 meses de exceso (> 10 días/mes), luego +1 por mes hasta 6; vuelve a 1 si el exceso desaparece 3 meses. La SSPD cita además la CREG 101 035/2024 | VIGENTE (el alcance de la 101 035/2024 `[no confirmado]`) | GE, MC | https://gestornormativo.creg.gov.co/gestor/entorno/docs/resolucion_creg_0015_2018.htm |
| CREG 243/2016 + acuerdos CNO | ENFICC de plantas solares y series de datos. **El Acuerdo CNO 1937/2025 NO es el protocolo solar: trata de la entrada en operación comercial** | número del acuerdo vigente para las series `[verificar]` (el 1727 es el antecedente) | ER, MC | cno.org.co |

## 6. Eficiencia energética y planeación

| Norma o documento | Qué establece | Estado al corte | Skill | URL |
|---|---|---|---|---|
| **Ley 2407/2024** | URE: **PGEE y gestor energético obligatorios para entidades públicas**; construcciones sostenibles | VIGENTE. **No se encontró un decreto que obligue a los privados a hacer auditorías.** No afirmarlo | GE | http://www.secretariasenado.gov.co/senado/basedoc/arbol/19637.html |
| Ley 697/2001 y PROURE | URE de interés social. **PAI PROURE 2026–2035 en versión preliminar** (jun-2026) | vigente / preliminar | GE | https://docs.upme.gov.co/DemandayEficiencia/Documents/PROURE/PAI_PROURE_version_preliminar_17-06-2026.pdf |
| PEN 2024–2054 (UPME) | Plan Energético Nacional (incluye eliminar el carbón hacia 2050) | publicado; adopción formal `[no confirmada]` | MC | docs.upme.gov.co |
| **PIEG 2025–2039** | Plan indicativo de expansión de la generación (reemplaza el 2023–2037) | vigente como referencia | MC | https://docs.upme.gov.co/SIMEC/Energia%20Electrica/PIEG/2025-2039/Plan_Generacion_2025-2039.pdf |
| **NDC 3.0** (aprobada el 11-dic-2025) | Tope de 169,44 Mt CO₂e en 2030 y de 155–161 Mt CO₂e en 2035. **Reemplaza el "−51 %" de la NDC 2020** | VIGENTE | MC, ER | https://unfccc.int/sites/default/files/2025-12/NDC%203.0%20Transformaciones%20para%20la%20Vida%20(Colombia).pdf |

## 7. Social, ambiental y carbono

| Norma | Qué establece | Estado al corte | Skill | URL |
|---|---|---|---|---|
| **Consulta previa**: Directiva Presidencial 08/2020 (modifica la 10/2013), a cargo de la DANCP (MinInterior) | 5 etapas: procedencia → coordinación → preconsulta → consulta → seguimiento. Sin acuerdos → test de proporcionalidad | VIGENTE | ER | https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=141807 |
| **Impuesto al carbono**: Ley 1819/2016 (mod. Ley 2277/2022) | **Tarifa 2026 = $29 070,49 por t CO₂e** (Res. DIAN 3/2026). Se ajusta cada 1 de febrero con el IPC + 1 hasta llegar a 3 UVT. El carbón paga 50 % en 2026 y 100 % desde 2028. UVT 2026 = $52 374 | VIGENTE. Las condiciones de no causación `[no confirmadas]` | ER, GE | https://normograma.dian.gov.co/dian/compilacion/docs/resolucion_dian_0003_2026.htm |
| MDL → Art. 6.4 del Acuerdo de París | Créditos de carbono internacionales | `[verificar transición]` | ER | unfccc.int |
| PCG del CH₄ | AR5 = 28 (material); AR6 = 27,0 no fósil / 29,8 fósil | declarar cuál se usa | ER | ipcc.ch |
