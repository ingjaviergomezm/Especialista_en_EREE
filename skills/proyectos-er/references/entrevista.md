# Entrevista de encargo — proyectos-er (Fase 0)

Cómo usar este banco:
- Pregunta en **bloques de 4–5**, en el orden A → F. No preguntes lo que el usuario ya dijo; confírmalo.
- Si una respuesta es "no sé", no la conviertas en supuesto todavía: anótala como `[POR CONFIRMAR EN CAMPO]` y en la
  Fase 1 se decide si se asume (con rango) o se consigue.
- Cada pregunta trae entre paréntesis **por qué importa**. Úsalo para explicarla si el usuario pregunta, no para leerla.

## Bloque A — La decisión (siempre primero)
1. ¿Qué decisión se quiere tomar con este estudio? (Ejemplos: invertir o no; elegir entre FV y diésel; presentar a una convocatoria.)
   *(define qué resultado sirve; sin esto se calcula de más o de menos)*
2. ¿Quién va a leer el resultado? (Cliente final, gerencia, junta de una comunidad, entidad financiadora o pública.)
   *(cambia el tono, el nivel de detalle y el formato)*
3. ¿Qué nivel de estudio se necesita: perfil (orden de magnitud), prefactibilidad o factibilidad?
   *(fija la precisión exigida y lo que queda fuera)*
4. ¿Cuál es el criterio de éxito, dicho con números? Por ejemplo: "viable si el VPN > 0 al 12 % y el payback < 7 años"
   o "cubrir el 60 % del consumo".
   *(sin una definición operativa, "viable" significa algo distinto para cada lector)*

## Bloque B — Sitio y red
5. Municipio, vereda o predio aproximado (sin coordenadas exactas si es confidencial). ¿Altitud aproximada?
   *(recurso solar o eólico y densidad del aire)*
6. ¿Hay conexión al SIN? ¿A qué distancia está la red y a qué tensión? ¿O es una zona no interconectada?
   *(conectado a red y aislado son métodos distintos; aislado es brecha B-ER2)*
7. Área disponible para el sistema: tipo (cubierta, suelo), m², orientación e inclinación de la cubierta, sombras
   (árboles, edificios, montañas) entre las 9 y las 15 h.
8. ¿El sitio está en territorio étnico o tiene resguardos o consejos comunitarios cerca?
   *(si la respuesta es sí, la consulta previa es ruta crítica del cronograma y riesgo de viabilidad)*

## Bloque C — Demanda y energía actual
9. ¿Hay 12 facturas de energía (kWh/mes, $/kWh, tipo de usuario, nivel de tensión, comercializador)? ¿Las comparte?
   *(la demanda y la tarifa reales valen más que cualquier promedio. Si solo hay $/mes: estrato, tarifa y consumo de
   subsistencia, porque el kWh ahorrado en estratos 1 a 3 vale la tarifa subsidiada)*
10. ¿Cómo es el perfil de uso: horario diurno o nocturno, fines de semana, estacionalidad, cargas grandes (bombas, frío)?
    *(autoconsumo vs. excedentes; los excedentes se pagan distinto)*
11. ¿Hay planes de ampliación o cambios de equipos en los próximos 5 años?
12. ¿Usan otra fuente de energía (diésel, gas, leña)? ¿Cuánto consumen y a qué costo?

## Bloque D — Dinero y propiedad
13. ¿Quién financia, quién es dueño del sistema, quién lo opera y quién recibe el ahorro o el ingreso?
    *(es la lección L1 del curso 01: un modelo comunitario con costos por familia quedó ambiguo)*
14. ¿Qué tasa de descuento o costo de capital usa el cliente? ¿Hay presupuesto máximo?
15. ¿El cliente declara renta y le serviría la deducción de la Ley 1715 (tope: 50 % de la renta líquida)? ¿Ya tiene
    certificación UPME en trámite?
16. ¿Quiere valorar la reducción de CO₂ en dinero (impuesto al carbono o bonos)? *(si la respuesta es sí, va como escenario aparte)*

## Bloque E — Restricciones y alcance
17. Tecnologías a evaluar o descartar de entrada. ¿Hay preferencia de equipos o proveedores?
18. Restricciones: estructurales (cubierta), ambientales, de permisos, del operador de red, de plazo.
19. ¿Qué queda fuera del alcance? Por ejemplo: diseño eléctrico de detalle, trámite de conexión, estudio de suelos.

## Bloque F — Entregable
20. Formato: informe (Word/PDF), Excel con el flujo de caja, presentación, memoria de cálculo. Extensión máxima.
    *(el formato y la extensión pactados se respetan: lecciones L2 y L3)*
21. Fecha de entrega y revisiones intermedias.

---

## Plantilla de salida — Ficha de Encargo (una página)
```
FICHA DE ENCARGO — proyectos-er          Fecha: AAAA-MM-DD   Versión: 1
Decisión a tomar:
Destinatario:
Nivel de estudio: perfil | prefactibilidad | factibilidad
Criterio de éxito (operativo):
Sitio: municipio · red (sí/no, distancia, tensión) · área · sombras
Territorio étnico: sí / no / por confirmar  → consulta previa: aplica / no aplica / por confirmar
Demanda: kWh/año (fuente) · perfil · tarifa $/kWh (fuente, mes)
Financiación y propiedad: quién paga / es dueño / opera / recibe el beneficio
Tecnologías a evaluar:
Incluido:                       Excluido:
Entregables y formato:          Extensión:
Plazo:
Datos pendientes [POR CONFIRMAR EN CAMPO]:
→ ¿Aprobado? (sí / ajustes)
```
