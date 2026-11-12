# Entrevista de encargo — gestion-energetica (Fase 0)

Cómo usar este banco:
- Pregunta en **bloques de 4–5**, en el orden A → F. Confirma lo que el usuario ya dijo en lugar de preguntarlo de nuevo.
- Si una respuesta es "no sé", anótala como `[POR CONFIRMAR EN CAMPO]`.
- El *por qué* entre paréntesis sirve para explicar la pregunta si el usuario lo pide.

## Bloque A — La decisión
1. ¿Qué se busca: bajar la factura, cumplir una obligación (por ejemplo el PGEE de la Ley 2407 en una entidad pública),
   preparar ISO 50001 o justificar una inversión puntual?
   *(cada objetivo pide un entregable distinto)*
2. ¿Quién decide y quién va a leer el resultado? (Gerencia, mantenimiento, comité energético, entidad.)
3. Nivel del estudio: revisión preliminar (con facturas), auditoría con recorrido y mediciones, o diagnóstico y plan del SGE.
4. Criterio de éxito con números. Ejemplos: "−8 % de kWh por unidad producida en 12 meses frente a la línea base";
   "medidas con payback < 3 años".
   *(la línea meta y la verificación posterior dependen de esto)*

## Bloque B — La instalación
5. Tipo de instalación y proceso: planta, hotel, hospital, edificio de oficinas, restaurante, entidad. Turnos y horario.
6. Sedes y áreas incluidas; sistemas excluidos del alcance.
7. ¿Qué energéticos usan (electricidad, gas natural, GLP, diésel, carbón, biomasa) y para qué uso final?
8. ¿Hay medición por áreas (submedidores) o solo la frontera de facturación?

## Bloque C — Datos
9. ¿Hay al menos 12 meses de facturas por energético (kWh o m³, $, demanda máxima, reactiva)? Lo ideal son 24–36 meses.
   *(la línea base se calcula con datos mensuales; con pocos puntos la regresión no es confiable)*
10. ¿Qué variable explica el consumo y está registrada mes a mes? Ejemplos: toneladas, unidades, huéspedes por noche,
    grados-día, m², ocupación.
    *(es la "P" de la regresión E = m·P + b)*
11. ¿Hay inventario de equipos con potencia, horas de uso y antigüedad? ¿Hay datos de placa de motores, calderas y compresores?
12. ¿Han hecho mediciones con analizador de redes o tienen estudios anteriores? *(esta skill no instruye la
    intervención de tableros; las mediciones las hace personal calificado)*
13. Poder calorífico y densidad del gas natural; para GLP, diésel o carbón: unidad de compra (kg, gal, t) y PCI de la
    ficha técnica del distribuidor. ¿Están en la factura o los da el proveedor?
    *(no se toman de ejercicios académicos)*

## Bloque D — Dinero
14. Tarifa de cada energético ($/kWh, $/m³) y su mes; ¿le cobran energía reactiva?
15. Tasa de descuento o criterio de inversión del cliente; presupuesto disponible.
16. ¿El cliente declara renta? ¿Le interesa el incentivo de gestión eficiente de la Ley 2099 (certificación UPME)?

## Bloque E — Gestión
17. ¿Existe una política energética, un responsable o gestor energético, un comité, o indicadores que ya se sigan?
18. ¿Hay medidas ya implementadas o en curso? *(para no contar dos veces un ahorro)*

## Bloque F — Entregable
19. Formato: informe de auditoría (estructura ISO 50002-1), Excel con la línea base, presentación a gerencia, plan de
    acción. Extensión máxima.
20. Plazo y revisiones intermedias.

---

## Plantilla de salida — Ficha de Encargo
```
FICHA DE ENCARGO — gestion-energetica    Fecha: AAAA-MM-DD   Versión: 1
Objetivo / decisión:
Destinatario:
Nivel: revisión preliminar | auditoría | diagnóstico y plan del SGE
Criterio de éxito (operativo):
Instalación: tipo · sedes · turnos
Energéticos y usos finales:
Datos: facturas (meses, energéticos) · variable relevante · inventario · mediciones
Tarifas y mes:
Incluido:                       Excluido:
Entregables y formato:          Extensión:
Plazo:
Datos pendientes [POR CONFIRMAR EN CAMPO]:
→ ¿Aprobado? (sí / ajustes)
```
