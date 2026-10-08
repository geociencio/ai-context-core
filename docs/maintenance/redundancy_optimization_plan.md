# Plan de Optimización por Redundancias — ai-context-core

**Fecha:** 2026-10-08
**Estado:** En ejecución (Fase A)
**Origen:** Análisis profundo de redundancias, código muerto y duplicaciones.

Este documento consolida los hallazgos del análisis y define un plan por fases
(de menor a mayor riesgo) para eliminar redundancias y código muerto.

---

## Contexto

El código mantiene un quality score de 100/100 y 316 tests, pero arrastra
redundancias estructurales de migraciones incrementales:

- ~31 archivos "facade" de deprecación que solo re-exportan símbolos.
- ~10 módulos completamente muertos (sin referencias de producción).
- Varias implementaciones duplicadas de la misma lógica.
- Tests "cazadores de cobertura" que mantienen vivo el código muerto.

> **Nota arquitectónica:** los hallazgos respetan la separación
> engine → providers → visitors/builders → reporting. Ninguna fase introduce
> lógica de análisis nueva ni acopla capas.

---

## Hallazgos

### 1. Facades de deprecación (dead indirection)

Programados para eliminación en v4.0.0 según `deprecations.py:6`.

| Paquete | Archivos | Re-exporta desde |
|---|---|---|
| `analyzer/patterns_detectors/` | 10 | `visitors/` + `pattern_base.py` |
| `analyzer/context_builders/` | 3 | `builders/` |
| `analyzer/summarizers/` | 4 | `builders/` |
| `analyzer/qgis_checkers/` | 2 | `visitors/` |
| `analyzer/security_checkers/` | 1 | `visitors/` |
| `analyzer/entry_point_detectors/` | 1 | `visitors/` |
| `analyzer/graph/` | 1 | `builders/` |
| `analyzer/checkers/` | 4 | `visitors/` |
| `commands/` (top-level) | 3 | `cli/commands/` |
| `cli_groups/` | 2 | `cli/commands/` |

Ninguno es importado por código de producción.

### 2. Módulos/funciones muertos

- `visitors/legacy.py` — 0 referencias.
- `visitors/antipattern_orchestrator.py` — 0 referencias.
- `builders/scorer.py` (`ProjectScorer`) — solo tests.
- `builders/graph_engine.py` — facade sin imports.
- `analyzer/engine_config.py` — importado con `# noqa: F401` en `engine.py:23`.
- `visitors/security_checker.py`, `visitors/tech_debt_checker.py`,
  `visitors/checker_registry.py`, `visitors/debt.py` — cadena `CheckerRegistry` muerta.
- `fs_tree.analyze_structure()`, `fs_utils.count_file_types()`,
  `fs_utils.calculate_size_stats()` (esta última ni en tests).
- `git_analysis.is_git_repo/get_git_hotspots/get_git_churn` (wrappers legacy).
- 7 wrappers delegadores en `builders/dependencies.py:230-271`.

### 3. Lógica duplicada

1. `load_config()` ×3: `providers/config_loader.py:18` y `engine_config.py:18`
   son idénticos; `config/loader.py:29` (`ConfigLoader`) es distinto (perfiles).
2. `_get_hardcoded_defaults()` ×2 con contenido divergente.
3. Parseo de `metadata.txt` ×2 inconsistente: `gis_utils.parse_qgis_metadata()`
   vs `qgis_resources._parse_metadata_txt()`.
4. `HalsteadVisitor` ×2: `visitors/halstead.py:8` (vivo) y
   `visitors/ast_metrics.py:35` (copia muerta).
5. Helpers `_get_func_name`/`_get_name` ×3 (`qgis_visitor.py:103`,
   `qgis_api.py:99`, `frameworks.py:29`).
6. Detección SIGNAL/SLOT ×2 (`frameworks.py` vs `qgis_api.py`).
7. Bases de detector/checker ×7 y 3 bases de builder (dos casi idénticas).
8. Score calculado ×2: `scorer.ProjectScorer` (muerto) vs
   `calculator.calculate_project_metrics` (vivo).
9. 20 comandos CLI registrados dos veces (nombre + alias `_cmd`) en
   `cli/__init__.py:23-42`.

### 4. Otros code smells

- Tests cazadores de cobertura (`test_absolute_final.py`, `test_coverage_*.py`,
  `test_final_*.py`, `test_gaps_batch*.py`).
- Violación del contrato de métricas en `metrics_summarizer.py:20-23`.
- Script roto `check_complexity.py` (import `analyzer.complexity_visitor`, ruta inexistente).
- Referencias fantasma a `patterns_detectors/observer_components/` en tests/changelogs.

---

## Fases

### Fase A — Limpieza segura (sin tocar API pública)

Objetivo: eliminar código provadamente muerto y los tests que solo existían
para cubrirlo.

1. Borrar módulos sin referencias: `visitors/legacy.py`,
   `visitors/antipattern_orchestrator.py`.
2. Borrar `builders/scorer.py` y sus tests (`test_scorer_extended.py`; retirar
   los tests de scorer de `test_final_bits.py`).
3. Borrar `builders/graph_engine.py` y ajustar los `patch` de
   `test_dependencies_extended.py` si fuera necesario.
4. Borrar `analyzer/engine_config.py`, quitar el import `# noqa` de
   `engine.py:23` y repuntar `test_self_score.py` a `providers.config_loader`.
5. Eliminar símbolos muertos dentro de módulos vivos:
   `HalsteadVisitor` dup de `ast_metrics.py`, `_mask_secret` de `secrets.py`,
   `analyze_structure` de `fs_tree.py`, `count_file_types`/`calculate_size_stats`
   de `fs_utils.py`, alias `scan_project_alt` de `providers/__init__.py`.
6. Reparar o borrar el script roto `check_complexity.py`.

### Fase B — Consolidación de duplicados

7. Unificar `load_config`/`_get_hardcoded_defaults` en un único módulo.
8. Unificar el parseo de `metadata.txt` en `gis_utils`.
9. Consolidar `_get_func_name`/`_get_name` en un util común.
10. Consolidar bases de builder (`context_base` + `summarizer_base`) y revisar
    las 7 bases de detector/checker.
11. Retirar wrappers legacy de `dependencies.py` y `git_analysis.py`
    (acoplados a tests/patch targets).
12. Corregir `metrics_summarizer.py` para usar `metric_keys`.

### Fase C — Eliminación de facades + tests de cobertura

13. Borrar los 10 paquetes facade y actualizar/eliminar los tests que los usan.
14. Eliminar el registro doble de comandos CLI (`_cmd` aliases) o reducirlo.
15. Limpiar tests cazadores de cobertura y referencias fantasma.

---

## Plan de verificación (cada fase)

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
uv run ai-ctx stats
```

Criterios: 0 errores de ruff, suite de tests verde, sin regresión en el
quality score ni en las métricas canónicas.

---

## Registro de progreso

- [x] **Fase A — Completada** (2026-10-08)
  - Eliminados: `visitors/legacy.py`, `visitors/antipattern_orchestrator.py`,
    `builders/scorer.py`, `builders/graph_engine.py`, `engine_config.py`,
    `check_complexity.py`.
  - Símbolos muertos retirados: `HalsteadVisitor` dup (`ast_metrics.py`),
    `_mask_secret`, `analyze_structure`, `count_file_types`,
    `calculate_size_stats`, alias `scan_project_alt`.
  - Tests de cobertura obsoletos retirados/reapuntados (9 tests menos).
  - Verificación: `ruff check` OK · `pytest` 307/307 · quality score 100/100 ·
    `validate_agent_system` PASS.
  - Nota: `ruff format --check` reporta 81 archivos desalineados por un cambio
    de versión de ruff (preexistente en HEAD, no introducido por esta fase).
- [ ] Fase B
- [ ] Fase C

