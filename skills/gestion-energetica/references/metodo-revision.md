# Método — revisión y auditoría energética

**Fuentes:**
- Curso 03 *Gestión de la Energía*: guías U1 y U2 (N2), plantilla de informe de auditoría (N3) y diapositivas C1 (N4).
- Act 1 (N5); Act 2 (N6: solo lecciones).
- La estructura del informe se alinea con la **ISO 50002-1:2025** (vigente; reemplazó a la ISO 50002:2014) `[contenido de pago: confirmar numerales con el texto]`.

**Scripts:** `scripts/balance_energetico.py`, `scripts/linea_base.py` y `scripts/medidas_ahorro.py`.

## 0. Dos cosas distintas (preguntarlo en la Fase 0)
- **Auditoría energética** (ISO 50002-1): mide consumos y busca ahorros.
- **Auditoría interna del SGE** (ISO 50001 §9.2): verifica que el sistema cumpla los requisitos. Ver `iso50001.md`.

## 1. Iniciación
- Principios del auditor: imparcialidad, objetividad y confidencialidad.
- Se acuerdan:
  - objetivos;
  - alcance (límites físicos y organizativos, energéticos incluidos);
  - equipo;
  - **reunión de apertura documentada**.
- **Nivel:**
  1. recorrido y facturas;
  2. mediciones por sistema;
  3. detallada, con evaluación de inversiones.
- **Información preliminar:**
  - **12 a 36 meses** de facturas por energético (mínimo 12 para captar la estacionalidad);
  - producción del mismo periodo;
  - unifilares y planos;
  - inventario de equipos y horarios.

## 2. Preparación
- **IDEn preliminares:** kWh/unidad, kWh/m², kWh/empleado. Comparar con referentes **solo si hay fuente con año** (B-GE4).
- **Pareto 20/80** para ubicar los usos significativos.
  - Dato de orientación del curso (N4, sin fuente primaria ni año: **SUPUESTO de orientación, no se cita como dato**):
    ≈ 69–70 % de la electricidad industrial va a **motores**, que casi siempre son USE.
  - Igual de orientativos (N4, SUPUESTO): HVAC ≈ 40 % en edificios comerciales; ACS ≈ 20 % en residencial. Para comparar
    se usa el BECO de la UPME o un referente con fuente y año (B-GE4).
- **Plan de mediciones:** analizador o registrador, puntos, duración y periodo representativo, más un **análisis de seguridad** antes de
  intervenir tableros. La skill no instruye esa intervención: la hace personal calificado (B-GE9).

## 3. Ejecución: balance con prueba de cierre (lo que hace `balance_energetico.py`)
1. **Todo a kWh** con el factor declarado:
   - electricidad: directo;
   - gas: m³ × PCI (MJ/m³)/3,6, con datos del comercializador;
   - GLP, diésel y biomasa: cantidad × PCI/3,6.
2. **Consumo por equipo** = kW × h/día × días × factor de carga. La potencia de placa no es el consumo: el factor de carga se mide o
   se declara como SUPUESTO `[POR CONFIRMAR EN CAMPO]`.
3. **Cierre:** la suma por energético contra la factura, dentro de una tolerancia declarada (por defecto ±10 %). Si no cierra, se
   revisan las horas, el factor de carga o los equipos faltantes **antes** de presentar porcentajes.
4. **Desagregación** por energético, por área y por equipo. Las tres suman lo mismo, por construcción.
5. **Energía y costo en columnas separadas.** Lección de un entregable del curso: el gas era más del 56 % de la energía y se reportó 29 %,
   probablemente por confundir energía con costo.
6. El **Sankey** se genera desde la misma tabla (`flujos_sankey`), así que suma por construcción.
7. **USE:** los equipos que acumulan el umbral de Pareto (80 %, declarado) más los de alto potencial de mejora.
   - Se **declaran formalmente**, con su criterio (lección de Act 3).
   - Justificación como en Act 1: potencia, horas de uso y kWh/día, horario pico y función.
8. **Ajuste de la LBEn** con lo medido. Ejemplo del curso: de 5 000 a 4 000 MWh/año (−20 %), de 50 a 40 kWh/unidad.
9. **Tabla de oportunidades.** Cada medida lleva inversión, kWh/año, $/año, payback, VPN, vida útil, prioridad y USE asociado.
   Ver `metodo-medidas.md`.

## 4. Informe de auditoría (estructura)
1. Portada e índice.
2. **Resumen ejecutivo** (1–2 páginas). Ejemplo del curso: "18 % de ahorro, $50 000/año, inversión de $120 000, retorno ≈ 2,4 años"
   (verificado: 120 000/50 000 = 2,4).
3. Antecedentes y alcance.
4. Equipo auditor, con **declaración de independencia**.
5. Metodología y nivel.
6. Caracterización energética:
   - balance y Sankey;
   - IDEn;
   - USE;
   - LBEn.
7. Evaluación del SGE, si aplica (`iso50001.md`).
8. Hallazgos con la estructura obligatoria de `informe-tecnico.md` §2.
9. Recomendaciones priorizadas, con ROI.
10. Conclusiones (madurez del SGE en lenguaje llano).
11. Anexos: datos, mediciones, supuestos, trazabilidad y normas con fecha.
12. Acta de la reunión de cierre.

## 5. Lecciones de un entregable del curso 03 (Act 2), convertidas en reglas
| Qué pasó | Regla |
|---|---|
| La cocina era ≈ 73,5 % del consumo y se reportó 44,8 % | El cierre lo calcula el script |
| El gas se reportó como 29 % cuando era más del 56 % | Energía y costo se reportan por separado |
| Los % por equipo no cuadraban y el Sankey no sumaba | Sankey generado desde la tabla |
| "Se usó IA sin verificar" | Ninguna cifra sale de memoria: todas salen del script, con trazabilidad |
