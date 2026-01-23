---
description: "Ejecuta la suite completa de pruebas unitarias para asegurar la estabilidad del código."
agent: QA Engineer
skills:
  - tech-stack
---

# Workflow: Run Tests

Este workflow ejecuta todas las pruebas unitarias disponibles en el proyecto.

1.  **Ejecución de Tests**:
    Usa `unittest` a través de `uv` para descubrir y correr las pruebas.
    // turbo
    ```bash
    uv run python -m unittest discover tests
    ```

> [!NOTE]
> Si se requieren pruebas específicas de QGIS, este comando podría necesitar ajustes o un entorno Dockerizado (ver `Makefile` si existe).
