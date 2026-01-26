---
description: "Ejecuta la suite completa de pruebas unitarias para asegurar la estabilidad del código."
agent: QA Engineer
skills:
  - tech-stack
  - testing-standards
---

# Workflow: Run Tests

Este workflow ejecuta todas las pruebas unitarias disponibles en el proyecto, garantizando un entorno limpio mediante Docker.

1.  **Ejecución de Tests (Dockerizado)**:
    Ejecuta el ciclo de pruebas completo, incluyendo linting y check de cobertura.
    // turbo
    ```bash
    make docker-test
    ```

    > [!TIP]
    > Si el usuario necesita correr solo un test específico localmente, puede usar `uv run pytest tests/test_mi_archivo.py`.
