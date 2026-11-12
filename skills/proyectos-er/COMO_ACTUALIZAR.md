# Cómo actualizar proyectos-er

La skill envejece por tres vías: **normas**, **precios y datos de mercado** y **errores de método**. Revisión recomendada: **cada 6 meses** o cuando salga una norma que toque el tema.

## 1. Vigencia normativa (lo más frecuente)
1. Abrir `references/normativa-vigente.md` y anotar la `fecha_corte` actual.
2. Para cada norma de la tabla, consultar **solo la fuente oficial** de la columna URL (Senado, Función Pública, CREG, UPME, MinEnergía, DIAN, ICONTEC/ISO).
   Normas más sensibles de esta skill: incentivos tributarios (Ley 1715/2014 y modificaciones, Res. UPME 563/2026), CREG 174/2021 y modificaciones (excedentes), RETIE, impuesto al carbono/UVT, precios de módulos e inversores.
3. Por cada cambio: actualizar la fila (estado, qué cambia en el método, URL, fecha de consulta) y buscar con grep dónde se cita esa norma en `SKILL.md` y `references/` para corregir también ahí.
4. Lo que no se pueda confirmar en fuente oficial queda `[no confirmado]`; nunca se rellena por analogía.
5. Cambiar `fecha_corte` a AAAA-MM y registrar en `CHANGELOG.md`.

## 2. Datos y precios ilustrativos
Las cifras de mercado del material son fotos ilustrativas. No se "actualizan" en la skill: la skill las consulta en vivo en cada uso. Solo revisar que sigan marcadas como ilustrativas.

## 3. Errores de método o de scripts
1. Escribir primero la prueba que reproduce el error en `scripts/test_*.py`.
2. Corregir el script hasta que pase **toda** la suite:
   ```
   python -m pytest scripts -q
   ```
3. Si el script se comparte con otra skill (`evaluacion_financiera.py`, `normativa-vigente.md`, `informe-tecnico.md`), copiar la corrección a las otras skills y correr sus pruebas.

## 4. Brechas
Si en campo aparece un tema que la skill no cubre, agregarlo a `references/brechas.md` (qué falta, riesgo, fuente donde buscar). Cerrar una brecha exige fuente N1–N3.

## 5. Publicar
Las skills viven en el maestro `Misión_C137\ADN_Agente\Sistema_Antigravity_MASTER\skills\` y se ven en Claude por junction: editar en el maestro, nunca en `~\.claude\skills`. Regenerar el .zip si se usa en claude.ai.
