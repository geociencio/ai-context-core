# Plan de Implementación: Corrección de Agregación de Métricas v3.2.1

Este plan aborda el bug donde las métricas globales de funciones, clases, complejidad y mantenimiento se reportan como `0` en `AI_CONTEXT.md` debido a un mismatch de llaves y omisiones en el calculador central.

## Cambios Propuestos

### Componente: Analyzer Builders

#### [MODIFY] [calculator.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/builders/calculator.py)
- Actualizar `calculate_project_metrics` para acumular `total_functions` y `total_classes` desde la lista de módulos.
- Renombrar las llaves de retorno para alinearlas con el estándar del sistema:
  - `avg_complexity` -> `average_complexity` (Manteniendo `avg_complexity` por compatibilidad en `metrics_summarizer.py`).
  - `avg_maintainability` -> `avg_maintenance_index` (Manteniendo `avg_maintainability` por compatibilidad).
- Añadir `total_functions` y `total_classes` al diccionario de retorno.

#### [MODIFY] [formatter.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/builders/formatter.py)
- Asegurar que `format_complexity_agg` use las llaves actualizadas del calculador.

## Plan de Verificación

### Pruebas Automatizadas
- **Análisis de Proyecto Real**: Ejecutar `uv run python -m ai_context_core.cli analyze` y verificar manualmente que `AI_CONTEXT.md` muestre valores distintos de cero.
- **Suite de Tests Existente**: Ejecutar `uv run pytest tests/test_aggregator_extended.py` para asegurar que la agregación no se rompa.
- **Nuevo Test Unitario**: Crear `tests/test_metrics_fix.py` para validar específicamente que `calculate_project_metrics` devuelva todas las llaves requeridas con valores correctos.

```bash
uv run pytest tests/test_metrics_fix.py
uv run pytest tests/test_aggregator_extended.py
```

### Verificación Manual
1. Borrar caché: `rm .ai_context_cache.json` (opcional).
2. Ejecutar: `uv run python -m ai_context_core.cli analyze`.
3. Inspeccionar `AI_CONTEXT.md` y buscar la sección `## 📈 COMPLEXITY AND METRICS`.
4. Verificar que **Functions**, **Classes**, **Average Complexity** y **Avg Maintenance Index** sean > 0.
