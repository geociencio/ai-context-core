# Plan de implementación — correcciones de `ai-context-core`

> **Fecha**: 2026-09-17
> **Fuente**: `docs/maintenance/developer_recommendations.md`

De las 9 recomendaciones, #1 (KeyError), #3 (i18n scope), #4a (classFactory) y #4b (Observer) ya están implementadas y testeadas. Este plan cubre lo pendiente + hardening.

---

## 1. Contrato único de claves de métricas (#2 — ALTA)

- Crear constantes compartidas de claves en `src/ai_context_core/analyzer/builders/metric_keys.py`.
- **Nombres canónicos**: `quality_score`, `average_complexity`, `avg_maintenance_index`, `total_functions`, `total_classes`, `total_lines_code`, `total_physical_lines`, `max_complexity`, `test_files_count`, `entry_points_count`.
- `calculator.py`: eliminar alias duplicados (`avg_complexity`, `average_complexity`, `avg_maintainability`, `avg_maintenance_index`) → dejar solo los canónicos.
- Actualizar consumidores inconsistentes (`formatter.py`, `metrics_summarizer.py`, `compare.py`, `stats.py`, `context_metrics.py`).
- Añadir `validate_metric_keys(metrics)` que avise si falta una clave esperada, invocada en `ResultsAggregator.aggregate`.
- **Tests**: contrato `calculator → formatter → stats/compare/context_metrics`; validación avisa claves faltantes.

## 2. Precisión en detección i18n (#6 — MEDIA)

- **Opt-out `# no-i18n`**: extraer líneas marcadas con `tokenize` en `worker.analyze_single`, adjuntarlas al AST y propagarlas por `check_qgis_compliance` → `I18nChecker`.
- **Entropía/detección de idioma** (best-effort) en `is_translatable_string`.
- **Tests**: `# no-i18n` excluye el string.

## 3. Hardening de lo ya implementado

- Auditar accesos a dict en pipeline de patrones/reportes (garantizar `.get()` con fallback).
- `observer_rules.py`: endurecer `_is_signal_definition` (evitar falsos positivos por substring `"signal"`).

## 4. Tests de regresión (#7 — transversal)

- Patrones sin clave `class`.
- Contrato de claves (item 1).
- `_match_path` con `**/*.py` anidado y rutas Windows.
- Scope `gui_only` vs `all`.
- `# no-i18n` opt-out.
- Casos borde entry point `classFactory` y señales Observer.

## 5. Renombrar etiquetas + documentar métricas (#8 — BAJA)

**Renombrado de display (claves JSON internas intactas):**

| Actual | Nueva | Archivos |
|---|---|---|
| `Quality Score` | `ai-ctx Quality Score` | `metrics_summarizer.py`, `summary_generator.py`, `stats.py`, `analyze.py`, `compare.py`, `workflows.py`, `analysis.py`, `ai_recommendations.py`, `defaults.toml` |
| `Average Complexity`/`Avg Complexity` | `Avg Cyclomatic Complexity` | `metrics_summarizer.py`, `context_metrics.py`, `stats.py` |
| `Complexity (Avg)` | `Cyclomatic Complexity (Avg)` | `compare.py` |

**Tests a actualizar:** `tests/test_cli.py`, `tests/test_visualization.py`.

**Documentación:**
- `README.md`: sección "Metrics" (definición de cada métrica y diferencias vs `qgis-analyzer`).
- `CHANGELOG.md`: entrada de rename + clarificación semántica.

---

## Orden de ejecución
1 → 2 → 3 → 4 → 5

## Verificación
- `uv run pytest`
- `uv run ruff check .` y `uv run ruff format .`
