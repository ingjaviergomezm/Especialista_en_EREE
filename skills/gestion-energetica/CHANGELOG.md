# CHANGELOG — gestion-energetica

## v0.9 — 2026-11-12 (versión de instalación, antes del piloto)
- Primera versión construida a partir de: Cursos 03 y 04 de EVEREE (UAM); vigencia normativa consultada al corte 2026-11.
- Flujo man-in-the-loop de fases 0–5 con compuertas ⛔, modo rápido de "cálculo puntual" y reglas inviolables.
- Scripts verificados con pytest contra los ejercicios del curso, cálculos a mano y casos borde: balance_energetico.py, linea_base.py, medidas_ahorro.py, evaluacion_financiera.py (copia).
- Referencias con fuente y nivel (N1–N6); normativa con `fecha_corte: 2026-11`.
- Verificación (2026-11-12): simulación con el humano en el ciclo (2 casos) y red team independiente; todas sus fallas
  se corrigieron con prueba (detalle en `_trabajo/verificacion_v09.md`). Descripciones ≤ 1 024 caracteres; regla
  común de traspaso entre skills y mínimo innegociable de compuertas.
- Pendiente para v1.0: piloto con un caso real de Javier y ajustes por sus observaciones.

## Cómo registrar cambios
Una entrada por versión: fecha, qué cambió, por qué (norma nueva, error encontrado, observación del piloto) y qué pruebas se corrieron.
