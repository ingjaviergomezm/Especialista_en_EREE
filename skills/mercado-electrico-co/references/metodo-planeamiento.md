# Método: proyección de demanda, escenarios y margen de reserva

**Fuentes:**
- Curso 04 *Planeamiento Energético*: presentación UPME de proyección de demanda 2022 y resumen del PEN (N4).
- Mis entregables A1.2, A2.3 y A3.2. Son N5: sirven como ejemplo, no como método, y tienen errores de cierre que se corrigen aquí.
- El curso no trae una guía de método, así que hay más SUPUESTOS estándar que en otros temas.

**Script:** `scripts/despacho_economico.py` (funciones `proyeccion`, `cierre_energia` y `margen_reserva`).

## 1. Proyección de demanda
- **Nacional o regional:** se usa la **revisión vigente de la UPME** (escenarios bajo, medio y alto, con bandas, por región y mercado),
  consultada en vivo.
  - Como escala, la revisión de 2022 proyectaba un crecimiento del SIN de 2,22 a 3,35 %/año, con 2,4 % en el escenario medio, para 2022–2036.
  - La generación distribuida resta entre 0,19 y 1,45 %.
- **Cliente:** la proyección parte de **su** historial y sus planes (ampliaciones, cambio de equipos). La tasa nacional es solo una referencia.
- **Método simple:** E_t = E_0·(1+g)^t, con **una sola tasa por escenario y su fuente citada**.
  - Lección de A1.2: el informe mezcló 2,01 % y 2,92 % como si fueran "la" tasa.
  - Las limitaciones se declaran (autogeneración, choques).

## 2. Escenarios prospectivos (Schwartz; aplicado en A3.2)
1. **Problema focal:** la decisión concreta.
2. **Fuerzas motrices:** costos de las FNCER, hidrología (ENSO), demanda, política de CO₂ y regulación.
3. **Incertidumbres críticas:** las de mayor impacto e incertidumbre.
4. **Matriz 2×2** con las dos incertidumbres críticas.
5. **Narrativa cuantificada** con reglas explícitas, por ejemplo "1 MW de carbón retirado ↔ 1,2 MW de FNCER".
6. **Implicaciones:** KPI (CO₂, margen, $/MWh) y decisión.

**Herramienta:** LEAP (demanda, capacidad, despacho y margen). Se consigue la licencia por la vía académica o institucional.

## 3. Supuestos y documentos oficiales (siempre en vivo y con fecha)
| Supuesto | Documento vigente al corte 2026-11 |
|---|---|
| CAPEX y O&M por tecnología | Catálogo Tecnológico de Generación de la UPME (la edición vigente) |
| Expansión y retiros | **PIEG 2025–2039**, que reemplaza el 2023–2037 que usé |
| Plan de largo plazo | **PEN 2024–2054** (publicado por la UPME; adopción formal `[no confirmada]`) |
| Meta climática | **NDC 3.0**: tope de 169,44 Mt CO₂e en 2030 y de 155–161 Mt en 2035. El "−51 %" quedó obsoleto |
| Factores ENFICC de FNCER | CREG 101 044/2024 y metodología UPME `[verificar]` |
| Precio sombra del CO₂ | declarar la fuente. Referencia nacional: impuesto al carbono 2026 de $29 070/t CO₂e |

## 4. Prueba de cierre (obligatoria)
- **E = P·h·FP** para toda cifra de energía.
- **Lecciones de A3.2, que fue bien calificado y aun así no cerraba:**
  - "1,6 GW de carbón ↔ 1,6 TWh/año": con FP de 0,8 son **11,2 TWh**; incluso con un despacho del 30 % serían 4,2 TWh.
  - "5,6 GW de FNCER → 17 TWh": con FP de 0,16 son **7,8 TWh**. Llegar a 17 exigiría un FP de 35 %.
  - Se usó la ENFICC (0,14/0,18) como si fuera el factor de planta. **ENFICC ≠ FP.** El FP eólico de La Guajira es mucho mayor que 0,14 `[verificar en vivo]`.
- **La calificación alta premió el método y las fuentes, no la aritmética. La skill verifica la aritmética.**

## 5. Capacidad y margen de reserva
- Hay una foto de la capacidad del SIN de 2025 (A2.3, Geovisor UPME), con hidráulica ≈ 64 % y solar ≈ 6 %. **Se actualiza con XM o la UPME en vivo.**
- **Margen de reserva** = (capacidad − demanda pico)/demanda pico, **declarando si la base es la capacidad nominal o la firme**
  (función `margen_reserva`).
  - Con la nominal, A2.3 y A3.2 daban más de 60 %.
  - En un sistema hidrodependiente lo relevante es la **energía o potencia firme (ENFICC)**.
