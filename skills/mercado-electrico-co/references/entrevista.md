# Entrevista de encargo — mercado-electrico-co (Fase 0)

Cómo usar este banco:
- Primero identifica el **tipo de encargo** (pregunta 1) y luego usa solo el bloque que le corresponde, más los bloques A y F.
- Pregunta en bloques de 4–5. Si una respuesta es "no sé", anótala como `[POR CONFIRMAR]`.

## Bloque A — Encargo y decisión (siempre)
1. ¿Qué tipo de encargo es?
   - (a) Entender o reducir la tarifa.
   - (b) Pasarse al mercado no regulado o negociar un contrato.
   - (c) Vender excedentes, autogenerar o formar una comunidad energética.
   - (d) Analizar el precio de bolsa o modelar un despacho.
   - (e) Planeamiento: demanda o escenarios.
2. ¿Qué decisión se toma con el resultado y quién la toma?
3. Horizonte de tiempo: este mes, 1 año, la duración del contrato, 10–20 años.
4. Criterio de éxito con números. Por ejemplo: "un precio contratado al menos 10 % por debajo del CU actual" o "exposición a bolsa < 20 %".

## Bloque B — Usuario y tarifa (encargos a y b)
5. Tipo de usuario (regulado o no regulado), nivel de tensión, estrato o uso, comercializador y operador de red.
6. Consumo (kWh/mes) y demanda máxima (kW) de los **últimos 6 meses**, medidos en un solo sitio.
   *(con eso se verifica si cumple > 0,1 MW o > 55 MWh/mes para ser no regulado)*
7. ¿Comparte las facturas con el desglose del CU (G, T, D, Cv, PR, R y el término COT si aparece)?
8. Si ya es no regulado: precio, indexación (IPP o IPC), duración, cantidades, penalidades y modalidad (pague lo contratado
   o pague lo demandado).
   *(si vuelve al mercado regulado, debe permanecer allí 3 años)*
9. ¿Tiene curva de carga horaria? *(define el costo en bolsa por hora y el riesgo de las horas pico)*

## Bloque C — Autogeneración y excedentes (encargo c)
10. Capacidad instalada o prevista (kW) y tecnología; porcentaje esperado de excedentes respecto al consumo.
11. ¿La autogeneración es en sitio, remota o colectiva (comunidad energética)? ¿Quiénes participan?
    *(cada figura tiene reglas CREG distintas y cambiaron entre 2025 y 2026)*
12. ¿Ya hay solicitud de conexión al operador de red? ¿Qué respondió?

## Bloque D — Bolsa y despacho (encargo d)
13. ¿Qué periodo, qué horas y qué zona? ¿Datos de XM descargados o hay que buscarlos?
14. ¿Qué se quiere explicar: el precio, la planta marginal, el efecto de la hidrología o una congestión?
15. Si es un modelo (microrred o nodos): cargas, recursos, costos, límites de líneas y baterías (capacidad, potencia, eficiencia, estado de carga inicial).

## Bloque E — Planeamiento (encargo e)
16. ¿Ámbito nacional, regional o del cliente? ¿Qué escenarios oficiales de la UPME se toman como referencia?
17. ¿Qué incertidumbres críticas quiere explorar? Por ejemplo: hidrología, CAPEX, retiro del carbón, demanda.

## Bloque F — Entregable (siempre)
18. Formato (informe, Excel, presentación, nota técnica) y extensión.
19. Plazo.

---

## Plantilla de salida — Ficha de Encargo
```
FICHA DE ENCARGO — mercado-electrico-co  Fecha: AAAA-MM-DD   Versión: 1
Tipo de encargo: tarifa | contrato | excedentes | despacho | planeamiento
Decisión y quién decide:
Horizonte:
Criterio de éxito (operativo):
Usuario: regulado/no regulado · tensión · comercializador · OR
Consumo y demanda (últimos 6 meses, fuente):
Datos disponibles: facturas · curva de carga · contrato · series XM
Incluido:                       Excluido:
Entregables y formato:          Extensión:
Plazo:
Datos pendientes [POR CONFIRMAR]:
→ ¿Aprobado? (sí / ajustes)
```
