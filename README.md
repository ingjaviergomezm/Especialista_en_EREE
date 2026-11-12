<div align="center">

# Especialista en EREE

### Tres skills de Claude para trabajar en campo en energías renovables, eficiencia energética y mercado eléctrico en Colombia

`proyectos-er` · `gestion-energetica` · `mercado-electrico-co`

![versión](https://img.shields.io/badge/versión-v0.9-F5B14C?style=flat-square&labelColor=0E0E0C)
![pruebas](https://img.shields.io/badge/pytest-149_pasan-7AB87A?style=flat-square&labelColor=0E0E0C)
![normativa](https://img.shields.io/badge/normativa-corte_2026--11-B5B0A4?style=flat-square&labelColor=0E0E0C)
![python](https://img.shields.io/badge/python-3.11+-B5B0A4?style=flat-square&labelColor=0E0E0C)
[![licencia](https://img.shields.io/badge/licencia-CC_BY_4.0-B5B0A4?style=flat-square&labelColor=0E0E0C)](LICENSE)

</div>

---

## Por qué existe

Al terminar la **Especialización en Energías Renovables y Eficiencia Energética (EVEREE, Universidad Autónoma de Manizales)** me quedé con unos 330 archivos: guías, diapositivas, hojas de Excel, cuadernos de despacho y mis propias entregas con la retroalimentación de los profesores.

Ese material sirve para aprobar un curso. Lo que necesito en el trabajo es otra cosa: **llegar a una planta, a una finca o a la oficina de un cliente y responder con método**. Por ejemplo:

- "¿Me conviene poner paneles?"
- "¿Por qué gastamos tanta energía?"
- "¿Me paso al mercado no regulado?"

Estas skills convierten ese material en **método profesional ejecutable**. Claude entrevista, calcula con scripts probados, verifica la norma vigente y entrega un informe con el que una gerencia puede decidir. Lo hace sin inventar un solo dato y deteniéndose para que el especialista apruebe cada paso.

> El objetivo no es replicar los entregables de la universidad. Es aplicar lo aprendido con la fiabilidad que exige un cliente.

---

## Qué hay en el conjunto

| Skill | La pregunta del cliente | Qué hace |
|---|---|---|
| **`proyectos-er`** | *"¿Le sirve un sistema renovable a este sitio?"* | Diagnostica la demanda y el recurso (solar, eólico, hídrico, biomasa) y selecciona la tecnología. Dimensiona sistemas FV conectados a red: strings, DC/AC, PR, P50/P90. Hace la prefactibilidad (CAPEX, VPN, TIR, payback, LCOE, sensibilidad) y revisa incentivos (Ley 1715/2099), excedentes (CREG 174 y modificaciones), impacto social y riesgos. |
| **`gestion-energetica`** | *"Esta instalación gasta mucho."* | Hace la revisión y auditoría energética (ISO 50002-1) y el balance por energético con prueba de cierre. Identifica los usos significativos (USE) y define indicadores (IDEn). Construye la línea base por regresión con CUSUM (ISO 50006) y evalúa medidas de ahorro con costo-beneficio: iluminación, motores, aire comprimido, calderas, factor de potencia, cogeneración. Diagnostica el SGE frente a ISO 50001. |
| **`mercado-electrico-co`** | *"¿Cuánto me cuesta la energía y cómo la compro o la vendo?"* | Explica el MEM y compara bolsa con contratos (pague lo contratado o lo demandado, bandas). Evalúa el paso a usuario no regulado y desglosa los componentes del CU. Modela el despacho por orden de mérito y la microrred con estado de carga. Cubre el cargo por confiabilidad, las subastas, los excedentes de autogeneración y la proyección de demanda por escenarios. |

Las tres comparten un motor común: Ficha de Encargo, Registro de Supuestos, estructura de hallazgo, plantilla de informe y vigencia normativa. También se pasan el trabajo entre sí:

```
reducir consumo ──► gestion-energetica
                      │  (demanda ya reducida)
                      ▼
generación nueva ──► proyectos-er ◄── precio de energía y excedentes ── mercado-electrico-co
```

---

## Cómo trabaja: el humano siempre en el ciclo

Ninguna skill salta de la pregunta al número. Cada encargo pasa por **seis fases**, y en las críticas hay una **compuerta ⛔** que solo se abre con la aprobación del especialista.

| Fase | Qué pasa | Compuerta |
|---|---|---|
| **0. Entrevista** | Preguntas en bloques cortos (≤ 5 por turno), cada una con su porqué: objetivo, decisión, alcance, nivel de estudio, datos, restricciones | ⛔ Ficha de Encargo aprobada |
| **1. Datos** | Cada dato con su origen: medido, factura, atlas o supuesto. Lo que falta queda `[POR CONFIRMAR EN CAMPO]` | ⛔ Registro de Supuestos aprobado |
| **2. Norma en vivo** | Consulta la vigencia en fuentes oficiales (CREG, UPME, MinEnergía, DIAN, XM) y la contrasta con la referencia | ⛔ si algo cambia la conclusión |
| **3. Cálculo** | Scripts probados, sensibilidad tipo tornado, prueba de cierre de energía | ⛔ Resultados preliminares validados |
| **4. Hallazgos** | Siempre en este orden: **qué se revisó → cómo → hallazgo → riesgo o impacto → recomendación con procedimiento** | ⛔ Hallazgos aprobados |
| **5. Entrega** | Resumen ejecutivo en pesos y kWh concretos, anexos de supuestos y fuentes, lista de chequeo | Autoverificación |

Para preguntas acotadas existe un **modo rápido** del tipo "¿cuántos paneles para 300 kWh/mes?". Entrega solo nivel **PERFIL**, declara cada supuesto y **nunca recomienda comprar**: si la conversación llega a "¿lo compro?", vuelve a la entrevista.

### Las reglas que no se negocian

1. **No inventar datos.** Toda cifra sale de un script, de una fuente citada o queda marcada como `SUPUESTO`.
2. **Normas y precios con fecha.** Lo que no se verifica en vivo lleva `[verificar vigencia — corte AAAA-MM]`.
3. **Nivel de estudio declarado.** Perfil, prefactibilidad o factibilidad. **Nunca diseño para construcción**: eso exige un profesional con matrícula y cumplir el RETIE.
4. **Los datos del cliente no salen.** En internet solo se consultan términos públicos.
5. **Prueba de cierre antes de mostrar.** E = P·h·FP, balances que suman 100 % y facturas conciliadas. Si no cierra, no se muestra.

---

## Ejemplos de aplicación

### 1 · Vivienda en Tauramena, Casanare: `proyectos-er`

> *"Mi mamá paga como 250 mil de luz. ¿Le conviene poner paneles? Dime cuántos y cuánto vale, rápido."*

**Lo que hace la skill:**
- **Datos que faltan:** explica en una frase que con pesos y sin kWh el número puede moverse un 25 %. Pide la tarifa y el estrato (en estratos 1–3, el kWh ahorrado dentro de la subsistencia vale la tarifa subsidiada).
- **Cálculo puntual de perfil:** **4 a 5 módulos de 590 Wp**, entre 3 500 y 4 350 kWh al año. Cada supuesto queda declarado: radiación del atlas, PR y fracción de autoconsumo.
- **"¿Cuánto vale?":** no inventa un precio. Responde con el **máximo que puede costar el sistema para pagarse en 5 años** y pide 2 o 3 cotizaciones.
- **"¿Le digo que compre?":** abre la entrevista completa y arma la Ficha de Encargo, con la estructura del techo de zinc `[POR CONFIRMAR EN CAMPO]`.

### 2 · Planta de lácteos en Boyacá: `gestion-energetica`

> *"La factura subió mucho este año. Quiero saber dónde se está yendo la energía y qué hago."*

**Lo que hace la skill:**
- **Conversión del GLP:** pasa los kg de GLP a kWh con el PCI del distribuidor, no con un valor de ejercicio.
- **Balance contra la factura:** el inventario explica solo el 45 % de la electricidad facturada. **No muestra porcentajes hasta conciliar** y pide los equipos que faltan: tanque de enfriamiento, aire comprimido, CIP.
- **Línea base:** con 8 meses de facturas y 6 de producción, la marca **PROVISIONAL** y no calcula meta.
- **Traducción a pesos:** *"aunque no produzcas un litro, la planta gasta unos 8 100 kWh al mes; eso son 6,3 millones de pesos fijos."*

### 3 · Industria evaluando el mercado no regulado: `mercado-electrico-co`

> *"Consumimos 70 MWh al mes. ¿Nos conviene pasarnos a no regulado y contratar?"*

**Lo que hace la skill:**
- **Umbral:** verifica si el consumo supera el límite (> 0,1 MW o ≥ 55 MWh/mes, CREG 131/1998), con la marca de vigencia.
- **Escenarios hidrológicos:** compara contrato fijo, contrato con bandas y bolsa en años Niño, normal y Niña. La lección es que **la mejor estrategia cambia con la hidrología**: con la bolsa a 250 $/kWh, contratar todo cuesta 95 M; con la bolsa a 150, la mezcla cuesta 87 M.
- **Riesgo de volumen:** en "pague lo contratado", si el consumo cae por debajo de lo contratado, el sobrante se liquida a bolsa. Lo calcula como escenario aparte.

### Otros campos de aplicación

- **Consultoría e ingeniería:** perfiles y prefactibilidades FV, PCH, eólica o biomasa; matrices de selección de tecnología; comparación con la opción "no hacer nada".
- **Industria y edificios:** auditorías de nivel ASHRAE I/II, diagnóstico de brechas ISO 50001 (plantilla Excel con 26 requisitos) y planes de ahorro priorizados por VPN.
- **Entidades públicas:** PGEE bajo la Ley 2407/2024, con línea base, metas y seguimiento.
- **Compras de energía:** evaluación de ofertas de comercializadores y lectura de los componentes del CU ("¿por qué subió la tarifa?").
- **Comunidades y territorio:** autogeneración colectiva, riesgo social y consulta previa como riesgo crítico de cronograma.
- **Análisis de mercado:** quién marca el precio en una hora, efecto de El Niño, series de XM anotadas con eventos, margen de reserva nominal frente a firme.

---

## Fiabilidad: cómo se probó

| Prueba | Resultado |
|---|---|
| **pytest** | **149 pruebas** pasan: 63 de `proyectos-er`, 61 de `gestion-energetica` y 25 de `mercado-electrico-co` |
| **Reproducción del material** | Los scripts reproducen **exactamente** los resultados de los profesores: Excel de VPN, TIR, FV e Hidro; Lote 10 en PVsyst; despacho G3 con su planta marginal hora a hora; microrred lineal con objetivo 307 188,54 |
| **Errores del material, documentados** | Se reproducen en una prueba y se corrigen en el método: impuesto con referencia absoluta en el Excel del curso, batería sin estado de carga, densidad de gas fuera de rango, eficiencia de biomasa, aritmética de cierre en planeamiento |
| **Simulación con el humano en el ciclo** | Dos casos simulados (FV residencial y planta de alimentos) con un usuario apurado y datos incompletos: las skills se detuvieron en cada compuerta y no inventaron. Las 12 fallas que encontró la simulación se corrigieron |
| **Revisión adversarial (red team)** | Un revisor independiente encontró 17 grupos de hallazgos: excedentes Exc1/Exc2, "precio por zona", reactiva hora a hora, valores por defecto ocultos, entre otros. **Todos corregidos, cada uno con su prueba** |
| **Disparadores** | 10 peticiones reales llegan a la skill correcta, sin choques con otras skills instaladas |

El detalle está en [`docs/verificacion.md`](docs/verificacion.md) y [`docs/disparadores.md`](docs/disparadores.md).

### Jerarquía de fuentes

Cada dato lleva su nivel. Cuando dos fuentes chocan, gana la de nivel más alto y el choque se anota.

`N1` norma vigente › `N2` guías del curso › `N3` ejercicios resueltos por los profesores › `N4` diapositivas › `N5` entregables propios bien calificados (ejemplo, no método) › `N6` lecciones de errores (nunca dato)

---

## Instalación

### Claude Code

```bash
git clone https://github.com/ingjaviergomezm/Especialista_en_EREE.git
cp -r Especialista_en_EREE/skills/* ~/.claude/skills/
```

Claude carga cada skill sola cuando la conversación lo pide; no hay que nombrarla.

### claude.ai

Comprime cada carpeta de `skills/` como `.zip` (por ejemplo `proyectos-er.zip`, con la carpeta en la raíz) y súbela en **Configuración → Capacidades → Skills**.

### Correr los scripts y las pruebas

Requiere Python 3.11+ con `numpy`, `scipy` (solo microrred), `openpyxl` y `pytest`.

```bash
cd skills/proyectos-er
python -m pytest scripts -q
python scripts/fv_dimensionamiento.py --consumo-mes 300 --hsp 4.8 --pr 0.78 --wp 590
python scripts/evaluacion_financiera.py --capex 12000000 --anos 25 --tasa 0.12 --energia 3480 --tarifa 850 --payback-objetivo 5
```

Cada script acepta `--help` y `--ejemplo`.

---

## Estructura

```
skills/
├── proyectos-er/
│   ├── SKILL.md                 flujo, compuertas, reglas, mapa de referencias
│   ├── references/              método FV, otras fuentes, financiero, impacto social,
│   │                            normativa vigente, informe técnico, entrevista, brechas
│   ├── scripts/                 fv_dimensionamiento · evaluacion_financiera · recursos_0d (+ pruebas)
│   ├── CHANGELOG.md
│   └── COMO_ACTUALIZAR.md
├── gestion-energetica/
│   ├── references/              revisión energética, línea base, medidas, ISO 50001, ...
│   ├── scripts/                 balance_energetico · linea_base · medidas_ahorro (+ pruebas)
│   └── assets/                  diagnostico_iso50001.xlsx
└── mercado-electrico-co/
    ├── references/              MEM, despacho, planeamiento, fuentes de datos, ...
    └── scripts/                 despacho_economico (+ pruebas y datos de prueba)
```

---

## Qué NO hacen

- **No firman diseños.** Todo resultado es de perfil, prefactibilidad o factibilidad. La ingeniería de detalle exige un profesional matriculado y cumplir el RETIE.
- **No dan precios de mercado vigentes de memoria.** Las cifras del curso son ilustrativas; las vigentes se consultan en XM, UPME, CREG o con la cotización del cliente.
- **No reemplazan el software especializado.** Para el diseño final se remiten a PVsyst, HOMER Pro o LEAP; los scripts sirven para dimensionar, verificar y decidir.
- **No son asesoría financiera ni legal.** Los incentivos tributarios se modelan con cifras que entrega el contador del cliente.
- **No se actualizan solas.** La normativa tiene `fecha_corte: 2026-11`; [`COMO_ACTUALIZAR.md`](skills/proyectos-er/COMO_ACTUALIZAR.md) describe la revisión semestral.

---

## Licencia y cómo dar crédito

Este repositorio está bajo **[Creative Commons Atribución 4.0 Internacional (CC BY 4.0)](LICENSE)**.

**Puedes**, incluso con fines comerciales:
- usar las skills, los scripts y las referencias;
- copiarlos, adaptarlos y redistribuirlos.

**Siempre debes dar crédito.** Cualquier uso, copia o derivado debe:
1. nombrar al autor: **Javier Gómez M.**;
2. enlazar este repositorio;
3. enlazar la licencia;
4. indicar si hiciste cambios.

Formato de atribución sugerido:

> *Especialista en EREE* — Javier Gómez M. (2026). https://github.com/ingjaviergomezm/Especialista_en_EREE · Licencia CC BY 4.0 · [modificado por …]

Los datos de prueba de origen académico (ver [Créditos](#créditos)) no son obra del autor y no quedan cubiertos por esta licencia.

---

## Créditos

- **Formación de base:** Especialización en Energías Renovables y Eficiencia Energética, **Universidad Autónoma de Manizales (UAM)**. El método se destiló con palabras propias y con cita de la fuente; las skills no reproducen texto del curso.
- **Datos de prueba:** `mercado-electrico-co/scripts/datos_prueba/` y algunas series de las pruebas provienen de ejercicios académicos de la especialización. Se usan **solo como pruebas de regresión**, con atribución ([detalle](skills/mercado-electrico-co/scripts/datos_prueba/README.md)).
- **Normativa:** consultada en fuentes oficiales (CREG, UPME, MinEnergía, DIAN, XM, Función Pública) con corte a noviembre de 2026.

---

<div align="center">

**Javier Gómez M.** · Ingeniero Industrial · Especialista en Energías Renovables y Eficiencia Energética

[Portafolio](https://ingjaviergomezm.github.io/) · [GitHub](https://github.com/ingjaviergomezm) · [LinkedIn](https://www.linkedin.com/in/ingjaviergomezm/)

<sub>"Si es medible, es mejorable."</sub>

</div>
