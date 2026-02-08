# 0007. Análisis de i18n con Alcance Configurable (Scoped i18n)

**Estado**: Aceptado

**Fecha**: 2026-02-07

**Autores**: Antigravity

**Decisores**: Juan M Bernales, Antigravity

---

## Contexto y Problema

El análisis de internacionalización (i18n) actual de `ai-context-core` examina todos los archivos del proyecto. Sin embargo, en el desarrollo de plugins QGIS es común tener módulos de "core" o lógica de negocio que contienen cadenas técnicas (logs, constantes internas) que no requieren traducción.

Esto genera dos problemas:
1. **Falsos Positivos**: El score de i18n se diluye al contar cadenas técnicas no traducibles como "pendientes de traducción".
2. **Falta de Foco**: Los desarrolladores no pueden distinguir fácilmente si la interfaz de usuario (GUI) está completamente traducida o no.

## Decisión

Se decide implementar un mecanismo de **filtrado por alcance (scoping)** para el análisis de i18n, configurable a nivel de perfil o por CLI.

### Nuevas Opciones de Configuración

Se introduce la sección `[qgis.i18n]` en el perfil `qgis.toml`:

- **`scope`**: Define el modo de operación.
    - `"all"` (Default): Comportamiento actual, analiza todo el proyecto.
    - `"gui_only"`: Analiza solo archivos que coincidan con patrones de GUI (ej. `gui/**/*.py`, `dialogs/**/*.py`).
    - `"custom"`: Usa listas explícitas de `include_patterns` y `exclude_patterns`.

### Implementación Técnica

- El filtrado se realiza en la etapa de **agregación** (`aggregate_qgis_compliance`), no en el visitor, para mantener la flexibilidad y performance.
- Se implementa una lógica de coincidencia de rutas robusta que soporta patrones glob recursivos (`**`).
- El reporte final incluye metadata sobre el alcance utilizado.

## Consecuencias

### Positivas
- **Scores más precisos**: Los desarrolladores obtienen una métrica real de cobertura de traducción para la interfaz de usuario.
- **Flexibilidad**: Adaptable a diferentes estructuras de proyecto.
- **Retrocompatibilidad**: El valor por defecto `"all"` preserva el comportamiento existente.

### Negativas
- **Complejidad de Configuración**: Añade una nueva capa de configuración que los usuarios deben conocer.
- **Riesgo de Exclusión**: Si se configura mal, se podrían ignorar cadenas que sí deberían traducirse.

## Validación

Se han añadido pruebas unitarias (`tests/test_i18n_scoping.py`) que verifican:
- El filtrado correcto de módulos en modo `gui_only`.
- La exclusión correcta en modo `custom`.
- La preservación del comportamiento en modo `all`.
