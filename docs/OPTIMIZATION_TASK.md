# Plan de Implementación: Optimizaciones AI-Context-Core

## Fase 1: Refactorización del Escáner de Seguridad (Alta Prioridad)
- [ ] Analizar el código actual de `find_security_issues` en `issues.py`
- [ ] Expandir `ASTSecurityDetector` para cubrir patrones actualmente detectados por búsqueda de cadenas
- [ ] Implementar detección AST para `exec`, `eval`, `os.system` y otros patrones peligrosos
- [ ] Separar `detect_secrets` como función independiente
- [ ] Eliminar o deprecar `find_security_issues` basado en cadenas
- [ ] Escribir tests unitarios para los nuevos detectores AST
- [ ] Validar que no hay falsos positivos en el auto-análisis

## Fase 2: Modularización de Componentes (Alta Prioridad)
- [ ] Dividir `ast_utils.py` en módulos cohesivos:
  - [ ] Crear `ast_visitors.py`
  - [ ] Crear `ast_metrics.py`
  - [ ] Crear `ast_entry_points.py`
  - [ ] Crear `ast_qgis.py`
- [ ] Reestructurar `issues.py`:
  - [ ] Crear subpaquete `checkers/` o `rules/`
  - [ ] Implementar interfaz común para checkers
  - [ ] Migrar detectores existentes a clases individuales
- [ ] Actualizar imports en todos los archivos afectados
- [ ] Ejecutar tests para validar la refactorización
- [ ] Actualizar documentación

## Fase 3: Externalización de Configuración (Media Prioridad)
- [ ] Identificar todos los valores hardcodeados (umbrales, pesos, patrones)
- [ ] Mover configuración a `defaults.yaml`
- [ ] Actualizar `engine.py` para cargar configuración desde YAML
- [ ] Implementar sobrescritura desde `.ai-context/config.yaml`
- [ ] Documentar opciones de configuración disponibles
- [ ] Escribir tests para el sistema de configuración

## Fase 4: Mejora del Análisis de Dependencias (Media Prioridad)
- [ ] Analizar lógica actual en `dependencies.py`
- [ ] Implementar diferenciación correcta entre tipos de dependencias:
  - [ ] Librería estándar
  - [ ] Dependencias internas
  - [ ] Dependencias de terceros
- [ ] Corregir construcción del grafo de dependencias
- [ ] Validar grafo Mermaid.js generado
- [ ] Escribir tests para clasificación de dependencias

## Fase 5: Incremento de Cobertura (Baja Prioridad)
- [ ] Auditar módulos sin docstrings
- [ ] Documentar funciones y clases públicas
- [ ] Escribir tests unitarios para `EntryPointVisitor`
- [ ] Integrar `ai-ctx audit` en CI/CD
- [ ] Establecer umbral mínimo de calidad
