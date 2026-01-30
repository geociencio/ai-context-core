---
description: "Inicializa la sesión: actualiza métricas, carga contexto crítico y verifica entorno."
agent: Senior Architect
skills:
  - project-context
  - tech-stack
validation: |
  - Verificar que 11 tests pasen
  - Confirmar que AI_CONTEXT.md está actualizado con métricas recientes
  - Validar que no hay regresiones en complejidad ciclomática
---

Este workflow optimiza el inicio del desarrollo asegurando un entorno sincronizado, **contextualizado** y validado.

1.  **Sintonización de Contexto (CRÍTICO)**:
    
    🤖 **Agent Action**: Actualizar y revisar contexto para entender "dónde nos quedamos".
    
    Actualiza y lee el contexto para entender el estado actual del proyecto.
    // turbo
    ```bash
    uv run python -m ai_context_core.cli analyze && cat .agent/next_steps.md
    ```
    
    🤖 **Agent Action**: Revisar archivos de contexto usando skills **project-context** y **tech-stack** para identificar:
    - Deuda técnica crítica (funciones largas, alta complejidad)
    - Módulos con complejidad ciclomática alta (CC > 15)
    - Recomendaciones de optimización pendientes
    
    Revisa los siguientes archivos en este orden:
    *   **`.agent/next_steps.md`**: **[CRÍTICO]** El Testigo. Punto exacto donde se detuvo la sesión anterior.
    *   **`AI_CONTEXT.md`**: Memoria de largo plazo, métricas y directrices de alto nivel.
    *   **`project_context.json`**: Datos estructurados de complejidad y dependencias.
    *   **`docs/DEVELOPMENT_LOG.md`**: Ver resumen de la última sesión (orden cronológico inverso).
    *   **`CHANGELOG.md`**: Cambios recientes y features en desarrollo.

2.  **Sincronización de Entorno**:
    
    🤖 **Agent Action**: Verificar que no hay conflictos de dependencias.
    
    Asegura que las dependencias estén sincronizadas.
    // turbo
    ```bash
    uv sync
    ```

3.  **Verificación de Estado (Sanity Check)**:
    
    🤖 **Agent Action**: Confirmar que el sistema está estable. Los 11 tests deben pasar.
    
    Verifica que el código base esté estable antes de empezar a trabajar.
    
    Verifica que el código base esté estable antes de empezar a trabajar.
    
    *Opción A (Docker - Robusto):*
    // turbo
    ```bash
    make docker-test
    ```
    
    *Opción B (Local - Rápido):*
    ```bash
    uv run pytest tests/ -v
    ```
    
    🤖 **Agent Action**: Si hay fallos en tests:
    - Identificar si son fallos de lógica o de configuración
    - Sugerir correcciones basadas en estándares del proyecto
    - Verificar cobertura de código (objetivo: >70%)

**Objetivo**: Empezar a codificar sabiendo *exactamente* qué pasó en la última sesión y con el contexto del proyecto cargado.

