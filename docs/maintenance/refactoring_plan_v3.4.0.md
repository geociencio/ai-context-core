# Plan de Refactorización — ai-context-core v3.4.0

> **Fecha**: 2026-10-06
> **Versión analizada**: `ai-context-core` v3.4.0 (CLI `ai-ctx`, commit `b8520a5`)
> **Base**: [`improvement_report_v3.4.0.md`](improvement_report_v3.4.0.md)
> **Estado**: propuesta aprobada en alcance; **sin cambios de código aún**.
> **Relación**: deriva de la auditoría del informe de mejora, con correcciones de verificación.

---

## 0. Resumen de auditoría previa

El informe base es correcto en los bugs de correctitud (A1–A5), pero se corrigieron
descaracterizaciones tras verificar cada hallazgo contra el código real:

| # | Hallazgo | Veredicto de auditoría |
| :--- | :--- | :--- |
| A1 | `entry_points` no persistido | ✅ Confirmado empíricamente (`AI_CONTEXT.md` con `ENTRY POINTS` vacía pese a `__main__.py`) |
| A2 | tests acoplados al `IgnoreFilter` | ✅ Confirmado, pero **la recomendación #2 del informe era insuficiente** (el scanner también filtra) |
| A3 | ruta legacy ignora i18n | ⚠️ Confirmado, pero es **código muerto** (sin llamadores) |
| A4 | parámetro muerto `in_dict_key` | ✅ Confirmado |
| A5 | `except` silencioso en `_match_path` | ✅ Confirmado |
| B | scoring opaco / `max_complexity` | ⚠️ Parcial: `max_complexity` **sí se reporta**, no solo se calcula |
| C | denylist i18n frágil | ✅ Confirmado |
| D | falta `--include-md` | ✅ Confirmado, con matiz: se leen **dos** docs fijos |
| E1 | paquetes muertos/duplicados | ❌ **Incorrecto**: son **facades de compatibilidad** (usadas por tests) |
| E2 | aliases de compatibilidad | ✅ Confirmado, sin uso en `src` |
| E4 | `aggregate_qgis_compliance` monolítica | ✅ Confirmado (~145 líneas) |

---

## 1. Principios del plan

- **Un solo cambio estructural por fase**, con test de regresión en cada bug.
- **Respetar el contrato de métricas**: toda clave nueva va en `builders/metric_keys.py`.
- **No romper la suite**: los shims de compatibilidad se deprecan, no se borran aún
  (los tests los importan).
- Verificación por fase: `uv run ruff check . && uv run pytest -q` + `uv run ai-ctx analyze --path .`.

---

## 2. Fase 1 — Correctitud (patch/minor)

### 1.1 — A1: persistir `entry_points`
- **Archivos**: `builders/aggregator.py`, `builders/structure.py`.
- **Cambio**: calcular `entry_points` como lista de `{path, type}` usando
  `m.get("entry_point_info", {}).get("type")`; añadir `"entry_points": entry_points`
  al dict de retorno de `aggregate()` (líneas 90-103). `StructureBuilder.build`
  tolera ambos formatos (str legacy / dict) y muestra `- \`path\` (type)`.
- **Test**: `tests/test_entry_points.py` — módulo con `classFactory` y con `__main__`
  aparecen listados; `analyses["entry_points"]` no vacío.
- **Riesgo**: bajo. **Revierte**: quitar la clave.

### 1.2 — A2: desacoplar conteo de tests del `IgnoreFilter`
- **Archivos**: `providers/fs_scanner.py`, `builders/aggregator.py`,
  `builders/calculator.py`, `builders/metrics_summarizer.py`.
- **Cambio**:
  - Nueva función `count_test_files(project_path)` que recorre el árbol ignorando
    **solo** `.venv/`, `.git/`, `build/`, `dist/`, `__pycache__` — **nunca** los
    patrones de `.analyzerignore`.
  - Eliminar el recálculo de `aggregator.py:68`; el scoring usa el nuevo contador.
  - Renombrar el label `Test Coverage` → `Test Files` (`metrics_summarizer.py:22`).
  - Si el conteo no se pudo determinar → `n/a` y **no** aplicar el `-20`.
- **Test**: proyecto con `tests/` en `.analyzerignore` da `test_files_count > 0`
  y sin penalización de `-20`.
- **Riesgo**: medio (toca scoring). **Mitigación**: fixtures con y sin ignore.

### 1.3 — A3: eliminar wrapper muerto
- **Archivo**: `builders/aggregator.py:175-181`.
- **Cambio**: borrar `_aggregate_qgis_compliance` (sin llamadores verificado por grep)
  y su import perezoso.

### 1.4 — A4: eliminar parámetro muerto
- **Archivo**: `visitors/i18n_components.py:16`.
- **Cambio**: quitar `in_dict_key` y su rama (líneas 29-31); el estado se gestiona en
  `qgis_visitor.py:95-101`.

### 1.5 — A5: no silenciar el `except`
- **Archivo**: `builders/aggregator_qgis.py:44-46`.
- **Cambio**: registrar `logger.warning("Invalid glob pattern %r", pattern)` antes del
  `return False` (mantener el fallback).

---

## 3. Fase 2 — Explicabilidad del score (minor)

- **2.1 — Score Breakdown**: `calculator.py` devuelve un `score_breakdown` (nuevas claves
  en `metric_keys.py`); `metrics_summarizer.py` lo renderiza desglosado
  (complejidad / MI / tests).
- **2.2 — Usar `max_complexity`**: penalizar outliers con umbral configurable
  (`complexity_high`), no solo el promedio.
- **2.3 — Externalizar umbrales/pesos** hoy mágicos (`65`, `-20`, `+2`, literal `15`)
  a `config/defaults.toml` + `config_loader.py`.
- **2.4 — Nota "no canónico"** dentro del reporte generado, no solo en README.
- **Riesgo**: medio-alto (cambia scores). **Mitigación**: golden files antes/después.

---

## 4. Fase 3 — Refactor estructural

### 3.1 — Consolidar shims de compatibilidad (E1+E2 unificados)
- **No son código muerto**: `context_builders/`, `patterns_detectors/` y `commands/`
  son facades finas que re-exportan lo canónico y **se importan desde los tests**.
- **Cambio**: añadir `DeprecationWarning` con fecha, migrar imports de tests a rutas
  canónicas, documentar público vs. interno. Borrado en versión mayor.

### 3.2 — Dividir `aggregate_qgis_compliance` (E4)
- **Cambio**: extraer `_should_include_for_i18n`, `_collect_api_issues`,
  `_aggregate_i18n_stats`, `_compute_compliance_score`, cada una CC ≤ 10.

---

## 5. Fase 4 — Valor diferencial

- **4.1 — i18n**: allowlist de APIs de UI (`setText`, `setTitle`, `QAction`,
  `addAction`…) configurable, sustituyendo la denylist frágil.
- **4.2 — `--include-md PATTERN` / `context_docs`**: volcar a "MANUAL ARCHITECTURE NOTES"
  (`structure.py:22-24`); hoy solo se leen 2 rutas fijas.
- **4.3 — CI golden files**: smoke test `ai-ctx analyze` sobre plugin fixture y
  comparación de `AI_CONTEXT.md`/`PROJECT_SUMMARY.md`.

---

## 6. Criterios de aceptación por fase

- `uv run ruff check .` sin errores.
- `uv run pytest -q` verde + nuevo test de regresión por bug.
- `uv run ai-ctx analyze --path .` sin regresiones; `ENTRY POINTS` no vacía.
- Conventional Commits en inglés.

**Esfuerzo estimado**: F1 ≈ 1 sesión; F2 ≈ 1; F3 ≈ 1-2; F4 ≈ 2+.

---

## 7. Orden recomendado

1. **Fase 1** completa (máximo impacto/correctitud, riesgo bajo).
2. **Fase 2** (explicabilidad).
3. **Fase 3** (refactor estructural, requiere tests verdes).
4. **Fase 4** (valor diferencial).

Cada fase en un commit(s) convencional independiente y con su test de regresión.
