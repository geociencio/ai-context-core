---
description: "Finaliza sesión: corre tests, actualiza logs (Dev/Maintenance), regenera contexto IA y propone commit de cierre."
agent: QA Engineer
skills:
  - project-context
  - commit-standards
validation: |
  - Verificar que todos los logs están actualizados
  - Confirmar que tests pasan antes de cerrar
  - Validar que .agent/next_steps.md existe y tiene contenido claro
---

Este workflow asegura un cierre limpio y documentado del trabajo realizado.

1.  **Formateo de Código**:
    Asegura consistencia en el estilo del código.
    ```bash
    uv run black .
    ```

2.  **Sanity Check (Tests)**:
    
    🤖 **Agent Action**: Verificar que los 7 tests pasan. Alertar si hay fallos.
    
    Verifica que no rompimos nada crítico antes de irnos.
    
    Verifica que no rompimos nada crítico antes de irnos.
    
    *Opción A (Docker - Final Check):*
    // turbo
    ```bash
    make docker-test
    ```
    
    *Opción B (Local):*
    ```bash
    uv run pytest tests/ -v
    ```
    
3.  **Actualización de Memoria (Logs & Roadmap)**:
    
    🤖 **Agent Action**: Validar que todos los archivos críticos están actualizados.
    
    *   **Identificación del Tema**: Define un nombre corto para la sesión (ej: `docker_integration`).
    *   **`.agent/next_steps.md`**: **[CRÍTICO]** Crea o actualiza este archivo con el "paso de testigo": qué falta, qué errores hay pendientes y cuál es el comando para retomar.
    *   **Archivado de Next Steps**: **[NUEVO]** Copia `.agent/next_steps.md` a `.agent/history/next_steps/next_steps_YYYY-MM-DD.md` para mantener el registro histórico.
    *   **`docs/sessions/session_YYYY-MM-DD_[TEMA].md`**: **[OBLIGATORIO]** Crea este archivo con el resumen técnico de la sesión.
    *   **`docs/DEVELOPMENT_LOG.md`**: **[CRÍTICO]** Añade una entrada `## [YYYY-MM-DD] Resumen` en la parte superior.
    *   **`CHANGELOG.md`**: Registra cambios visibles para el usuario en `[Unreleased]`.

4.  **Sincronización de Contexto Final**:
    
    🤖 **Agent Action**: Actualizar AI_CONTEXT.md y validar que next_steps.md es claro.
    
    Actualiza las métricas y la memoria de largo plazo del proyecto. Valida calidad antes de cerrar.
    // turbo
    ```bash
    uv run ai-ctx audit --threshold 50
    uv run ai-ctx analyze && cat .agent/next_steps.md
    ```

5.  **Commit de Cierre**:
    
    🤖 **Agent Action**: Usar skill **commit-standards** para generar mensaje apropiado.
    
    Guarda tu progreso.
    ```bash
    git add .
    git commit -m "chore(docs): close session [TEMA]"
    ```
    
    **Formato recomendado**: `chore(docs): close session [tema_descriptivo]`

6.  **Resumen para el Usuario**:
    
    🤖 **Agent Action**: Generar resumen estructurado de la sesión.
    
    Genera un mensaje final listando:
    *   Archivos de log actualizados.
    *   Estado de los tests (7 tests OK).
    *   Contenido de `.agent/next_steps.md`.
    *   Sugerencia para la próxima sesión (comando `/inicia-sesion`).

**Filosofía**: Una sesión no termina cuando el código funciona, sino cuando la historia está contada.

