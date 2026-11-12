# Método: despacho económico, precio de bolsa, nodos y microrredes

**Fuentes:**
- Curso 08: diapositivas MEC p.56–69 (N4); datos G3 y ejercicio JuMP de la docente (N3).
- CREG 025/1995 (código de operación) `[verificar modificaciones]`.

**Script:** `scripts/despacho_economico.py`. Reproduce exactamente las correcciones de la docente.

## 1. Secuencia operativa
1. **D−1, antes de las 8:00:** cada generador oferta un **precio único para las 24 h** y la **disponibilidad hora a hora**.
   - Las térmicas declaran además rampas y precios de arranque y parada.
   - Las hidráulicas pueden declarar mínimos operativos.
2. **Predespacho ideal:** el despacho sin restricciones define la planta marginal y el precio de cada hora.
3. **Despacho programado:** agrega las restricciones del SIN y los intercambios internacionales.
4. **D+1, despacho ideal** con la demanda real → **precio de bolsa** hora a hora y liquidación.

**Qué mueve el precio de bolsa:**
- hidrología y reservas;
- balance entre oferta y demanda;
- combustibles;
- mantenimientos;
- TRM;
- márgenes de los agentes;
- nivel de contratación.

## 2. Orden de mérito (función `merito`)
1. En la hora h se toman las plantas con disponibilidad > 0 y se ordenan de menor a mayor precio de oferta.
2. Se acumula su disponibilidad hasta cubrir la demanda D_h.
3. **La planta marginal es la última necesaria, y su precio de oferta es el precio marginal.**
4. **Por zona (solo como ejercicio didáctico):** el predespacho de Interior o de Costa usa **solo las plantas de esa
   zona**. El nacional usa todas. **En Colombia no hay precio por zona:** el precio de bolsa es uno nacional, sale del
   despacho ideal de XM (solo las plantas flexibles marcan precio) e incluye un adicional sobre el precio marginal; la
   congestión entre áreas se paga como restricciones (componente R del CU). Para un precio real se consulta XM.
   - Con `precio_escasez=` el script alerta cuando el marginal lo supera (se activan las OEF).
   - **Se respeta la zona que trae el archivo de datos**, no la geografía. En G3, Urrá figura en "Interior".
5. **Siempre se reportan la planta marginal y el precio** de cada hora y zona. Si hay empate de precio, se listan las empatadas.
   - Lección de A4: se reportó solo el precio y hubo errores en H23 y H0.
6. **Déficit:** si la disponibilidad no alcanza, se reporta el déficit. No se inventa un precio.

**Casos de prueba (G3; todos pasan):**

| Zona y hora | Planta marginal | Precio |
|---|---|---|
| Nacional H23 | Betania | 1 015 $/kWh |
| Interior H0 | Urrá | 1 020 $/kWh |
| Nacional H0 | Guavio | 1 005 $/kWh |
| Costa H0 | Guajira 2 | 479,476 $/kWh |

## 3. Condición hidrológica
- **No se usan umbrales propios.** Los 40/60 % de mi entregable no tenían fuente (B-MC2).
- Se consultan en XM los aportes hídricos como % de la media histórica y el nivel del embalse agregado, más el pronóstico ENSO (IDEAM/NOAA).
  Se cita la fecha.
- La participación hidráulica en el despacho se puede **describir**, pero no reemplaza esos indicadores.

## 4. Despacho uninodal y nodal (función `dos_nodos`)
- Ofertas lineales π = a + b·P. Sin congestión, un solo precio; con congestión, cada nodo tiene su precio.
- **Renta de congestión** = (π_importador − π_exportador) × límite de la línea.
- **Caso del curso:**
  - A tiene 500 MW con π = 10 + 0,01·P; B tiene 1 500 MW con π = 13 + 0,02·P.
  - Sin límite: π = 24,33 y el flujo es de 933 MW.
  - Con una línea de 400 MW: π_A = 19, π_B = 35 y la renta es de 6 400 $/h.
- **Regla:** el precio es mayor en el nodo importador y menor en el exportador.
- **Didáctico:** Colombia no liquida precios nodales; sirve para entender congestión y la discusión de reforma.

## 5. Microrredes
- **Ejercicio del curso** (función `microrred_curso`):
  - programa lineal de 24 h con solar fija y diésel de 0 a 8,56 kW;
  - batería de 0 a 10 kW **tratada como un generador**;
  - penalidad de 1 000 $/kWh por demanda no atendida;
  - objetivo = **307 188,54** (lo reproduce exactamente con scipy/HiGHS).
- **Defecto de método (B-MC4):** la batería entrega energía que nunca cargó, el excedente solar no se almacena y la penalidad es
  arbitraria. **No se usa para decidir.**
- **Modelo recomendado** (función `microrred_soc`):
  - SOC_t = SOC_{t−1} + η_c·carga − descarga/η_d;
  - límites de SOC y de potencia;
  - **SOC final ≥ SOC inicial**, para no "regalar" energía;
  - vertimiento explícito;
  - **un VOLL o costo de racionamiento con fuente** (UPME, en vivo) o declarado como SUPUESTO (B-MC5).
  - Las pruebas verifican el balance horario y el del SOC.
- **Para un diseño de sistemas híbridos aislados** se remite a HOMER Pro (B-ER2). Esta función sirve para entender el despacho.

## 6. Análisis de series históricas (lección de A2)
- **Fuentes:** XM Sinergox/SIMEM (datos abiertos), UPME y MinEnergía.
- Lo que pide un análisis profesional son **series de tiempo superpuestas con los eventos anotados** (Niño y Niña, COVID, cambios
  normativos), no coeficientes de correlación ni diagramas de dispersión.
- Cada variable se define con su unidad y su fuente.
