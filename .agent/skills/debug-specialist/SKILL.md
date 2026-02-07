---
name: debug-specialist
description: Especialista en resolución sistemática de errores mediante el método científico, asegurando que cada fix sea reproducible y no genere regresiones.
---

# Debug Specialist

Este skill guía la resolución de errores técnicos evitando parches rápidos y priorizando la estabilidad y calidad del código.

## Cuándo usar este skill
- Cuando el usuario reporte un bug o error.
- Cuando un test falle inesperadamente.
- Cuando se detecte un comportamiento anómalo en el análisis AST.
- Ante excepciones no manejadas en la ejecución de scripts.

## Grado de Libertad
- **Estricto**: La creación de un test de reproducción es obligatoria antes de modificar el código fuente.

## Inputs necesarios
- Traceback del error o descripción del comportamiento esperado vs real.
- Acceso a la suite de tests (`tests/`).

## Workflow

1.  **Aislamiento**: Identificar la causa raíz analizando logs y tracebacks.
2.  **Reproducción**: Crear un nuevo test en `tests/` que falle específicamente debido a este bug.
3.  **Hipótesis**: Formular una explicación clara de por qué ocurre el error.
4.  **Corrección**: Aplicar el fix mínimo necesario respetando `@coding-standards`.
5.  **Verificación**: Correr el nuevo test y toda la suite (`make docker-test`).
6.  **Documentación**: Registrar la lección en `.agent/memory/AGENT_LESSONS.md` si es un patrón recurrente.

## Instrucciones y Reglas

### 1. No parches "a ciegas"
- Está prohibido modificar código sin entender *exactamente* por qué falla.
- Si el error es intermitente, usa logs adicionales para capturar el estado antes de intentar el fix.

### 2. Prioridad de Tests
- El fix solo se considera exitoso si el test de reproducción pasa y no bajan las métricas de `ai-ctx analyze`.

### 3. Limpieza
- Eliminar cualquier `print` temporal o código de debug antes de hacer el commit.

## Output (formato exacto)
- Informe diagnóstico: [Causa Raíz].
- Test de reproducción: `tests/test_issue_XXX.py`.
- Fix aplicado en: [Módulo].
- Resultado de validación: [PASÓ/FALLÓ].

## Lista de Verificación de Calidad
- [ ] ¿Se creó un test que inicialmente fallaba?
- [ ] ¿El fix respeta el uso de `pathlib` y tipos?
- [ ] ¿Se ha verificado que no hay regresiones en otros módulos?
- [ ] ¿Se ha mantenido o mejorado el Quality Score?
- [ ] ¿Se documentó la lección aprendida si aplica?
