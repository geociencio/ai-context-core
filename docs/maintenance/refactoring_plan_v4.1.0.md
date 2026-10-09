# Plan de Refactorización — ai-context-core v4.1.0

> **Fecha**: 2026-10-08
> **Versión analizada**: `ai-context-core` v4.0.0 (CLI `ai-ctx`, commit `ae8ab85`)
> **Base**: demanda de consumo de SecInterp (rol real: mapa de contexto + priorización de deuda)
> **Estado**: aprobado en alcance — una única `v4.1.0` con los workstreams WS-0..WS-5.
> **Secuencia**: WS-0 → WS-1 → WS-2 + WS-3 → WS-4 + WS-5 (orden sugerido aceptado).

---

## 0. Objetivo

Convertir a `ai-ctx` en lo que de verdad aporta a los proyectos consumidores
(mapa de contexto + priorización de deuda técnica), eliminando el ruido de métricas
que duplican a `qgis-analyzer` y reparando los tres defectos que hoy inutilizan su
parte más valiosa.

## 1. Causas raíz confirmadas

| # | Defecto | Causa raíz | Archivo |
| :--- | :--- | :--- | :--- |
| G1 | Grafo con `Edges: 1` | `resolve_import` no mapea imports absolutos con prefijo de paquete (`sec_interp.core.x`) contra `import_map` que solo tiene `core.x` (sin prefijo) | `builders/builder_components.py`, `builders/builder.py` |
| G2 | Mermaid malformado | dedup usa `->` pero emite `-->`; `__init__.py`→`init` colisiona; `class` solo para `top_node_names` | `builders/reporting.py` |
| C1 | Churn absurdo (`512,593`) | `parse_churn` suma `added+deleted` de todos los commits de 30 días, incluyendo renombrados | `providers/parser.py`, `providers/analyzer.py` |
| A1 | Anti-patrones ruido | `MagicNumberDetector` marca todo número `∉{-1,0,1}` con severity `low`, sin allowlist; el render ignora `severity` | `visitors/magic_number.py`, `builders/patterns.py` |
| S1 | Score siempre emitido | el score se calcula en `aggregate()` y se imprime/audita siempre; no hay vía "solo contexto" | `engine.py`, `cli/commands/analyze.py` |
| K1 | Config duplicada | dos loaders (`config/loader.py` vs `providers/config_loader.py`) y doble formato (`.yaml` en CLI, `.toml` en engine) | `config/loader.py`, `cli/commands/analyze.py` |

## 2. Principios del plan

- **Un cambio estructural por workstream**, con test de regresión en cada defecto.
- **Respetar el contrato de métricas**: toda clave nueva va en `builders/metric_keys.py`.
- **No romper la suite**: `uv run pytest -q` verde tras cada workstream.
- **Formato canónico**: `ruff format` en todos los archivos tocados.
- Verificación por workstream: `uv run ruff check . && uv run pytest -q`.

---

## 3. Workstreams

### WS-0 — Unificar la carga de configuración (fundacional)

- **Archivos**: `config/loader.py`, `analyzer/providers/config_loader.py`, `cli/commands/analyze.py`.
- **Cambio**:
  1. Un solo loader canónico `providers/config_loader.load_config` con detección de `.toml` (y `.yaml` legacy como fallback).
  2. `config/loader.py` → faceta `DeprecationWarning` que delega al loader canónico.
  3. La CLI deja de leer `.ai-context/config.yaml` directamente; pasa por `load_config`.
- **Test**: `tests/test_config.py`, `tests/test_config_extended.py` — `context_docs`/`scoring` de un proyecto consumidor se reflejan en el output.
- **Riesgo**: bajo.

### WS-1 — Reparar grafo de importaciones + diagrama (valor máximo)

- **Archivos**: `builders/builder.py`, `builders/builder_components.py`, `builders/dependencies.py`, `builders/reporting.py`, `visitors/imports_visitor.py`.
- **Cambio**:
  1. `ImportGraphBuilder` deriva el prefijo raíz del proyecto (paquete top-level desde `metadata.txt`/`pyproject`/`src/`) y normaliza ambos lados (strip del prefijo en el import o prefijo en las claves del map).
  2. Resolver imports relativos (`node.level > 0`) en `imports_visitor.py` reconstruyendo el módulo absoluto desde el paquete del archivo actual.
  3. Reescribir `generate_dependency_diagram`: sanitizar IDs (reemplazar `/`, `.`, `-` por `_`), dedup sobre la forma emitida (`-->`), declarar `class` para **todos** los nodos citados, `classDef` una sola vez.
  4. Tests golden con `tests/fixtures/golden_plugin/`.
- **Test**: `tests/test_dependencies_advanced.py`, `tests/test_dependencies_extended.py` — `edges >= N` esperado y mermaid parsable.
- **Riesgo**: medio.

### WS-2 — Churn/hotspots realistas

- **Archivos**: `providers/analyzer.py`, `providers/parser.py`, `builders/git_tech.py`.
- **Cambio**:
  1. `get_churn` usa `git log --numstat --find-renames` y agrupa por archivo (per-file), no un total global.
  2. `parse_churn` devuelve `per_file: {path: {added, deleted}}` además del total acotado.
  3. `GitTechBuilder` renderiza `total` (sin renombrados) + top-5 por churn cruzado con hotspots.
- **Test**: `tests/test_git_analysis.py`.
- **Riesgo**: bajo.

### WS-3 — Anti-patrones con severidad + allowlist + priorización

- **Archivos**: `visitors/magic_number.py`, `visitors/antipattern_base.py`, `builders/patterns.py`.
- **Cambio**:
  1. Config `[patterns.antipatterns]`: allowlist de constantes, umbral de severidad, filtro por archivo.
  2. `MagicNumberDetector` consulta la allowlist (añadir constantes comunes).
  3. `PatternsBuilder.build` ordena por severidad (high→low), muestra severidad y respeta el corte configurable.
- **Test**: `tests/test_antipatterns.py`.
- **Riesgo**: bajo.

### WS-4 — Modo "context-only" (desacoplar contexto de score)

- **Archivos**: `cli/commands/analyze.py`, `cli/commands/__init__.py` (registro de comandos), `engine.py`.
- **Cambio**:
  1. Nuevo comando `ai-ctx context` (o `analyze --no-score`): genera `AI_CONTEXT.md` + `project_context.json` sin imprimir/auditar el score.
  2. `run_audit` queda como único intérprete del score como gate.
  3. El output del score se etiqueta como heurístico/no-canónico.
- **Test**: `tests/test_cli.py`, `tests/test_report_coverage.py`.
- **Riesgo**: medio.

### WS-5 — Secciones seleccionables de `AI_CONTEXT.md`

- **Archivos**: `builders/ai_context_generator.py`, `builders/dependencies.py`, `builders/git_tech.py`.
- **Cambio**:
  1. Config `[context].sections` para togglear cada builder.
  2. Defaults saneados: omitir `PROJECT KEYWORDS` y `UNUSED IMPORTS` triviales.
  3. `DependencyBuilder` filtra `__future__` de unused imports.
- **Test**: `tests/test_report_coverage.py`.
- **Riesgo**: bajo.

---

## 4. Criterios de éxito

| Criterio | Ahora | Objetivo v4.1.0 |
| :--- | :--- | :--- |
| Grafo de importaciones | `Edges: 1`, density 0.000 | `Edges` real (~80+ en SecInterp), mermaid válido |
| Churn 30 días (SecInterp) | `512,593` | orden de magnitud realista, top-5 por archivo |
| Anti-patrones | solo Magic Numbers sin priorizar | severidad + allowlist + orden high→low |
| Modo contexto | siempre emite/audita score | `ai-ctx context` sin score |
| Config | dos loaders (yaml/toml) | un loader canónico |

---

## 5. Referencias

- `docs/ARCHITECTURE.md` — capas (providers/visitors/builders/cli/context).
- `docs/maintenance/refactoring_plan_v3.4.0.md` — patrón de plan previo.
- Release notes v4.0.0 — anti-patterns visibles, dead code removal.
