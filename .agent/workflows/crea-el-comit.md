---
description: "Crea el comit asegurando calidad (Ruff), métricas y changelog."
agent: QA Engineer
skills:
  - commit-standards
  - tech-stack
  - project-context
validation: |
  - Verificar que ruff y black pasan sin errores
  - Confirmar que ai-ctx analyze se ejecutó correctamente
  - Validar que el mensaje de commit sigue Conventional Commits
---

Este workflow es el estándar de oro para guardar cambios. No solo hace commit, sino que limpia el código, actualiza la memoria del proyecto y asegura documentación.

## Pasos del Workflow

1.  **Preparación y Limpieza (Automático)**:
    
    🤖 **Agent Action**: Asegurar que el código cumple con estándares de calidad.
    
    Asegura que el código cumple con el estándar de ruff y black para evitar fallos en los hooks.
    // turbo
    ```bash
    uv run ruff check --fix .
    uv run ruff format .
    uv run black .
    ```

2.  **Stage Changes**:
    Añade los archivos que deseas confirmar.
    ```bash
    git add .
    ```

3.  **Sincronización de Calidad (Guardián)**:
    
    🤖 **Agent Action**: Analizar métricas de calidad y alertar si hay regresiones.
    
    Registra el impacto de los cambios en el Cerebro del Proyecto antes de guardar.
    // turbo
    ```bash
    uv run python -m ai_context_core.cli analyze
    ```
    
    🤖 **Agent Action**: Analizar métricas de calidad y alertar si:
    - Complejidad ciclomática aumentó significativamente
    - Cobertura de código bajó
    - Se detectaron nuevas issues de seguridad o deuda técnica

4.  **Actualizar CHANGELOG.md**:
    
    🤖 **Agent Action**: Insertar entrada en sección `[Unreleased]`.
    
    *   Revisa `git status` y `git diff --cached`.
    *   Inserta una línea concisa en la sección `[Unreleased]` de `CHANGELOG.md` describiendo el valor aportado.

5.  **Propuesta de Mensaje (Asistida por IA)**:
    
    🤖 **Agent Action**: Usar skill **commit-standards** para:
    - Analizar cambios preparados (`git diff --cached`)
    - Generar 2-3 opciones de mensajes siguiendo Conventional Commits
    - Validar formato: tipo correcto, scope apropiado, inglés, imperativo
    - Sugerir scope basado en archivos modificados (core, cli, analyzer, config, etc.)
    - Alertar si hay breaking changes que requieren `!` o footer
    
    Ejemplo de sugerencias:
    ```text
    Opción 1: feat(cli): add --output flag for custom report location
    Opción 2: refactor(analyzer): extract complexity calculation to separate module
    Opción 3: fix(config): resolve profile loading error for custom paths
    ```

6.  **Commit**:
    Ejecuta el commit con el mensaje aprobado.
    ```bash
    git commit -m "type(scope): description" -m "detailed body"
    ```
    
    *Si el pre-commit hook persiste en fallar:*
    1. Revisa los mensajes de error detectados.
    2. Ejecuta `git add` de nuevo si hubo cambios automáticos.
    3. Repite el commit.

## Notas Importantes

- Si `ruff` o `black` modificaron archivos en el paso 1, esos cambios se incluirán automáticamente en el commit.
- El mensaje debe seguir **Conventional Commits** (ver `docs/COMMIT_GUIDELINES.md`).
- Si el mensaje generado no te convence, edítalo antes de aprobar el comando final.

**Filosofía**: Cada commit es una unidad de valor limpio, documentado y validado métricamente.

