# Método — evaluación financiera de proyectos de energía

**Fuentes:**
- Curso 05: Excel de evaluación y presentación "Evaluación de proyectos" del profesor (N3).
- Curso 01: unidad 3, Economía de la energía (N2).
- Lecciones de mis entregables (N5/N6).

**Script:** `scripts/evaluacion_financiera.py`. Reproduce los ejercicios del curso y corrige sus errores, con pruebas que lo verifican.

## 1. Reglas de decisión (PPT-EV)
- **VPN** > 0 se acepta; = 0 es indiferente; < 0 se rechaza.
- **TIR** = la tasa que hace VPN = 0, y se compara con la tasa de oportunidad del cliente.
  - La TIR no es "la rentabilidad anual del capital": es el interés que ganan los dineros mientras están en el proyecto.
  - Si los flujos cambian de signo más de una vez, puede haber varias TIR. En ese caso se decide con el VPN; el script lo avisa.
- **Payback simple:** años hasta que el acumulado se vuelve ≥ 0. No considera lo que pasa después.
- **Payback descontado:** lo mismo, con flujos descontados.
- **LCOE descontado** = Σ costos_t/(1+i)^t ÷ Σ E_t/(1+i)^t. Es un SUPUESTO estándar (B-ER1); el curso solo trae la versión no descontada.

## 2. Estructura del flujo de caja (hoja Hidro del curso, corregida)
```
Año 0:    − inversión (CAPEX)
Año t:    + energía autoconsumida_t × tarifa evitada_t
          + excedentes_t × precio de excedentes_t     (regla CREG vigente; NUNCA igual a la tarifa por defecto)
          + otros ingresos (garantías, cargo por confiabilidad, carbono si el cliente lo pide)
          − O&M_t (crece con la inflación)  − T&D_t  − reposiciones (inversor, baterías)
          − impuesto_t = tasa × max(0, ingresos − costos − depreciación_t)
Flujo_t = ingresos − costos − reposiciones − impuesto      (la depreciación NO sale de caja)
```
- La **energía** se degrada de forma compuesta: E_t = E_1·(1 − d)^(t−1).
- El **impuesto se calcula año a año**. El Excel del curso usa la renta del año 1 en todos los años (B-ER7); el script lo
  reproduce solo para la prueba y documenta la diferencia.
- Unidad del precio: **$/kWh**. El Excel del curso dice "$/kW", lo cual es un error.
- **Esquema de financiación** explícito: quién pone el CAPEX, quién recibe el ahorro, quién opera. Lección del curso 01: un
  proyecto comunitario quedó con costos por familia y un payback afirmado sin cálculo.

## 3. Incentivos (Ley 1715/2014 mod. Ley 2099/2021; ver `normativa-vigente.md`)
- **Deducción en renta del 50 % de la inversión**, con tope del 50 % de la renta líquida del contribuyente. Depende de la
  renta del **cliente**, no del proyecto, así que va como **escenario aparte** con su supuesto declarado.
- **Exclusión de IVA y exención arancelaria**: reducen el CAPEX de los bienes certificados.
- **Depreciación acelerada.**
- Todo exige el **certificado UPME (Res. 563/2026)** antes de aplicar. Si no está, el escenario base va sin incentivos.

## 4. Sensibilidad (obligatoria)
- Se hace un **tornado** sobre 3 a 5 variables críticas: tarifa, energía (recurso y PR), CAPEX, precio de excedentes, tasa y
  O&M. Por defecto se usa ±20 %, o el rango del Registro de Supuestos.
- Se calcula el **punto de equilibrio** de la variable más incierta, por ejemplo "con una tarifa por debajo de X $/kWh el
  proyecto deja de ser viable".
- **En el resumen ejecutivo:** "de 10 escenarios razonables de tarifa y producción, en 8 el proyecto se paga antes del año 7".

## 5. Costos y supuestos típicos que se declaran (nunca se toman del curso como vigentes)
- **CAPEX y O&M**: cotización del cliente, o Catálogo Tecnológico de la UPME vigente (consultarlo en vivo).
  - A3.2 usó 1 000 USD/kW FV y 1 677 USD/kW eólica (Catálogo UPME 2025), con O&M de 20/35 USD/kW-año. Son solo referencia.
- **Imprevistos**: se declaran con rango (B-ER9). Mi entregable pasó de 13 % a 28 % sin justificarlo.
- **Degradación FV**: 0,4–0,5 %/año. El Lote 10 usó 0,4 %. Se confirma con la garantía del fabricante.
- **Reposición del inversor**: se pide la vida útil al fabricante. En el ejercicio del curso fue en los años 10 y 20.
- **Tarifa**: la factura del cliente o el comercializador (SUI). **Nunca** una web no oficial (B-ER8).
  - Si solo hay $/mes, se pide la tarifa o se usa un rango del SUI con fecha, marcado SUPUESTO.
  - **Estratos 1 a 3:** el kWh ahorrado dentro del consumo de subsistencia vale la tarifa subsidiada. Por encima, la plena.
    Estrato 4 y no residenciales: tarifa plena; estratos 5, 6 y comercial pagan contribución. `[verificar vigencia]`
- **Excedentes Exc1 y Exc2** (CREG 174/2021 y modificaciones `[verificar vigencia]`): Exc1 = exportación hasta lo
  importado en el periodo (se reconoce por permuta o crédito, cercano a la tarifa menos comercialización); Exc2 = lo que
  supera la importación (valorado a Mc o a bolsa según la regla vigente). En el script: `energia_exc1_kwh`/`precio_exc1`
  y `energia_excedente_kwh`/`precio_excedente`. El precio de Exc2 **no** sigue a la tarifa (`escalamiento_excedente` propio).
- **Incentivos Ley 1715** como escenario aparte: el ahorro de impuesto por año lo calcula el contador (deducción ≤ 50 %
  de la renta líquida, depreciación acelerada) y entra en `beneficios_tributarios={año: monto}`. Nunca de memoria.
- **El CLI exige `--tasa` y `--anos`** (salen del Registro de Supuestos) e imprime todos los supuestos usados.
- **Payback**: cuenta el último cruce a positivo (una reposición tardía puede volver negativo el acumulado).
- **Reposiciones**: se tratan como gasto deducible del año (SUPUESTO simplificado; el contador puede capitalizarlas).
- **Autoconsumo vs. excedentes**: se separan siempre. La fracción autoconsumida se declara (perfil de uso) y el excedente
  se valora con la regla CREG vigente, consultada en vivo.
- **"¿Cuánto puede costar?"**: `capex_max_para_payback` (CLI `--payback-objetivo`) da el CAPEX máximo que cumple el plazo del cliente.
  No es un precio de mercado: se compara contra cotizaciones.

## 6. Casos de prueba (todos pasan en `test_evaluacion_financiera.py`)
| Caso del curso | Resultado |
|---|---|
| VPN de la hoja VPN (i = 35 %) | 527,998 |
| TIR de la hoja TIR (200; −80; −100; −120) | 21,6478 % |
| FV 5 kW (21,5 M; 7 000 kWh × 600; O&M 0,5 M; inversor 3 M en los años 10 y 20; 12 %) | VPN 4 860 021; TIR 15,638 %; payback de 5,8 años |
| Hidro 1,2 MW con el error del curso | VPN 10 259 539 186; TIR 35,36 %. Corregido, el VPN es menor |

**Lección del curso 05 (Act 6).** Recalculado con sus propios supuestos, mi VPN daba 874 M y no los 962 M
reportados. La TIR daba 13,44 % y no 13,8 %. Por eso el VPN siempre sale del script.

## 7. Ingresos por carbono (solo si el cliente los pide)
- Van como escenario aparte, con los costos de validación y verificación.
- **Referencias:**
  - impuesto al carbono colombiano 2026: $29 070,49 por t CO₂e (Res. DIAN 3/2026);
  - mercado voluntario y Art. 6.4: `[buscar en vivo]`.
- **Factor de emisión:** se declara con su fuente (factor del SIN publicado por la UPME, consultado en vivo).
