---
description: "Genera y actualiza la documentación del proyecto."
agent: Plugin Developer
skills:
  - project-context
  - tech-stack
---

# Workflow: Update Documentation

Este workflow se encarga de mantener la documentación al día.

1.  **Actualizar Resumen del Proyecto**:
    Regenera `PROJECT_SUMMARY.md` y `AI_CONTEXT.md` para reflejar la estructura actual.
    // turbo
    ```bash
    uv run ai-ctx analyze
    ```

2.  **Verificar Documentation existente**:
    Revisar `docs/` para asegurar que los nuevos features estén documentados.

3.  **Generar Sphinx Docs (Opción Futura)**:
    *Si se configura Sphinx en el futuro, aquí irían los comandos `make html` o similares.*
