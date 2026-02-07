---
name: testing-standards
description: Directrices para asegurar la estabilidad del código mediante pruebas automatizadas con Pytest y Docker.
---

# Testing Standards

Define los requisitos y mejores prácticas para el testing dentro del proyecto, priorizando la consistencia del entorno y la velocidad de ejecución.

## Cuándo usar este skill
- Al crear nuevas funcionalidades (TDD o post-implementación).
- Al refactorizar lógica crítica.
- Antes de subir cambios al repositorio.
- Durante la fase de VERIFICACIÓN de un flujo agentic.

## Grado de Libertad
- **Estricto**: El uso de Docker (`make docker-test`) es obligatorio para la validación final.

## Inputs necesarios
- Código a probar y suite de tests existente en `tests/`.

## Workflow
1. **Diseño**: Escribir tests usando `unittest.TestCase`.
2. **Ejecución Local**: Probar rápidamente con `uv run pytest`.
3. **Validación Final**: Ejecutar en entorno aislado con `make docker-test`.
4. **Análisis**: Verificar que la cobertura cumpla los umbrales establecidos.

## Instrucciones y Reglas

### 1. Framework y Runner
- **Estilo**: Usar la librería estándar `unittest`.
- **Runner**: Ejecutar con `pytest` para mejores reportes y herramientas de cobertura.
- **Ubicación**: Todos los tests en la carpeta `tests/`.
- **Nomenclatura**: Archivos con prefijo `test_` (ej. `test_engine.py`).

### 2. Aislamiento con Docker
- **Obligatorio**: La validación final **debe** realizarse con Docker para replicar condiciones de CI.
- Comando: `make docker-test`

### 3. Cobertura y Calidad
- **Umbral Global**: Mínimo **70%** de cobertura.
- **Rutas Críticas**: `engine.py` y `ast_utils.py` deben apuntar a >80%.
- **Mocks**: Usar `unittest.mock` para aislar dependencias externas (sistema de archivos, git).
- **Sin Efectos Secundarios**: Usar directorios temporales (`tempfile`) y limpiar tras la ejecución.

## Output (formato exacto)
Reporte de tests exitosos y métricas de cobertura aprobadas.

## Lista de Verificación de Calidad
- [ ] ¿Los tests se ejecutan correctamente con `make docker-test`?
- [ ] ¿Se cumple el umbral de cobertura del 70%?
- [ ] ¿Se usan mocks para dependencias externas?
- [ ] ¿El código sigue la nomenclatura `test_*.py`?
- [ ] ¿La documentación del skill está en español?
