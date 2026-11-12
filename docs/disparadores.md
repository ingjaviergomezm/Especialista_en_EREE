# Verificación de disparadores (v0.9, 2026-11-12)

**Método:**
- Se leyeron 10 peticiones realistas contra las `description` de las 3 skills nuevas y contra las skills ya instaladas que podrían chocar: `creador-memorias-calculo`, `instructivo-ocensa`, `creador-instructivos-ocensa`, `evaluar-estrategia-trading`, `data:*`, `xlsx`.
- Es un juicio sobre el texto de las descripciones, no una corrida automática del optimizador. Esa corrida se puede hacer en el piloto si aparecen fallos reales.

## Resultado por petición

| # | Petición | Skill esperada | Resultado | Riesgo de choque |
|---|---|---|---|---|
| 1 | "¿Cuántos paneles necesito para 300 kWh al mes en Villavicencio?" | proyectos-er (modo rápido) | ✅ "cuántos paneles necesita" | Ninguno |
| 2 | "Hazme la prefactibilidad de una PCH de 2 MW en Caldas" | proyectos-er | ✅ "PCH" y "prefactibilidad" | Ninguno |
| 3 | "¿En cuántos años se paga un sistema solar de 50 kWp para una bodega?" | proyectos-er | ✅ "en cuánto se paga" | `evaluar-estrategia-trading` es poco probable: no hay operaciones ni EA |
| 4 | "El hotel gasta muchísima energía, te paso 12 facturas" | gestion-energetica | ✅ "hotel", "gasta mucha energía" y "facturas" | Bajo: proyectos-er también menciona facturas, pero para dimensionar |
| 5 | "Necesito armar la línea base ISO 50001 de la planta" | gestion-energetica | ✅ | Ninguno |
| 6 | "Revisa el factor de potencia, nos están cobrando reactiva" | gestion-energetica | ⚠️ mercado-electrico-co también dice "energía reactiva" | **MEDIO**. Se resuelve abajo |
| 7 | "¿Por qué subió la tarifa de energía este año?" | mercado-electrico-co | ✅ literal en la descripción | Bajo: gestion-energetica dice "bajar la factura" |
| 8 | "¿Me conviene pasarme a usuario no regulado? Consumo 70 MWh/mes" | mercado-electrico-co | ✅ | Ninguno |
| 9 | "¿Quién marcó el precio de bolsa a las 7 p.m. ayer?" | mercado-electrico-co | ✅ | Ninguno |
| 10 (ambigua) | "¿Cuánto me pagan por los excedentes de mis paneles?" | mercado-electrico-co para la regla y el precio; proyectos-er si es parte de evaluar el proyecto | ⚠️ ambas lo mencionan | **BAJO**. proyectos-er ya dice que llama a mercado-electrico-co para el precio de la energía |

## Choques con skills existentes

- **`creador-memorias-calculo`** (OCENSA): sus disparadores son costear contratos, AIU y HECMO. "Memoria de cálculo" de un sistema FV podría tocarla. proyectos-er excluye "memorias firmadas".
  - **Riesgo bajo.** Una petición del tipo "memoria de cálculo del sistema FV" cae en proyectos-er por "FV", y de todos modos se declara el nivel de estudio.
- **`instructivo-ocensa` / `creador-instructivos-ocensa`:** son procedimientos operativos. No hay solape.
- **`evaluar-estrategia-trading`:** analiza operaciones financieras. mercado-electrico-co excluye "asesoría de inversión financiera". No hay solape.
- **`xlsx`:** si el usuario entrega facturas en Excel, puede activarse junto con gestion-energetica. Es compatible: xlsx lee y la skill analiza.

## Límite de longitud
Las tres `description` medían entre 1 369 y 1 556 caracteres. claude.ai acepta como máximo 1 024. Se reescribieron (897, 949 y 998) conservando todos los disparadores de la tabla.

## Corrección aplicada
- **#6:** la reactiva en la factura de una instalación es una medida de ahorro (compensación), así que va a gestion-energetica. En mercado-electrico-co solo entra la regla regulatoria del cobro.
  - Se ajustó la descripción de mercado-electrico-co: "energía reactiva (solo la regla CREG de cobro; la compensación en planta → gestion-energetica)".
