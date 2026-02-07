---
description: "Ejecuta la suite completa de pruebas unitarias para asegurar la estabilidad del código."
agent: QA Engineer
skills:
  - tech-stack
  - testing-standards
---

# Workflow: Ejecución de Pruebas

Este workflow garantiza que el código sea estable y cumpla con los umbrales de cobertura definidos.

## 1. Ejecución Estratégica

**Opción A: Entorno Aislado (Docker - Recomendado)**
Garantiza un entorno limpio y reproducible.
// turbo
```bash
make docker-test
```

**Opción B: Entorno Local (uv - Rápido)**
Para desarrollo activo e iteraciones rápidas.
```bash
uv run pytest tests/ -v --cov=src/ai_context_core --cov-report=term-missing
```

## 2. Análisis de Resultados

- **Fallo de Tests**: Si un test falla, detén el desarrollo y prioriza la corrección.
- **Cobertura**: Verifica que no haya regresiones. El objetivo global es **>70%**.
- **Regresión**: Si la cobertura baja, se debe justificar o añadir más tests.

## Tips Útiles
- Usar `-x` para detenerse al primer error.
- Usar `--ff` para ejecutar primero los tests que fallaron anteriormente.
