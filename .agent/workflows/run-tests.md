---
description: "Ejecuta la suite completa de pruebas unitarias para asegurar la estabilidad del código."
agent: QA Engineer
skills:
  - tech-stack
  - testing-standards
---

# Workflow: Run Tests

Este workflow ejecuta todas las pruebas unitarias disponibles en el proyecto, garantizando un entorno reproducible mediante uv.

1.  **Ejecución de Tests**:
    
    *Opción A: Entorno Aislado (Docker - Recomendado)*
    Garantiza que funciona en un entorno limpio sin contaminación local.
    // turbo
    ```bash
    make docker-test
    ```

    *Opción B: Entorno Local (uv - Rápido)*
    Para iteraciones rápidas durante el desarrollo.
    ```bash
    uv run pytest tests/ -v --cov=src/ai_context_core
    ```

    > [!TIP]
    > Parametros útiles:
    > - `-k "pattern"`: Ejecuta solo tests que coincidan con el patrón.
    > - `-x`: Detiene la ejecución al primer fallo.
    > - `--pdb`: Entra en el debugger al fallar.
