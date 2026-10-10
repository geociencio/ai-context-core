# 0008. Contrato Context-Only: `ai-context-core` como compilador de contexto

**Estado**: Aceptado

**Fecha**: 2026-10-09

**Autores**: Juan M Bernales, @architect

**Decisores**: Juan M Bernales, @architect (@auditor para disciplina de alcance)

---

## Contexto y Problema

`ai-context-core` (CLI `ai-ctx`, v4.1.1) se presenta como *"el sistema nervioso
central para tu flujo de trabajo asistido por IA"*, con **Context Management**
como capacidad principal. Sin embargo, ha crecido hasta convertirse en un
**motor de análisis estático completo** que duplica casi línea por línea a
`qgis-plugin-analyzer`.

Evidencia verificada (2026-10-09):

- `analyzer/visitors/` tiene **58 módulos** (security, QGIS, i18n, patrones,
  anti-patrones, métricas) y `analyzer/builders/` **33**.
- La capa `context/` (**260 LOC**) está **instanciada pero no consumida**:
  `engine.py:22,63` construye `AIContextManager` y nunca lee su resultado.
- Las dependencias de runtime (`click`, `rich`) permiten seguir
  auto-contenido ⇒ se re-implementa el análisis en lugar de consumirlo.
- ADR-0002 ("13 mejoras") reforzó *añadir análisis* en vez de afinar la promesa
  de contexto.

Esto genera dos problemas: **duplicación de mantenimiento** con
`qgis-plugin-analyzer` y **deriva de identidad** del producto.

## Factores de Decisión

- **Responsabilidad única**: un proyecto, una promesa.
- **Coherencia de ecosistema**: `qgis-plugin-analyzer` debe ser el único dueño
  de la higiene de plugin.
- **Eficiencia de tokens / verificabilidad**: los artefactos de contexto deben
  ser compactos, versionados y con provenance.
- **Costo de compatibilidad**: cambio mayor (`4.x → 5.0.0`) con consumidores
  (`sec_interp`, `qgis-plugin-analyzer` como dev-dep).
- **Riesgo de migración**: una sola iteración de deprecación exige facades y
  stubs de redirección.

## Opciones Consideradas

### Opción 1: Status quo (analizador completo)

**Descripción**: Mantener el motor de análisis dentro de `ai-context-core`.

**Pros**:
- ✅ Cero costo de migración.
- ✅ Autónomo para proyectos Python no QGIS.

**Contras**:
- ❌ Duplica `qgis-plugin-analyzer` de forma indefinida.
- ❌ Contradice la identidad "context management".
- ❌ Mantenimiento doble y resultados divergentes.

### Opción 2: Context-only estricto (rompiente, v5.0.0)

**Descripción**: `ai-context-core` se convierte en un **compilador de contexto**
que *consume* análisis y produce artefactos para agentes de IA.

**Pros**:
- ✅ Identidad coherente y mantenible.
- ✅ Elimina la duplicación; `qgis-plugin-analyzer` pasa a ser el único dueño de
  la higiene.
- ✅ Habilita presupuesto de tokens, verificación y symbol index.

**Contras**:
- ❌ Cambio mayor con comandos e imports eliminados.
- ❌ Requiere una iteración de deprecación y stubs de redirección.

### Opción 3: Híbrido (mantener análisis + añadir contexto)

**Descripción**: Conservar todo el análisis y agregar la capa de contexto.

**Pros**:
- ✅ Sin ruptura inmediata.

**Contras**:
- ❌ No resuelve la duplicación (el problema raíz).
- ❌ Aumenta superficie de mantenimiento y deuda.

## Decisión

**Opción elegida**: **Opción 2 — Context-only estricto (v5.0.0)**.

`ai-context-core` compila contexto mediante un pipeline
**`source` (extraer) → `transform` (contexto / symbol index / budget) →
`render` (artefactos) → `verify`**.

Puntos vinculantes de este contrato:

1. **Capa de extracción = `sources/`.** Se nombra `sources/` y **no**
   `providers/` para evitar colisión con el paquete existente
   `analyzer/providers/` (fs cache, scanner, worker, git, config loader,
   `secrets_scanner`). El protocolo vive en `sources/base.py`
   (`AnalysisProvider`) y normaliza a `model/AnalysisResult`.
   - `sources/external/` consume `qgis-analyzer` (JSON) o
     `analysis_results/project_context.json`.
   - `sources/builtin/` extrae un mínimo Python-genérico (estructura, imports,
     complejidad) como fallback autónomo.
2. **El Quality Score / gate `audit` se renombra a "context health".** No hay
   puerta de calidad; `audit` se elimina y `health` sólo falla por staleness.
3. **Ownership de artefactos.** `qgis-plugin-analyzer` es dueño de
   `analysis_results/project_context.json`; `ai-context-core` mantiene su
   `project_context.json` en la raíz (retrocompatible) y le añade un bloque
   `_meta = {schema, producer, tool_version}`. Nunca escribe en
   `analysis_results/`.
4. **No-objetivos (propiedad de los hermanos).** Cumplimiento QGIS, i18n
   (`MISSING_I18N`), seguridad (Bandit/secrets/injection), scoring de calidad /
   gate CC, lint/format (`ruff`), packaging/deploy y scaffolding.
5. **Compatibilidad.** Bump mayor `4.x → 5.0.0`, `REMOVAL_VERSION = "5.0.0"`,
   facades de import (advertir, no romper) y stubs de CLI que redirigen al
   dueño durante una release.

## Consecuencias

### Positivas

- ✅ Identidad de producto coherente ("compilador de contexto").
- ✅ Fin de la duplicación con `qgis-plugin-analyzer` (single-sourcing de i18n,
  seguridad, cumplimiento).
- ✅ Artefactos de contexto compactos, versionados y verificables (budget +
  `verify` + symbol index).

### Negativas

- ❌ Cambio mayor con eliminación de comandos e imports.
- ❌ Trabajo de migración en consumidores y stubs de deprecación por una release.

### Neutrales

- ℹ️ La capa `context/` deja de estar "instanciada pero no consumida" y pasa a
  albergar `transform`/`budget`/`verify`/`store`.
- ℹ️ `roadmap` depende de complejidad + churn: no se podan
  `complexity_visitor`, `sloc` ni `git_tech`.

## Implementación

Detalle completo en
[`docs/plans/implementation_plan_ai_context_core_context_only_v5.md`](../plans/implementation_plan_ai_context_core_context_only_v5.md)
(revisado vía `/ia-critic`, ver
[`docs/reviews/ia_critic_implementation_plan_context_only_v5.md`](../reviews/ia_critic_implementation_plan_context_only_v5.md)).

- [x] **F0** — Contrato y congelación (este ADR; `REMOVAL_VERSION`; naming de docs).
- [x] **F1** — Capa `sources/` + `model/`; `--source`; `context` como ruta primaria.
- [x] **F2** — Eliminación (v5.0.0): comandos/visitantes/builders; facades; tests.
- [x] **F3** — Presupuesto de tokens + manifest.
- [x] **F4** — `verify` + symbol index + `health`.
- [ ] **F5** — Alineación de ecosistema — **DIFERIDA a los repos hermanos** (fuera del alcance de `ai-context-core`): `agentic-forge` (skill `project-context`), `qgis-plugin-analyzer` (README/cross-link), `sec_interp` (workflows `/start-session`, `/close-session`). Cada repo gestiona su propio cambio.

**Congelación de features**: desde F0 no se añaden nuevas capacidades de análisis
a `ai-context-core`; cualquier propuesta de ese tipo se rechaza en F2
(@auditor gate).

## Validación

- `uv run pytest -q` verde y `uv run ruff check .` limpio por fase.
- `ai-ctx context` equivalente vía `sources/external` vs `builtin` (snapshot).
- `ai-ctx verify` → 0 fresco, 1 stale; `--max-tokens N` nunca excede `N`.
- Tras F5, `forge validate` verde en los tres repos hermanos.

## Referencias

- Plan: `docs/plans/implementation_plan_ai_context_core_context_only_v5.md`
- Revisión: `docs/reviews/ia_critic_implementation_plan_context_only_v5.md`
- ADR-0002: `docs/adr/0002-implement-13-improvements-roadmap.md` (origen de la deriva)
- ADR-0006: `docs/adr/0006-elimination-of-root-facades-and-enforcement-of-strict-modularity.md`
- Sibling: `qgis-plugin-analyzer` (dueño de la higiene de plugin)

## Notas

- La edición mecánica de los documentos activos (README, `CONFIGURATION.md`)
  para renombrar el score puede completarse en F2, cuando el comando `health`
  exista; en F0 se registra la decisión y el aviso de deprecación para no
  documentar un comando inexistente.
