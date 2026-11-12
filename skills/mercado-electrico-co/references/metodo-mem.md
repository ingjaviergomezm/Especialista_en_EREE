# Método: estructura del MEM, contratos, tarifa y cargo por confiabilidad

**Fuentes:**
- Curso 08: diapositivas "Mecanismos de intercambio" (feb–mar 2026, N4), Encuentros 1 y 3 (N4) y taller de subastas (N3).
- Curso 01: guía U1 (N2).

Toda cifra de mercado que aparece aquí es una **foto ilustrativa**. Los valores vigentes se consultan en vivo
(ver `fuentes-datos.md`).

## 1. Estructura
- **Cadena G-T-D-C:**
  - **G** (generación): hidráulica, térmica y FNCER.
  - **T** (transmisión): STN, ≥ 220 kV.
  - **D** (distribución): STR/SDL, hasta el usuario.
  - **C** (comercialización): compraventa, facturación, medición y representación del usuario.
- **Mercado mayorista (MEM):** generadores y comercializadores. XM es el administrador (ASIC/LAC) y el operador (CND).
  **Mercado minorista:** el comercializador y el usuario.
- **Origen:** el apagón de 1992 llevó a las **Leyes 142 y 143 de 1994**. La 142 regula los servicios públicos (subsidios y contribuciones por estrato); la 143 es la Ley Eléctrica (separación de actividades y participación privada).
- **Usuario no regulado (CREG 131/1998):**
  - umbral: **> 0,1 MW o ≥ 55 MWh/mes**, como promedio de los últimos 6 meses y en un solo sitio de entrega;
  - negocia el precio libremente;
  - si vuelve al mercado regulado, debe permanecer allí un tiempo mínimo (el curso dice **3 años**) `[verificar en vivo en la CREG]`;
  - función: `usuario_no_regulado`.
- **Usuario regulado:** paga el **CU** (CREG 119/2007). CU = G + T + D + Cv + PR (pérdidas) + R (restricciones), a lo que la
  CREG 101 028/2023 agregó el término **COT**, que recupera el saldo de la opción tarifaria.
  - Los valores de cada componente se leen en la **factura** o en la publicación mensual del comercializador.
  - Esto explica "por qué subió la tarifa": se mira qué componente subió y por qué (bolsa, IPP, restricciones, COT).

## 2. Contratos frente a bolsa
- La docente indica que ≈ 80 % de las ventas de los generadores va por contratos y ≈ 20 % por bolsa. Es ilustrativo: se verifica con XM.
- **Contratos:** bilaterales, financieros y registrados ante XM. Dan cobertura frente a la volatilidad.
  - **Por cantidad:**
    - pague lo contratado (el riesgo es del comprador);
    - pague lo demandado (el riesgo es del vendedor);
    - pague lo generado;
    - pague lo contratado condicional.
  - **Por precio:**
    - fijo e indexado (IPC, IPP Oferta Interna o una mezcla);
    - bolsa libre;
    - **bolsa con bandas** (techo si la bolsa supera el techo, piso si queda por debajo, bolsa + K si está en medio; función `precio_bandas`).
- **Asignación** (CREG 024/1995): de menor a mayor precio hasta cubrir el consumo. Si hay empate, los "pague lo contratado" se
  asignan completos y los "pague lo demandado" a prorrata.
- **Posición en bolsa:**
  - al comprador le falta energía → la compra en bolsa y pierde si P_bolsa > P_contrato;
  - al vendedor le sobra → la vende en bolsa y gana si P_bolsa > P_contrato.
- **Evaluación de un contrato para un cliente** (función `contrato_vs_bolsa`):
  1. Estimar la energía mensual y la curva de carga horaria; el riesgo está en las horas pico.
  2. Plantear escenarios hidrológicos (Niño, normal y Niña) con precios de bolsa de las **series de XM**, citadas con fecha.
  3. Calcular el costo de cada fracción contratada en cada escenario.
  4. **Lección del taller:** la mejor estrategia depende de la hidrología.
     - Con bolsa a 250, cubrir todo en contrato a 190 cuesta 95 M y la mezcla 60/40 cuesta 107 M.
     - Con bolsa a 150, la mezcla cuesta 87 M.
     - Por eso **ninguna recomendación sale sin sensibilidad hidrológica**.
  5. Revisar las cláusulas: indexación, duración, cantidades, penalidades y la salida a los 3 años.
  6. **Limitación del script:** `costo_mezcla`/`contrato_vs_bolsa` modelan en la práctica "pague lo demandado" (la
     cantidad contratada sigue al consumo). En "pague lo contratado" hay además **riesgo de volumen**: si el consumo real
     queda por debajo de lo contratado, el sobrante se liquida a bolsa (pérdida si la bolsa está baja). Ese escenario
     se calcula aparte, con consumo bajo y bolsa baja simultáneos.

## 3. Subastas
- **Teoría:** subasta inversa; sobre cerrado a primer o a segundo precio (Vickrey); abiertas inglesa y holandesa; maldición del ganador.
- **FNCER de largo plazo** (Res. MME 40590/2019 y modificaciones): dos puntas, sobre cerrado, bloques horarios.
  - Resultados de 2019 y 2021: 1 281 MW a ≈ 155,7 $/kWh y 796 MW a ≈ 194,8 $/kWh (precios a dic-2024).
  - **Solo ≈ 17 % estaba en operación y ≈ 40 % se canceló** → adjudicar no es construir: hay riesgo de ejecución.
- **Energía ofertable** = MW × 24 × factor. Factores del taller (N3, **SUPUESTO didáctico**, no son los de la metodología
  vigente): solar 8–15 %, eólica 20–30 %, térmica 90 %, hidráulica 30–40 %.

## 4. Cargo por confiabilidad
- **ENFICC:** la energía firme máxima en hidrología crítica, por año (CREG 071/2006).
  - Aproximación del curso en % de capacidad (N4, **SUPUESTO didáctico**; la ENFICC real sale de la metodología CREG y de
    los protocolos CNO, consultados en vivo): hidráulica 30–40 %, térmica 90 %, solar 10–20 %, eólica 20–30 %.
  - **ENFICC ≠ factor de planta.** El FP es el promedio y la ENFICC es el mínimo firme (lección del curso 04).
- **OEF:** obligaciones adjudicadas en subasta (sobre cerrado, precio marginal, hasta 20 años).
- **Precio de escasez:**
  - Si la bolsa lo supera, se activan las OEF y el precio queda acotado: el riesgo pasa del consumidor al generador.
  - **Desde la CREG 101 066/2024 hay un precio de escasez inferior y uno marginal.** La CREG 101 102/2026 reabrió la opción de acogerse al inferior.
  - Hay un proyecto de precio de escasez superior. El valor del mes se consulta en vivo.
- **Oferta mínima en bolsa** = CERE + FAZNI.
- **Restricciones:** generación de seguridad fuera de mérito, por ejemplo en los enlaces Interior–Costa. Su costo pasa al componente R del CU.

## 5. Autogeneración y excedentes (lo que el curso 08 no desarrolló, actualizado al corte 2026-11)
- **AGPE y GD:** CREG 174/2021, modificada.
  - **Los excedentes Exc2 se valoran con el costo promedio ponderado Mc** (CREG 101 072/2025).
  - Durante la transición se aplica el precio de bolsa (CREG 101 087/2025, que también sustituyó la liquidación del art. 24).
- **Autogeneración remota:** CREG 101 099/2026.
- **Comunidades energéticas:**
  - figuras de autogeneración colectiva y generación distribuida colectiva (Decreto 2236/2023, CREG 101 072/2025);
  - los excedentes de una autogeneración colectiva de hasta 1 MW se reparten con reglas propias;
  - para comercializar deben cumplir las mismas condiciones que cualquier agente.
- **En la skill:**
  - el precio de los excedentes es un **dato de entrada** que sale de la regla vigente y de la oferta del comercializador;
  - el autoconsumo se valora a la tarifa evitada;
  - nunca se asume que son iguales.
