# Informe técnico — plantillas y lista de chequeo (común a las 3 skills)

Este archivo contiene:
- el **Registro de Supuestos**;
- la **estructura de cada hallazgo**;
- la **estructura del informe**;
- la **tabla de trazabilidad**;
- la **lista de chequeo** de calidad.

La lista de chequeo traduce a criterio profesional los errores que costaron puntos en la especialización (P1–P12): son
los mismos errores que hacen que una gerencia no pueda decidir con un informe.

La Ficha de Encargo está al final de `entrevista.md`.

---

## 1. Registro de Supuestos (Fase 1 ⛔)

```
REGISTRO DE SUPUESTOS — <proyecto>          Versión: N    Fecha: AAAA-MM-DD    Estado: borrador | aprobado
| # | Variable | Valor | Unidad | Origen | Fuente y fecha | Rango para sensibilidad | Crítico | Estado |
|---|----------|-------|--------|--------|----------------|-------------------------|---------|--------|
| S1 | Consumo anual | 42 300 | kWh/año | factura | 12 facturas ene–dic 2025 del cliente | ±5 % | sí | confirmado |
| S2 | Irradiación en el plano | 4,9 | kWh/m²·día | atlas | Global Solar Atlas, consulta 2026-11-12 | 4,6–5,2 | sí | supuesto aprobado |
| S3 | PR | 0,78 | – | supuesto | curso 06 (rango 0,70–0,85) | 0,72–0,82 | sí | supuesto aprobado |
| S4 | Precio de excedentes | — | $/kWh | por confirmar | regla CREG vigente + oferta del comercializador | — | sí | [POR CONFIRMAR] |
```

**Origen** puede ser: medido · factura · ficha técnica · atlas/base oficial · norma · supuesto.

**Reglas:**
- Un solo valor por variable en todo el informe (lección: dos tasas de crecimiento distintas en un mismo entregable).
- Lo **crítico** es lo que mueve la decisión. Va al tornado de sensibilidad.
- Ningún dato "supuesto" crítico pasa a la Fase 3 sin el "aprobado" del usuario.
- Precios, tarifas y TRM siempre con mes y año. Los datos del material del curso (2024–2025) no son vigentes.

## 2. Estructura de cada hallazgo (Fase 4 ⛔): exigida por el usuario

```
HALLAZGO H<n> — <título corto>                                  Prioridad: alta | media | baja
1. Qué se revisó:   <sistema, equipo, contrato, norma, dato>
2. Cómo se hizo:    <método: script X con datos Y; inspección; comparación con la norma Z (consultada AAAA-MM-DD)>
3. Hallazgo:        <qué se encontró, con cifra y unidad>
4. Riesgo o impacto: <consecuencia en kWh/año, $/año, plazo, cumplimiento o seguridad; en lenguaje llano>
5. Recomendación y procedimiento sugerido:
   a. <paso>  — responsable: <rol>  — plazo: <semanas o meses, con cifra>
   b. <paso>  ...
   Verificación: <cómo se comprobará que se resolvió (IDEn, medición, documento)>
```

Nada de "ejecución inmediata" ni "a corto plazo" sin cifra (P7). Si el usuario descarta un hallazgo crítico, se deja
constancia en el anexo de pendientes con su motivo.

## 3. Estructura del informe (Fase 5)

1. **Resumen ejecutivo** (máximo 1 página, para quien decide), en este orden:
   - problema o necesidad, con cifra;
   - **la decisión que se solicita**, con su umbral ("aprobar si el VPN > 0 a la tasa del cliente" o "si se paga en < N años");
   - recomendación;
   - cuánto cuesta, **con la precisión del nivel de estudio** (perfil ±30–50 %, prefactibilidad ±20–30 %, factibilidad
     ±10–15 %; referencia AACE 18R-97 clases 5–3, SUPUESTO de práctica común);
   - cuánto ahorra o gana (en $ y kWh);
   - **el costo de no actuar** (lo que se sigue pagando por año);
   - riesgo principal;
   - siguiente paso, con responsable y fecha.

   Lenguaje llano, incertidumbre en frecuencias ("de cada 10 años, en 9…"), **técnico y no publicitario**: sin adjetivos de
   venta (P11, y la lección del pitch que "parecía un comercial").
2. Antecedentes, objetivo y alcance (de la Ficha de Encargo), con el **nivel de estudio** declarado.
3. Metodología y fuentes (jerarquía N1–N6).
4. Caracterización (sitio, demanda, recurso, sistema o mercado, según la skill).
5. Análisis y resultados: alternativas comparadas (incluida "no hacer nada"), sensibilidad y prueba de cierre.
6. Hallazgos (estructura §2).
7. Recomendaciones priorizadas y plan de acción: **cronograma y desembolsos** por etapa, y **alternativas de
   financiación** cuando aplique (recursos propios, crédito, leasing, ESCO o contrato por desempeño, PPA).
8. **Matriz de riesgos** (probabilidad × impacto, con mitigación y responsable): regulatorio, social (consulta previa),
   financiero, de ejecución y técnico.
8b. **Plan de medición y verificación** del ahorro o de la producción: qué se mide, cómo, cada cuánto, quién y cuánto
   cuesta (sin M&V el ahorro prometido no se puede demostrar).
9. Qué falta para el siguiente nivel de estudio.
10. Anexos:
    - A. Registro de Supuestos;
    - B. Trazabilidad;
    - C. Normas citadas con su fecha de consulta;
    - D. Salidas de los scripts;
    - E. Pendientes y hallazgos descartados.

Cada skill puede reemplazar el §4 o el §5 por su estructura propia. Por ejemplo, la auditoría usa la estructura de la ISO 50002-1 en
`gestion-energetica`.

## 4. Tabla de trazabilidad (anexo B)

```
| Cifra del informe | Dónde aparece | Cálculo (script y función o fórmula) | Datos de entrada (# del registro) |
|---|---|---|---|
| VPN = 48,2 M COP | resumen, §5 | evaluacion_financiera.py flujo_caja | S1, S2, S3, S5, S7 |
```

Toda cifra del resumen ejecutivo debe estar en esta tabla. Si una cifra no tiene fila, no va al informe (P2: ningún
número "de memoria").

## 5. Lista de chequeo antes de entregar

**Coherencia (P1, P3)**
- [ ] Los balances suman lo que dice la factura o la fuente, dentro de la tolerancia declarada. Los % suman 100 %.
- [ ] Cada gráfico se generó desde la misma tabla que el texto, sin cifras copiadas a mano.
- [ ] E = P·h·FP cierra para cada energía reportada; el FP implícito es plausible.
- [ ] Energía y costo se reportan por separado, con las unidades homogéneas y declaradas.
- [ ] (GE) La línea meta queda por debajo de la línea base en todo el rango de la variable.

**Trazabilidad y supuestos (P2, P4)**
- [ ] Cada cifra del resumen está en la tabla de trazabilidad.
- [ ] El Registro de Supuestos está aprobado, con un solo valor por variable.
- [ ] Ningún dato del material del curso se presenta como vigente.

**Economía (P5)**
- [ ] Hay flujo de caja año a año, con VPN, TIR (o la nota de por qué no existe), payback y sensibilidad de 3 a 5 variables.
- [ ] Están declarados el esquema de financiación (quién paga, quién es dueño, quién opera, quién recibe el beneficio) y la tasa de descuento.
- [ ] (ER, MC) Los excedentes se valoran con la regla CREG vigente, aparte del autoconsumo.

**Normativa**
- [ ] Cada norma citada fue verificada en la Fase 2, con su fecha, o lleva la marca `[verificar vigencia — corte AAAA-MM]`.
- [ ] No se cita la "Ley 1517", la ISO 50002:2014 ni la NDC del "−51 %" como vigentes.

**Alcance y responsabilidad**
- [ ] El nivel de estudio está declarado, junto con lo que falta para el siguiente.
- [ ] Ninguna recomendación funciona como diseño para construcción. Lo eléctrico se remite a un profesional matriculado y al RETIE.
- [ ] (ER) Si hay territorio étnico, la consulta previa aparece como riesgo de ruta crítica.

**Comunicación (P6, P7, P9–P12)**
- [ ] La demanda y el recurso están cuantificados con su fuente; nunca solo "disponible".
- [ ] Las metas y los plazos tienen cifra, responsable e indicador.
- [ ] Si hay matriz de decisión, los pesos suman 1, la escala está orientada y declarada, el total lo calculó un script y se probó la sensibilidad de los pesos.
- [ ] Cada término evaluativo (viable, rentable, eficiente) tiene una definición operativa.
- [ ] El formato, la extensión y el destinatario coinciden con la Ficha de Encargo.
- [ ] El resumen ejecutivo no tiene tono de venta.
- [ ] Ningún dato del cliente se usó en búsquedas web.
