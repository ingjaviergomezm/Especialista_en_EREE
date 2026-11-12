# Método: línea base, IDEn, línea meta, CUSUM y M&V

**Fuentes:**
- Curso 03: guías U1, U3 y U4 (N2).
- Mi Act 4: la lógica de la regresión la validó la profesora. Lo demás de esa entrega se usa solo como lección.
- Alineado con la **ISO 50006:2023**, que está vigente y reemplazó a la de 2014.

**Script:** `scripts/linea_base.py`.

## 1. Indicadores de desempeño (IDEn)
| Indicador | Definición | Ejemplo verificado |
|---|---|---|
| CEE (consumo específico) | energía / unidad producida o de servicio | Cemento: 1 000 000 kWh / 500 t = **2 000 kWh/t**; meta −15 % → **1 700 kWh/t** |
| IEE (índice de eficiencia) | energía usada / energía óptima; > 1 = sobreconsumo | Aire acondicionado: 12 000/9 500 = **1,263** (26 % de sobreconsumo) |
| IDEn por regresión | E = m·P + b | ver §2 |
| IDEn de costo | $/unidad | **Siempre aparte** del IDEn físico: la tarifa cambia aunque el desempeño no cambie |

**Reglas para los IDEn:**
- Si hay varios energéticos, todos se pasan a kWh con el factor declarado.
- Si hay varios productos, se usa la **producción equivalente** con un factor declarado (en A4 se usó "salchipapa equivalente").
- **El cociente simple engaña cuando hay consumo base fijo.** Si la producción baja, el kWh/unidad sube sin que haya
  ineficiencia. Cuando la regresión tiene un intercepto b significativo, el IDEn es la regresión.

## 2. Línea base energética (LBEn) por regresión
- **E = m·P + b.**
  - E = kWh del periodo.
  - P = la variable relevante: producción, grados-día, ocupación o huéspedes-noche.
  - b = consumo fijo; m = consumo por unidad.
- **Requisitos que el script verifica o advierte:**
  - **≥ 12 periodos** sin cambios estructurales. Con menos, el script advierte: no se capta la estacionalidad;
  - una variable que **varía**. Si P es constante, la regresión es indefinida y el script da error;
  - **R², n y el rango de validez [P_mín, P_máx] declarados.** El script bloquea la extrapolación salvo que se pida explícitamente;
  - **atípicos** (> 2σ) señalados para explicarlos con el cliente. **No se borran en silencio.**
- **Calidad mínima:** el script advierte si R² < 0,75 (umbral SUPUESTO de práctica común; la ISO 50006 no fija uno)
  o si la pendiente es ≤ 0, y en esos casos **no calcula línea meta**. Se busca otra variable o se usa otro IDEn.
- **Periodo de reporte fuera del rango de la LB:** el CLI marca con * cada mes que extrapola; se declara o se ajusta la LB.
- **Con menos de 12 periodos: LBEn PROVISIONAL.** Se informa como tal, sin línea meta (el script la bloquea) y se
  recalcula al completar 12. La línea meta además exige ≥ 6 periodos bajo la LB.
- **Periodos que no coinciden** (p. ej. 8 meses de energía y 6 de producción): la regresión usa solo los meses que tienen
  ambas variables; el balance usa todo el periodo facturado, con los días de uso de los equipos del mismo periodo.
- **Una LBEn por energético** (electricidad, GLP, gas…) y, si sirve para la meta, una total en kWh equivalentes,
  declarando el factor de conversión.
- **Criterios de ajuste de la LB:** cambio de instalaciones, de producto, de horario o de alcance. Si ocurren, se declaran.
- Ejemplo: E = 1,6876·P + 127,13 kWh/mes (A4). Las pruebas del script recuperan esos coeficientes.

## 3. Seguimiento
- **CUSUM = Σ(E_real − E_modelo)**, acumulado periodo a periodo (SUPUESTO estándar, B-GE2).
  - Pendiente negativa: ahorro. Pendiente positiva: deterioro.
  - Un cambio de pendiente marca el periodo en que cambió el desempeño.
- **Ahorro % = (E_modelo − E_real)/E_modelo.** Positivo = ahorro. En A4 el signo quedó invertido (lección L3).
- Lección L2: en A4 el CUSUM se calculó como "127,13/H²", que no tiene sentido.

## 4. Línea meta
- Es la misma regresión, pero solo con los periodos **por debajo** de la LB. Representa lo que la planta **ya demostró** que
  puede lograr con buenas prácticas y sin inversión (SUPUESTO estándar, B-GE1).
- **Debe quedar por debajo de la LB en todo el rango de P.** El script lo verifica y da error si no se cumple.
  - En A4, la meta 1,7598·P + 136,94 quedó **por encima** de la LB, y eso contradice su definición.
- Si hay menos de 3 periodos bajo la LB, no se calcula. La meta se declara como un % de la LB, justificado.
- **Potencial de buenas prácticas** = Σ (LB − meta) en el periodo. Son ahorros de gestión, sin inversión.

## 5. Objetivos y metas (ISO 50001 6.2): SMART y trazables
- Cada meta tiene:
  - indicador;
  - valor de la LB;
  - valor meta;
  - fecha;
  - responsable;
  - acción.
- **Trazabilidad:** meta → USE → IDEn → acción → política energética. Si falta la política, es una brecha de primer orden (lección de Act 3).
- Nada de "ejecución inmediata" (lección de Act 4): el plazo va en semanas o meses.

## 6. Medición y verificación (M&V)
- La ISO 50015:2014 está vigente. El material solo la menciona (B-GE3).
- **SUPUESTO estándar con cita:** opciones IPMVP.
  - A: aislamiento con medición de parámetros clave.
  - B: aislamiento con medición completa.
  - C: toda la instalación por regresión, que es lo que hace este script.
  - D: simulación calibrada.
- El ahorro se reporta como LB ajustada − real, con la incertidumbre declarada.
- **Para contratos de desempeño (ESCO)** se remite a un profesional en M&V: la skill da el método, no certifica.

## 7. Cómo se presenta
- **Resumen ejecutivo**, por ejemplo: "Con la misma producción, la planta gastó 4 200 kWh menos de lo esperado en 6 meses
  (≈ $3,8 M). Hubo 5 de 6 meses por debajo de la línea base."
- **Anexo:** la ecuación, R², n, el rango, los atípicos y el gráfico CUSUM.
