# Método — FV conectado a red (perfil, prefactibilidad y factibilidad)

**Fuentes.**
- Curso 06 *Modelamiento y Simulación*: guías M1 y M2 (N2) e informe PVsyst del Lote 10 (N5, como caso de prueba).
- Curso 05 *Fuentes de ER*: diapositivas de solar (N4).

**Convenciones.**
- `[forma estándar]` = fórmula que la guía tiene en imagen. Se usa la forma IEC o de fabricante como SUPUESTO declarado.
- Script: `scripts/fv_dimensionamiento.py`.

## 1. Dónde está el estudio (M2 p.10–19)
| Etapa EPC | Nivel de la skill | Qué se entrega |
|---|---|---|
| Ingeniería conceptual | perfil o prefactibilidad | concepto, capacidad, alternativas, energía aproximada |
| Ingeniería básica | factibilidad | simulación detallada (PVsyst u otra), BOM preliminar, especificaciones |
| Ingeniería de detalle | **fuera de la skill** | planos y memorias firmados por un profesional matriculado (RETIE) |
| As built | fuera | lo construido, que se entrega a O&M |

Errores que el docente señala:
- subestimar la ingeniería conceptual;
- no actualizar el diseño cuando cambian el sitio o el mercado;
- **usar datos meteorológicos genéricos** (el proyecto deja de ser bancable).

No se modela sin caracterizar el sitio y conocer la regulación local.

## 2. Recurso solar
- **Variables.**
  - GHI: global horizontal.
  - DNI: directa normal; solo importa para concentración.
  - Irradiación en el plano del arreglo: es la que entra a la fórmula.
  - PVOUT: kWh/kWp.
  - "Horas de sol pico" (HSP) = kWh/m²·día en el plano. **El script recibe HSP en el plano.** Si solo hay GHI, se declara
    "H horizontal usada como aproximación (SUPUESTO)" y se contrasta con el PVOUT del atlas, que ya incluye la transposición.
- **Fuentes** (siempre con fecha de consulta):
  - Global Solar Atlas, Atlas IDEAM, PVGIS, NREL/NSRDB, Solargis, Meteonorm.
  - Según el estudio CNO/Uniandes que cita M2 p.68, NREL funciona mejor en montaña y Solargis en llanura.
- **Calidad del dato.**
  - Lo mejor es medir en sitio de 1 a 2 años y correlacionar con satélite. Para la ENFICC de plantas grandes se exige medición en sitio según el protocolo CNO vigente `[verificar umbral y acuerdo en vivo]`.
  - TMY = año típico de 10 a 20 años (ISO 15927-4 `[verificar]`).
  - Con datos gratuitos se decide con **P90**.
- **Inclinación.**
  - β_opt = 3,7 + 0,69·|φ| (curso 05, SOL p.24), con un **mínimo de 15° para autolimpieza**. En Colombia casi siempre manda el 15°.
  - Cerca del ecuador, la pérdida por usar estructura fija es pequeña.
- **Sombras.** Regla de la industria: **ningún módulo con sombra entre las 9:00 y las 15:00**.
  - Distancia entre filas: d = h/tan(α_sol)·cos(γ_sol − γ_panel) `[forma estándar]`, evaluada con la carta solar.

## 3. Selección de equipos (M2 p.32–36): "no hay fórmula mágica"
- **Módulo.**
  - Técnicos: degradación anual, Voc, Isc, coeficientes de temperatura, Wp/m², tecnología (mono o bifacial).
  - Económicos: $/Wp.
  - Comerciales: Incoterm, garantías, certificaciones, corrosión del sitio, conector.
- **Inversor.**
  - Rango MPPT, I máx. por MPPT, Isc admisible.
  - Derrateo por temperatura y altitud; eficiencia europea.
  - Número de MPPT; anti-isla (UL/IEC); rango de FP y THDi.
  - Grado IP; clase de corrosión C3–C5; repuestos.
- **Estructura.** Galvanizado en caliente; NSR-10 (viento y sismo); estudio de suelo e hincado validados por un ingeniero estructural.

## 4. Dimensionamiento
### 4.1 Potencia y energía (M1 p.68–69)
- **E = Pp · H_plano · PR**. Con Pp en kWp y H en kWh/m²·periodo, el resultado sale en kWh.
- Para un consumo: kWp = consumo · cobertura / (H · PR).
  - Es un balance **anual**: no dice qué parte es autoconsumo y qué parte excedente.
  - Para separarlas hace falta el perfil horario de la carga.
- **PR** típico entre 0,70 y 0,85 (M1). El docente insiste en que la mejor alternativa es el software especializado.
- Factor de temperatura: P(T) = P_STC·[1 + γ·(T_cel − 25)]. La γ sale de la ficha técnica.

### 4.2 Relación DC/AC (M2 p.36–57)
- DC/AC = Σ Pdc STC por MPPT / Pac nominal.
- Guía:
  - clima cálido (Barranquilla) ≈ 1,4;
  - clima frío (Bogotá) ≈ 1,2;
  - los fabricantes admiten de 1,2 a 1,4.
- Una relación alta trae clipping y estrés térmico; el clipping se revisa en el informe de pérdidas.
- El script alerta fuera del rango 1,2–1,4 y lanza una alerta fuerte por encima de 1,5.

### 4.3 Strings (M2 p.80–94) `[forma estándar]`
- Todo lo que va al mismo MPPT lleva el mismo módulo, el mismo N en serie y la misma orientación. Se prefiere la conexión en serie.
- **N_serie,máx = floor(V_máx,inv / Voc(T_mín))**, con Voc(T) = Voc,STC·[1 + β_Voc·(T − 25)] y T_mín = la mínima histórica del sitio.
- **N_serie,mín = ceil(V_MPPT,mín / Vmp(T_cel,máx))**. El Lote 10 usó T_cel = 69 °C.
- **Strings por MPPT ≤ floor(I_máx,MPPT / Imp)**, y además la Isc del arreglo ≤ la Isc admisible.
- Qué pasa al salirse de los límites:
  - tensión > máx → falla o derrateo;
  - < mín MPPT → no genera;
  - corriente > máx → clipping;
  - > Isc admisible → daño.

### 4.4 Punto de conexión
- La potencia AC no supera la capacidad del tablero, la acometida o la subestación, ni el nivel de cortocircuito.
- **CREG 174/2021**: ≤ 100 kW con ≤ 50 % de excedentes → sin estudio de conexión, pero un ingeniero electricista valida la
  capacidad y el cortocircuito.
- Por encima de eso → estudio de conexión (DIgSILENT, ETAP o NEPLAN).
- Las reglas de excedentes cambiaron en 2025–2026 (ver `normativa-vigente.md`).

## 5. Pérdidas típicas y PR (M1 p.56–61; IEC 61724-1:2021)
| Pérdida | Rango típico |
|---|---|
| IAM y reflexión | 1–3 % |
| Sombreado | 0–5 % (hasta 10 % con mal diseño) |
| Suciedad | 2–6 % |
| Temperatura | 4–8 % |
| Mismatch y tolerancias | 1–3 % |
| Cableado CC | 1–3 % |
| Inversor | 2–5 % |
| Cableado CA y transformador | 1–3 % |
| Indisponibilidad | 1–3 % |

- PR > 80 % es excelente; > 78 % es aceptable; **< 70 % indica deficiencias** de diseño, construcción u O&M.
- **Garantía de PR en un EPC.**
  - Se mide en ventanas de 7 días, dos veces al año.
  - Se cumple si PR_medido ≥ 0,95·PR_garantizado.
  - Penalidad máxima: 5 % del contrato en los años 1 y 2 (ejemplo del curso, N4: **SUPUESTO**, cada EPC la negocia).

## 6. Incertidumbre: P50 y P90
- **P90 = P50·(1 − 1,2816·σ)**, con σ = √Σu² (variabilidad del clima, modelo, inversor, suciedad, degradación).
- **En el resumen ejecutivo:** "9 de cada 10 años se producirán al menos X MWh". En el anexo: P50, P90 y σ.

## 7. Caso de prueba: Lote 10, Mérida, Santander (N5, verificado con el script)
- 4 032 × 670 Wp = **2 701,4 kWp**; 6 × 330 kVA → DC/AC = 1,364.
- 4 284,8 MWh/año → **1 586 kWh/kWp·año**; PR = **0,862** con H plano ≈ 1 839 kWh/m².
- P90 = **4 115 MWh** con σ = 3,1 %.
- Mayores pérdidas: temperatura −6,4 %; LID −1,1 %; inversor −1,3 %.
- Supuestos: suciedad 1 %; Uc = 20 W/m²K; degradación 0,4 %/año.
- Lección de un entregable del curso: bien dimensionado, pero **"no supieron vender la idea"**. Hace falta un resumen ejecutivo con la decisión,
  la cifra clave en kWh y en $, y el riesgo principal.

## 8. Ejemplo de Manizales (M2 p.116–117)
- Cubierta a dos aguas: 480 + 520 módulos de 620 Wp = 620 kWp.
- 5 inversores de 100 kW (10 MPPT × 1 string de 20) → **DC/AC = 1,24**.

## 9. Datos de sitio vistos en el curso (N5, reverificar en el atlas antes de usarlos)
- Tauramena, Casanare: GHI ≈ 5,18 kWh/m²·día; Yopal ≈ 1 700 kWh/m²·año.
- Viento de 2,5–4,5 m/s, así que la eólica no es competitiva allí.
