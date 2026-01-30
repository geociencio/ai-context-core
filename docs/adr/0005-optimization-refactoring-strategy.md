# 0005. Estrategia de Refactorización y Optimización del Analizador

**Estado**: Propuesto

**Fecha**: 2026-01-29

**Autores**: AI Assistant (Gemini)

**Decisores**: Equipo de desarrollo ai-context-core

---

## Contexto y Problema

El análisis de calidad del proyecto ai-context-core reveló un Quality Score de 52.3/100, indicando oportunidades significativas de mejora. Los problemas principales identificados son:

1. **Falsos positivos en seguridad**: El escáner `find_security_issues` usa búsqueda de cadenas, generando falsos positivos al detectar definiciones de patrones como vulnerabilidades reales.

2. **Módulos monolíticos**: `ast_utils.py` contiene 1000+ líneas con múltiples responsabilidades (visitors, métricas, entry points, QGIS), dificultando el mantenimiento.

3. **Configuración hardcodeada**: Umbrales, pesos de calidad y patrones están codificados directamente en el código, limitando la flexibilidad.

4. **Análisis de dependencias incorrecto**: La clasificación de dependencias identifica módulos internos como "terceros" y genera grafos desconectados.

5. **Baja cobertura de documentación**: Solo 49.2% de docstrings, dificultando la comprensión y mantenimiento.

**Restricciones**:
- Mantener compatibilidad con API pública existente
- No introducir dependencias adicionales
- Preservar rendimiento actual (caché, paralelización)

## Factores de Decisión

- **Precisión**: Reducir falsos positivos en detección de seguridad
- **Mantenibilidad**: Facilitar comprensión y modificación del código
- **Extensibilidad**: Permitir agregar nuevos checkers y reglas fácilmente
- **Flexibilidad**: Hacer la herramienta configurable por proyecto
- **Compatibilidad**: Minimizar breaking changes para usuarios existentes

## Opciones Consideradas

### Opción 1: Refactorización Incremental por Fases

**Descripción**: Dividir las mejoras en 5 fases priorizadas, implementando cambios graduales con períodos de deprecación.

**Pros**:
- ✅ Menor riesgo de introducir regresiones
- ✅ Permite validación continua entre fases
- ✅ Facilita revisión de código en PRs manejables
- ✅ Usuarios pueden adaptarse gradualmente
- ✅ Posibilidad de pausar si surgen problemas

**Contras**:
- ❌ Mayor tiempo total de implementación
- ❌ Requiere mantener código legacy temporalmente
- ❌ Posibles conflictos entre fases

### Opción 2: Refactorización Completa en una Sola Versión

**Descripción**: Implementar todos los cambios simultáneamente en una versión mayor (v3.0.0).

**Pros**:
- ✅ Implementación más rápida
- ✅ No requiere mantener código de compatibilidad
- ✅ Arquitectura limpia desde el inicio

**Contras**:
- ❌ Alto riesgo de regresiones
- ❌ Difícil de revisar (PRs masivos)
- ❌ Breaking changes abruptos para usuarios
- ❌ Difícil rollback si hay problemas

### Opción 3: Crear Herramienta Nueva (ai-context-core-v2)

**Descripción**: Desarrollar una nueva versión desde cero manteniendo la versión actual.

**Pros**:
- ✅ Libertad total de diseño
- ✅ Sin restricciones de compatibilidad
- ✅ Versión actual sigue funcionando

**Contras**:
- ❌ Duplicación de esfuerzo
- ❌ Fragmentación de la base de usuarios
- ❌ Mantenimiento de dos proyectos
- ❌ Pérdida de momentum del proyecto actual

## Decisión

**Opción elegida**: Opción 1 - Refactorización Incremental por Fases

**Justificación**: 

La refactorización incremental ofrece el mejor balance entre mejora de calidad y gestión de riesgo. Permite:

1. **Validación continua**: Cada fase puede ser probada exhaustivamente antes de continuar
2. **Compatibilidad gradual**: Períodos de deprecación dan tiempo a usuarios para migrar
3. **Revisión manejable**: PRs más pequeños facilitan code review de calidad
4. **Flexibilidad**: Podemos ajustar el plan basándonos en feedback de fases anteriores

Las fases propuestas están ordenadas por impacto y dependencias:
- **Fase 1** (Alta): Seguridad AST - Mejora inmediata en precisión
- **Fase 2** (Alta): Modularización - Base para futuras mejoras
- **Fase 3** (Media): Configuración - Flexibilidad sin breaking changes
- **Fase 4** (Media): Dependencias - Corrección de funcionalidad existente
- **Fase 5** (Baja): Documentación - Mejora continua

## Consecuencias

### Positivas

- ✅ **Precisión mejorada**: Eliminación de falsos positivos en seguridad mediante análisis AST
- ✅ **Mantenibilidad incrementada**: Módulos cohesivos y bien organizados
- ✅ **Flexibilidad**: Configuración externalizada permite adaptación por proyecto
- ✅ **Extensibilidad**: Sistema de checkers facilita agregar nuevas reglas
- ✅ **Calidad medible**: Quality Score objetivo >70 (vs 52.3 actual)
- ✅ **Riesgo controlado**: Validación continua entre fases

### Negativas

- ❌ **Tiempo de implementación**: 5 fases requieren más tiempo que enfoque big-bang
- ❌ **Código temporal**: Necesidad de mantener deprecation warnings y compatibilidad
- ❌ **Coordinación**: Requiere sincronización cuidadosa entre fases

### Neutrales

- ℹ️ **Breaking changes controlados**: Algunos cambios requerirán migración de usuarios
- ℹ️ **Documentación adicional**: Guías de migración para cada fase
- ℹ️ **Versionado semántico**: Incrementos de versión menor/mayor según impacto

## Implementación

### Fase 1: Refactorización del Escáner de Seguridad
- [ ] Expandir `ASTSecurityDetector` con detección de `exec`, `eval`, `os.system`
- [ ] Deprecar `find_security_issues` con warnings
- [ ] Separar `detect_secrets` como función independiente
- [ ] Tests para cada patrón AST
- [ ] Validar auto-análisis sin falsos positivos

### Fase 2: Modularización de Componentes
- [ ] Dividir `ast_utils.py` en: `ast_visitors.py`, `ast_metrics.py`, `ast_entry_points.py`, `ast_qgis.py`
- [ ] Crear sistema de checkers en `analyzer/checkers/`
- [ ] Implementar `BaseChecker` interface
- [ ] Migrar detectores a checkers individuales
- [ ] Actualizar todos los imports

### Fase 3: Externalización de Configuración
- [ ] Extender `defaults.yaml` con umbrales y pesos
- [ ] Modificar `engine.py` para cargar configuración
- [ ] Implementar override desde `.ai-context/config.yaml`
- [ ] Documentar opciones en `CONFIGURATION.md`

### Fase 4: Mejora del Análisis de Dependencias
- [ ] Corregir clasificación en `dependencies.py`
- [ ] Usar `sys.stdlib_module_names` para stdlib
- [ ] Generar grafos Mermaid conectados
- [ ] Tests para cada tipo de dependencia

### Fase 5: Incremento de Cobertura
- [ ] Añadir docstrings (Google Docstrings)
- [ ] Tests para `EntryPointVisitor`
- [ ] Integrar `ai-ctx audit` en CI/CD
- [ ] Establecer umbral mínimo de quality score

## Validación

**Métricas de éxito**:

- **Quality Score**: Incremento de 52.3 → >70
- **Falsos positivos**: Reducción del 100% → <5% en detección de seguridad
- **Cobertura de docstrings**: 49.2% → >80%
- **Modularidad**: Reducción de complejidad ciclomática en módulos principales
- **Precisión de dependencias**: 100% de clasificación correcta en auto-análisis

**Validación por fase**:

1. **Fase 1**: Auto-análisis sin reportar vulnerabilidades en definiciones de patrones
2. **Fase 2**: Todos los tests pasan, no hay imports circulares
3. **Fase 3**: Configuración personalizada funciona correctamente
4. **Fase 4**: Grafo de dependencias muestra módulos internos conectados
5. **Fase 5**: CI/CD pasa con quality score >70

## Referencias

- [OPTIMIZATION_RECOMMENDATIONS.md](file:///home/jmbernales/qgispluginsdev/ai-context-core/docs/OPTIMIZATION_RECOMMENDATIONS.md) - Análisis detallado de problemas
- [Implementation Plan](file:///home/jmbernales/.gemini/antigravity/brain/5f3068a5-6e6d-4374-bd77-9a225ee9e2ed/implementation_plan.md) - Plan técnico detallado
- [ADR-0002](file:///home/jmbernales/qgispluginsdev/ai-context-core/docs/adr/0002-implement-13-improvements-roadmap.md) - Roadmap de mejoras previo
- [Coding Standards](file:///home/jmbernales/qgispluginsdev/ai-context-core/.agent/skills/coding-standards/SKILL.md) - Estándares del proyecto

## Notas

- **Compatibilidad**: Se mantendrá compatibilidad hacia atrás durante al menos 2 versiones menores
- **Deprecation policy**: Warnings claros con instrucciones de migración
- **Rollback plan**: Cada fase puede revertirse independientemente si es necesario
- **Comunicación**: Changelog detallado y release notes para cada fase
