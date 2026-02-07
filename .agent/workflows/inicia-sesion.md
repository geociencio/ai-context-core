---
description: "Inicializa la sesión: actualiza métricas, carga contexto crítico y verifica entorno."
agent: Senior Architect
skills:
  - project-context
  - tech-stack
validation:
  - ¿Los 11 tests pasan satisfactoriamente?
  - ¿AI_CONTEXT.md refleja las últimas métricas?
  - ¿Se ha leído .agent/next_steps.md para retomar el trabajo?
---

# Workflow: Iniciar Sesión

Este workflow optimiza el inicio del desarrollo asegurando un entorno sincronizado, **contextualizado** y validado.

## 1. Sintonización de Contexto (CRÍTICO)

Actualiza y lee el contexto para entender el estado actual del proyecto.

// turbo
```bash
uv run python -m ai_context_core.cli analyze && cat .agent/next_steps.md
```

**Acciones del Agente**:
- Revisar `.agent/next_steps.md` para identificar el punto exacto de interrupción.
- Consultar `AI_CONTEXT.md` para métricas de complejidad y deuda técnica.
- Verificar `CHANGELOG.md` para cambios recientes.

## 2. Sincronización de Entorno

Asegura que las dependencias y el entorno estén al día.

// turbo
```bash
uv sync
```

## 3. Verificación de Estado (Sanity Check)

Verifica que el código base sea estable antes de comenzar.

**Opción A (Docker - Recomendado):**
// turbo
```bash
make docker-test
```

**Opción B (Local - Rápido):**
```bash
uv run pytest tests/ -v
```

## Resultado Esperado
- Entorno de desarrollo actualizado (`uv sync`).
- Contexto de la IA fresco y alineado con los últimos cambios.
- Plan de acción claro basado en los "next steps" previos.
- Estado de tests: **11 tests OK**.
