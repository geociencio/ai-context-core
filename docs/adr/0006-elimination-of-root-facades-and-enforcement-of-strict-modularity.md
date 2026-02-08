# 0006. Eliminación de facades raíz y cumplimiento de modularidad estricta

**Estado**: Aceptado

**Fecha**: 2026-02-07

**Autores**: Antigravity

**Decisores**: Juan M Bernales, Antigravity

---

## Contexto y Problema

Durante la evolución del paquete `analyzer`, se crearon múltiples archivos en la raíz del paquete (`src/ai_context_core/analyzer/`) que actuaban como **facades** (ej. `issues.py`, `dependencies.py`, `git_analysis.py`). Estos archivos no contenían lógica de negocio, sino que servían para re-exportar funciones y clases de sub-paquetes más granulares (`visitors`, `builders`, `providers`).

Aunque inicialmente esto facilitaba las importaciones, a largo plazo generó:
1.  **Redundancia**: Mantener la facade y el módulo real duplicaba el esfuerzo de actualización.
2.  **Confusión**: Los desarrolladores no sabían si importar desde la raíz o desde el sub-paquete.
3.  **Acoplamiento Implícito**: La raíz del paquete se convirtió en un "punto caliente" (hotspot) innecesario.
4.  **Dificultad en Testing**: Los tests unitarios a menudo apuntaban a las facades, enmascarando la verdadera estructura del sistema.

## Factores de Decisión

- **Mantenibilidad**: Reducir el número de archivos que requieren actualización cuando cambia una firma.
- **Claridad Arquitectónica**: Reforzar la arquitectura modular (Visitors -> Builders -> Providers).
- **Consistencia**: Asegurar que todos los componentes (tests, CLI, engine) usen el mismo estándar de importación.
- **Rendimiento**: Minimizar la cadena de importaciones en tiempo de ejecución.

## Opciones Consideradas

### Opción 1: Mantener las Facades Indefinidamente
**Descripción**: Mantener los archivos en la raíz para facilitar el uso por parte de terceros o scripts internos.

**Pros**:
- ✅ No rompe compatibilidad con versiones anteriores.
- ✅ Importaciones más cortas (`from analyzer import issues`).

**Contras**:
- ❌ Perpetúa la deuda técnica.
- ❌ Dificulta la refactorización profunda de los sub-paquetes.

### Opción 2: Eliminación Total de Facades (Elegida)
**Descripción**: Eliminar todos los archivos redundantes en la raíz de `analyzer` y migrar todas las referencias internas y tests a los nuevos paths modulares.

**Pros**:
- ✅ Arquitectura limpia y sin redundancias.
- ✅ Los tests se vuelven puramente unitarios al apuntar al componente exacto.
- ✅ Alineación total con el estándar de "Fragmentation Extrem" del proyecto.

**Contras**:
- ❌ Requiere una migración masiva de tests (266 tests afectados).
- ❌ Puede romper scripts externos que dependan de la estructura antigua.

## Decisión

**Opción elegida**: Opción 2 - Eliminación Total de Facades.

**Justificación**: 
Para alcanzar el objetivo de un **Quality Score > 90** y una arquitectura mantenible a largo plazo, es imperativo que la estructura de archivos sea un reflejo fiel de la arquitectura lógica. Las facades en la raíz creaban una "ilusión" de simplicidad que complicaba el mantenimiento real. La migración exitosa de la suite completa de tests (100% pass rate) valida que el sistema es más robusto sin estas capas intermedias.

## Consecuencias

### Positivas

- ✅ **Transparencia**: La estructura de directorios (`visitors`, `builders`, etc.) ahora dicta claramente dónde vive cada responsabilidad.
- ✅ **Test Isolation**: Los tests unitarios ahora validan módulos específicos sin cargar dependencias innecesarias de la raíz.
- ✅ **Cero Duplicación**: Se eliminaron ~23 archivos que solo contenían declaraciones de importación.

### Negativas

- ❌ **Breaking Change**: Esta es una ruptura mayor de la API interna para cualquier extensión que no use los entry points oficiales.

### Neutrales

- ℹ️ **Curva de Aprendizaje**: Los nuevos contribuidores deben conocer la estructura modular profunda en lugar de confiar en un "catch-all" en la raíz.

## Implementación

- [x] Crear scripts de migración temporal para actualizar imports en `/tests`.
- [x] Ejecutar la eliminación de archivos facade en `src/ai_context_core/analyzer/`.
- [x] Refactorizar `engine.py` para usar imports directos.
- [x] Actualizar todas las sub-apps del CLI.
- [x] Validar la suite completa con `pytest`.

## Validación

- **Métrica 1**: Cobertura de tests (mantenida en >98%).
- **Métrica 2**: Éxito en ejecución de `ai-ctx analyze` sobre el propio proyecto.
- **Métrica 3**: Verificación manual de la ausencia de imports circulares en la raíz.

## Referencias

- [Modular Refactor Phase 3: Facade Elimination](docs/CHANGELOG.md)
- [Architecture Guide: Semantic Extraction Pipeline](docs/ARCHITECTURE.md)
