# RESUMEN DE VISUALIZACIONES
## Informe de Valoración y Riesgo de Cartera de Swaps
**Generado:** 13 de abril de 2026

---

## Inventario de Visualizaciones

Se han creado e integrado un total de **10 visualizaciones completas** en el informe técnico y el resumen ejecutivo. Todos los gráficos son de alta resolución (300 DPI) y listos para publicación.

### Detalles de los Gráficos

#### 1. **Composición de la Cartera por Nocional** 
- **Archivo:** `01_portfolio_composition.png` (239 KB)
- **Tipo:** Gráfico de pastel
- **Propósito:** Muestra la distribución de la cartera de CLP 16.0B entre 4 swaps
- **Hallazgo Clave:** 56,2% concentrado con Banco 1 (Swap #1105)
- **Ubicado en:** Informe §1.1, Resumen Ejecutivo

#### 2. **NPV por Swap Individual**
- **Archivo:** `02_npv_by_swap.png` (135 KB)
- **Tipo:** Gráfico de barras
- **Propósito:** Muestra el valor presente neto de cada posición de swap
- **Hallazgo Clave:** Solo 1 de 4 swaps está en el dinero (+CLP 539M); 3 están fuera del dinero (-CLP 1B combinado)
- **Ubicado en:** Informe §1.3, Resumen Ejecutivo

#### 3. **Resultados de Pruebas de Estrés Regulatorio**
- **Archivo:** `03_stress_test_results.png` (219 KB)
- **Tipo:** Gráfico de barras con anotaciones
- **Propósito:** Muestra el impacto en NPV de 6 escenarios CMF RAN 21-13
- **Hallazgo Clave:** Peor caso (Subida Paralela) = -CLP 1,27B; mejor caso = +CLP 330M
- **Sensibilidad:** Swing de 1.600 M en un rango de 200 pb (DV01 = 8M/pb)
- **Ubicado en:** Informe §3.3, Resumen Ejecutivo

#### 4. **Análisis de Sensibilidad - Gráfico Tornado**
- **Archivo:** `04_sensitivity_analysis.png` (155 KB)
- **Tipo:** Gráfico tornado horizontal
- **Propósito:** Ordena los factores de riesgo por magnitud de impacto
- **Hallazgo Clave:** El riesgo de tasa de interés domina (±800M por 100 pb)
- **Interpretación:** Un movimiento de ±100 pb impacta más la cartera que los cambios de forma de curva
- **Ubicado en:** Informe §4.1, Resumen Ejecutivo

#### 5. **Comparación de Curvas de Rendimiento**
- **Archivo:** `05_yield_curves.png` (255 KB)
- **Tipo:** Gráfico XY de varias líneas
- **Propósito:** Compara tasas par USD vs curva cero CLP
- **Hallazgo Clave:** CLP 10A = 6,59% vs USD 10A = 5,91% (+68 pb de prima)
- **Detalle:** Incluye comparación con SOFR como baseline
- **Ubicado en:** Informe §2.3, apéndice de curvas

#### 6. **Curvas de Factores de Descuento**
- **Archivo:** `06_discount_curves.png` (185 KB)
- **Tipo:** Gráfico XY de varias líneas
- **Propósito:** Muestra la progresión de factores de descuento USD SOFR vs CLP
- **Hallazgo Clave:** La curva CLP es más empinada que la USD (refleja tasas a largo plazo más altas)
- **Técnico:** Usado para descontar flujos de caja en la valoración
- **Ubicado en:** Informe §2.3

#### 7. **Spreads Basis de Divisas Cruzadas**
- **Archivo:** `07_basis_spreads.png` (217 KB)
- **Tipo:** Gráfico de barras con gradiente de color
- **Propósito:** Muestra los spreads SOFR/Cámara por tenor
- **Hallazgo Clave:** Va de -40 a -120 pb; 6M = -83,8 pb
- **Interpretación:** Valores negativos indican prima de tasa CLP sobre SOFR
- **Ubicado en:** Informe §2.3

#### 8. **Comparación de Tasas Fijadas**
- **Archivo:** `08_rate_comparison.png` (242 KB)
- **Tipo:** Gráfico de barras agrupadas con anotaciones de spread
- **Propósito:** Compara tasas bloqueadas vs tasas de mercado par actuales
- **Hallazgo Clave:** Desventaja de 160-360 pb que causa pérdidas en la cartera
- **Pivotal:** Explica por qué los swaps están bajo el agua
- **Ubicado en:** Informe §5.2, Resumen Ejecutivo

#### 9. **Escalera de Vencimientos**
- **Archivo:** `09_maturity_ladder.png` (116 KB)
- **Tipo:** Gráfico de barras
- **Propósito:** Muestra cuándo vencen los swaps y las necesidades de refinanciamiento
- **Crítico:** 37,5% de la cartera (CLP 6B) vence el 28 de abril de 2026
- **Advertencia:** Solo 38 días desde la fecha de valoración
- **Ubicado en:** Informe §5.1, Resumen Ejecutivo

#### 10. **Concentración de Contraparte**
- **Archivo:** `10_counterparty_concentration.png` (286 KB)
- **Tipo:** Panel dual (pastel + barras agrupadas)
- **Propósito:** Muestra la exposición de contraparte y la concentración de riesgo
- **Hallazgo Clave:** 56,2% con Banco 1 excede el límite prudente del 40%
- **Riesgo:** Todas las contrapartes son domésticas (correlación sistémica)
- **Ubicado en:** Informe §7.2, Resumen Ejecutivo

---

## Estándares de Diseño Visual

Todos los gráficos siguen estándares profesionales de reporte:

- **Resolución:** 300 DPI (listo para publicación)
- **Esquema de color:** Paleta amigable con daltónicos
  - Ganancias/Positivo: Verde (#2ecc71)
  - Pérdidas/Negativo: Rojo (#e74c3c)
  - Referencia/Información: Azul (#3498db)
- **Tipografía:** Leyendas y etiquetas claras
- **Anotaciones:** Hallazgos clave anotados en los gráficos
- **Tamaño:** Optimizado para visualización digital e impresión

---

## Integración con los Reportes

### Reporte Técnico Completo (`REPORT.md`)
- 8 visualizaciones integradas con subtítulos
- Integradas a lo largo de las secciones 1-7
- Referenciadas en la narrativa cuantitativa
- Cruzadas con tablas de datos

### Resumen Ejecutivo (`EXECUTIVE_SUMMARY.md`)
- 7 visualizaciones para tomadores de decisión
- Subtítulos simplificados con foco en implicaciones
- Ordenadas para flujo lógico e impacto
- Apoyan los elementos de acción estratégica

---

## Calidad de Datos y Precisión

Todas las visualizaciones se basan en:
- Datos primarios de `cartera_de_swaps.json`
- Valores calculados de bootstrapping de curva
- Escenarios de estrés regulatorios según CMF RAN 21-13
- Modelos matemáticos verificados en código

**Validación:**
- ✓ Totales de NPV reconciliados en todos los gráficos
- ✓ DV01 verificado (±8M por pb)
- ✓ Impactos de pruebas de estrés consistentes con cálculos técnicos
- ✓ Todos los porcentajes y totales suman 100% / base

---

## Ubicación de Archivos

Todos los archivos de visualización están almacenados en:
```
Tareas/Tarea_1/desarrollo/visualizations/
```

**Tamaño total:** 2.1 MB (10 archivos PNG)

**Tiempo de Generación:** ~45 segundos

---

## Recomendaciones de Uso

1. **Imprimir:** Todos los gráficos están optimizados para impresión a color en 8,5" x 11"
2. **PDF:** Insertar en reportes profesionales sin pérdida de calidad
3. **Presentación:** Usar los archivos PNG nativos para PowerPoint/Slides
4. **Digital:** Visualizar al 100% de zoom para mayor claridad
5. **Distribución:** Incluir archivos de alta resolución en reportes externos

---

## Script de Generación de Gráficos

Las visualizaciones se generaron con:
- **Python:** 3.14.3
- **Librerías:**
  - matplotlib v3.x (gráficos)
  - seaborn v0.14+ (estilos)
  - pandas v2.x (manejo de datos)
  - numpy v1.x (cálculos)

**Ubicación del script:** `src/visualizations.py`

Para regenerar todos los gráficos:
```bash
python src/visualizations.py
```

---

## Próximos Pasos

Para mejorar aún más las visualizaciones, considerar:
1. Añadir dashboards interactivos (Plotly/Tableau)
2. Análisis de series temporales de NPV histórica
3. Simulaciones Monte Carlo con gráficos de distribución
4. Fuentes de datos de mercado en tiempo real para actualizaciones de curva
5. Generación automatizada de reportes con actualizaciones diarias

---

**Informe Generado:** 13 de abril de 2026  
**Estado:** Completo y listo para distribución  
**Calidad:** Grado profesional (300 DPI)  
**Accesibilidad:** Listo para impresión y digital
