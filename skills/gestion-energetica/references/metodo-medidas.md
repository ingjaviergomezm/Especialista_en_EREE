# Método — medidas de ahorro por sistema

**Fuentes:** curso 03, guía U3 (N2) y diapositivas C1 (N4). Las formas estándar se marcan SUPUESTO.

**Script:** `scripts/medidas_ahorro.py`, que usa `evaluacion_financiera.py` para el VPN y la TIR.

**Regla general (lección L4).** Cada medida lleva estos datos:
- inversión;
- ahorro en kWh/año y en $/año;
- payback;
- VPN y TIR;
- vida útil;
- USE asociado;
- responsable y plazo con cifra.

Las medidas se priorizan por **VPN** y por su potencial en los USE, no por el producto más vendido. El payback se reporta,
pero no decide solo.

**Dos vías de ahorro** (C1):
- **Gestión y buenas prácticas:** bajo costo; es la base de la línea meta.
- **Inversión en tecnología.**

## 1. Iluminación
- **Ahorro** = n·(W_actual − W_nuevo)·h/1000, más los sensores como fracción del consumo nuevo.
- **Ejemplo del curso (es prueba del script):** 100 luminarias de 80 W → LED de 35 W, 3 000 h/año.
  - Ahorro: 13 500 kWh/año, que a 0,15 €/kWh son 2 025 €/año.
  - Con sensores (−20 %): 15 600 kWh/año.
- **Restricción:** se respeta el nivel de lux del **RETILAP compilado 2026**. La medida se valida con lux medidos y nunca se ahorra
  dejando el sitio subiluminado.

## 2. Factor de potencia y reactiva
- **FP = kW/kVA.**
- **Compensación:** Qc = P·(tan φ1 − tan φ2). Ejemplo: 100 kW, de FP 0,80 a 0,95 → 42,1 kVAr.
- **Cobro de reactiva:** CREG 015/2018, cap. 12 (mod. 199/2019 y 195/2020).
  - FP inductivo mínimo de 0,9.
  - El script estima los kVArh en exceso sobre el 50 % de la energía activa `[verificar el límite vigente]`.
  - **Factor M:** 1 durante los primeros 12 meses con exceso (> 10 días/mes); luego +1 por mes hasta 6; vuelve a 1 tras 3 meses sin exceso `[verificar en vivo: CREG 015/2018 cap. 12 y CREG 101 035/2024]`.
  - **El exceso se evalúa HORA A HORA** (`reactiva_en_exceso_horaria`): con totales mensuales se diluye y se subestima.
    La **reactiva capacitiva** también se cobra: un banco fijo sobredimensionado (FP objetivo 1,0) la genera en baja carga.
  - El valor en $ se toma de la **factura**.
- Otras pérdidas de distribución:
  - transformadores (en vacío y en carga): pedir los datos de placa y el protocolo de pruebas;
  - conductores: I²R.

## 3. Motores
- **Ahorro** = P_eje·h·carga·(1/η_actual − 1/η_nueva). Es la forma estándar.
- Las eficiencias se toman de la placa o del catálogo (IE2/IE3/IE4).
- **Variadores:** solo en cargas de par variable (bombas y ventiladores). El ahorro depende del perfil de caudal, así que **se mide o se
  simula**; no se asume.

## 4. Aire comprimido
- Solo el **10–15 %** de la energía eléctrica llega como trabajo útil.
- **Fugas:** kW del compresor × fracción de fugas × horas. La fracción se mide con una prueba en vacío o con ultrasonido.
- **Reducir la presión:** ≈ **7 %** por bar (cifra del material). Es un SUPUESTO con sensibilidad que se confirma con el fabricante.
- Eliminar los usos indebidos (limpieza con aire comprimido).

## 5. Térmica (calderas y vapor)
- **Eficiencia** de la caldera por el método directo o indirecto. El PCI y la densidad del combustible los da el comercializador.
  - El ejercicio C1 del curso traía una densidad del gas de 16,38 kg/m³, que es implausible (≈ 0,7–0,8). El script la rechaza.
- **Medidas:**
  - precalentar el agua de alimentación (recuperación de calor);
  - aislar;
  - recuperar condensados;
  - ajustar la combustión (exceso de aire).
- **Horas de operación:** factor de **utilización** (no el factor de potencia) × 8 760 (por ejemplo, 0,8 × 8 760 = 7 008 h).

## 6. Cogeneración (CHP)
- Eficiencia global de ≈ 56 % en generación separada frente a 75–87 % en CHP.
- El ahorro de energía primaria = E_útil/η_separada − E_útil/η_CHP.
- Exige la demanda simultánea de calor y electricidad, que se verifica con el perfil.

## 7. HVAC y edificios
- HVAC ≈ 40 % en el sector comercial.
- **Medidas:** setpoints, horarios, BMS, envolvente, equipos de alta eficiencia (COP/EER) y mantenimiento.
- El ahorro se estima con el inventario y las horas, o con simulación. Se valida con la LBEn por grados-día.

## 8. Incentivos
- Las acciones de **gestión eficiente de la energía** pueden acceder a los beneficios de la Ley 1715 (mod. Ley 2099/2021) con el
  **certificado UPME** (Res. 563/2026).
- En el flujo de caja van como escenario aparte (ver `normativa-vigente.md`).
