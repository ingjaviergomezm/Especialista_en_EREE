# Método — otras fuentes (modelos 0D) y selección de tecnología

**Fuentes:**
- curso 05, diapositivas EOL, HID, BIO, GEO, OCE, INT (N4);
- curso 06, M1 p.70–95 (N2);
- curso 08, TEN (N3).

**Script:** `scripts/recursos_0d.py`.

**Alcance:** perfil y prefactibilidad. El diseño de dispositivos (FEM/CFD) queda fuera. La oceánica queda fuera; la geotermia solo de perfil.

## 0. Formulación (flujo enseñado en el curso 05, Act 2 → 4 → 6)
1. **Necesidad**: demanda en kWh/mes con su fuente.
2. **Recurso**: cuadro con los 5 recursos (solar, eólico, hídrico, biomasa, geotérmico) **cuantificados** y con su atlas de
   origen (lección P6: nunca solo "disponible").
3. **Selección**: preselección con capacidad y eficiencia → matriz de decisión → diseño conceptual (tecnología,
   diagrama de montaje, ubicación).
4. **Costos y viabilidad**: ver `metodo-financiero.md`.

### Fuentes de recurso recomendadas por el curso
Siempre se consultan en vivo y con fecha.

| Recurso | Fuente |
|---|---|
| Solar | Global Solar Atlas; Atlas interactivo IDEAM |
| Eólico | Global Wind Atlas 3.0 (DTU) |
| Biomasa | UPME — Atlas del potencial energético de la biomasa residual |
| Hídrico | UPME — Atlas hidroenergético; DHIME-IDEAM (series de caudal) |
| Geotérmico | SGC — potencial geotérmico preliminar (2020); ANH |

## 1. Indicadores generales
- **Factor de planta** = E real / (P nominal × horas). Ejemplo: 648 000 MWh / (1 000 MW × 720 h) = 0,90.
- **Horas equivalentes** = E anual / P. Ejemplo: 108 GWh / 20 MW = 5 400 h.
- **Prueba de cierre**: E = P·h·FP con un FP plausible para la tecnología.

## 2. Eólica
- **P = ½·ρ·A·v³·Cp**, con el límite de Betz Cp ≤ 16/27 ≈ 0,593.
- **Perfil vertical:** V = V₀·(H/H₀)^β. Valores de β:
  - liso: 0,10–0,13;
  - rural: 0,13–0,20;
  - bosque o barrio: 0,20–0,27;
  - ciudad: 0,27–0,40.
- **Energía anual:** E = T·∫P(v)·f(v)dv.
  - f es la distribución de Weibull del sitio (k, c).
  - P(v) es la curva de potencia del fabricante, medida según IEC 61400-12-1.
- **Corrección por densidad.** La curva vale para ρ = 1,225 kg/m³. Para leerla, la velocidad equivalente es v_std = v_sitio·(ρ_sitio/ρ_std)^(1/3).
  - El exponente pasa de 1/3 a 2/3 entre 7–8 y 12–13 m/s (RENAC).
  - ρ por altitud: atmósfera ISA (SUPUESTO). Si hay presión y temperatura del sitio, se usan esas. En Manizales (2 150 m), ρ ≈ 0,99.
- **Parque:** P = Σ n·P·φ(estela)·ξ(disponibilidad)·η(pérdidas).
- Con velocidades medias de 2,5–4,5 m/s (caso Casanare), la eólica no es competitiva.

## 3. Hidráulica (PCH y micro)
- **P = ρ·g·Q·H·η**, con η global ≈ 0,80–0,85 (turbina × multiplicador × generador × transformador).
- **Series:** se necesitan **≥ 20 años de caudales**. Se usa la curva de duración (Q30, Q50, Q90).
  - Para pasada, Q_d entre Q30 y Q50.
  - Forma del curso: **Q_d = f·Q_m − Q_e**, con f = 0,4–0,7. El Q_e lo aprueba la **autoridad ambiental**.
- **Mínimo técnico** (como fracción del caudal de diseño Q_d): Pelton 10 %, Kaplan 25 %, Francis 40 %.
- **Clasificación técnica del curso:** pico < 1 kW; micro 1–100 kW; **PCH 100 kW–10 MW**; mediana 10–100 MW; grande > 100 MW.
  **No es la regulatoria:** en Colombia las "plantas menores" son < 20 MW (CREG 086/1996 y modificaciones)
  `[verificar vigencia]`; ese umbral define si la planta se despacha centralmente y cómo comercializa.
- **Escorrentía de una cuenca pequeña:** V = A·P·C. Ejemplo del curso (es una prueba del script): A = 2 km², P = 150 mm, C = 0,4 → 120 000 m³/año → Q = 0,0038 m³/s; con H = 132 m, P bruta ≈ 4,9 kW y útil ≈ 3,9 kW.
- **Impactos:** efecto barrera, régimen hidrológico, territorio y aspectos socioeconómicos.

## 4. Biomasa
- **Disponible:** B = A·Y·f_res·f_rec. Por ejemplo, f_res ≈ 0,25 en paja de cereal y f_rec = 0,5–0,8.
- **Rutas:**
  - combustión (rendimiento ≈ 80 % con biomasa seca y ≈ 60 % con húmeda);
  - gasificación;
  - pirólisis;
  - digestión anaerobia (biogás + digestato).
- **Potencia eléctrica:** P = B·PCI·η_neta / horas.
  - **η_neta la da el fabricante.** En plantas pequeñas suele estar entre 15 y 30 %.
  - El rango 0,55–0,90 del curso no es la eficiencia del ciclo (B-ER11).
- **Factores críticos:** logística y humedad. Es renovable solo si el uso no supera la reposición.

## 5. Geotermia (solo PERFIL)
- Gradiente G = ΔT/Δz: 25–30 °C/km en promedio y 50–100 °C/km o más en zonas volcánicas.
- **Q = ṁ·cp·ΔT** y **P_el = Q·η_ciclo**, con η entre 0,10 y 0,20.
- Ejemplo del curso: 50 kg/s, 4,2 kJ/kg·K, de 160 a 60 °C → **21 MWt → 3,15 MWe** con η = 15 %.

## 6. Matriz de decisión (factores ponderados)
1. Los criterios y subcriterios llevan peso, y **los pesos suman 1**.
2. **La escala va orientada y declarada por criterio**, por ejemplo "5 = el menor costo" o "1 = el que menos reduce el CO₂".
3. **El total lo calcula el script.** Lección del curso 05: mi matriz tenía errores aritméticos (eólica 2,8, reportada como 2,5).
4. Se prueba la **sensibilidad de los pesos** (±10 %): ¿cambia el ganador? Si cambia, se dice.
5. Criterios típicos:
   - técnico: recurso, madurez, capacidad;
   - económico: CAPEX, LCOE;
   - ambiental: CO₂, biodiversidad;
   - social: empleo, aceptación, consulta previa;
   - regulatorio: incentivos, conexión.
