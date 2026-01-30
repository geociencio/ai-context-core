# Plan de Implementación: Optimizaciones AI-Context-Core

Plan detallado para implementar las recomendaciones de optimización identificadas en [OPTIMIZATION_RECOMMENDATIONS.md](file:///home/jmbernales/qgispluginsdev/ai-context-core/docs/OPTIMIZATION_RECOMMENDATIONS.md). Este plan aborda las áreas críticas que mejorarán la precisión, mantenibilidad y flexibilidad de la herramienta.

## User Review Required

> [!IMPORTANT]
> **Refactorización Mayor de `ast_utils.py`**
> 
> La Fase 2 implica dividir el archivo `ast_utils.py` (actualmente ~1000+ líneas) en 4 módulos separados. Esto afectará todos los imports en el proyecto y requiere una migración cuidadosa. Se recomienda realizar esta fase en una rama separada con revisión exhaustiva.

> [!WARNING]
> **Cambios en la API de Configuración**
> 
> La Fase 3 externalizará valores hardcodeados a archivos YAML. Esto podría afectar a usuarios que dependan del comportamiento actual si tienen configuraciones personalizadas no documentadas.

> [!CAUTION]
> **Eliminación de `find_security_issues`**
> 
> La Fase 1 deprecará/eliminará la función `find_security_issues` basada en búsqueda de cadenas. Aunque genera falsos positivos, algunos usuarios podrían depender de ella. Se recomienda un período de deprecación con warnings antes de la eliminación completa.

---

## Proposed Changes

### Fase 1: Refactorización del Escáner de Seguridad

**Objetivo:** Eliminar falsos positivos en la detección de vulnerabilidades mediante análisis AST en lugar de búsqueda de cadenas.

#### [MODIFY] [issues.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/issues.py)

- Deprecar función `find_security_issues` con warning de deprecación
- Separar `detect_secrets` como función independiente y bien documentada
- Añadir flag de configuración para habilitar/deshabilitar el método legacy

#### [MODIFY] [ast_utils.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/ast_utils.py)

- Expandir clase `ASTSecurityDetector` para incluir:
  - Detección de `exec()` y `eval()` mediante análisis de nodos `ast.Call`
  - Detección de `os.system()`, `subprocess` sin validación
  - Detección de `pickle.loads()` con datos no confiables
  - Detección de SQL injection patterns en construcción de queries
- Implementar método `visit_Call` mejorado que diferencia entre:
  - Uso real de funciones peligrosas
  - Menciones en strings/comentarios
  - Uso en contextos seguros (ej: dentro de tests)

#### [NEW] [test_security_ast.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/tests/test_security_ast.py)

- Tests para cada patrón de seguridad detectado por AST
- Tests que verifican ausencia de falsos positivos
- Tests con casos edge (funciones con nombres similares, strings, etc.)

---

### Fase 2: Modularización de Componentes de Análisis

**Objetivo:** Mejorar mantenibilidad dividiendo módulos monolíticos en componentes cohesivos.

#### Reestructuración del Módulo `analyzer`

##### [NEW] [ast_visitors.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/ast_visitors.py)

- Mover todas las clases Visitor:
  - `CodeAnalysisVisitor`
  - `EntryPointVisitor`
  - `ASTSecurityDetector`
  - `DependencyVisitor`

##### [NEW] [ast_metrics.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/ast_metrics.py)

- Mover funciones de cálculo de métricas:
  - `calculate_complexity`
  - `calculate_maintainability_index`
  - Funciones auxiliares de análisis de código

##### [NEW] [ast_entry_points.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/ast_entry_points.py)

- Mover lógica específica de detección de entry points:
  - Detección de CLI entry points
  - Detección de API endpoints
  - Detección de event handlers

##### [NEW] [ast_qgis.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/ast_qgis.py)

- Mover detección específica de QGIS:
  - Detección de plugins QGIS
  - Detección de processing algorithms
  - Análisis de metadata QGIS

##### [MODIFY] [ast_utils.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/ast_utils.py)

- Mantener solo utilidades genéricas de AST
- Añadir imports de re-exportación para compatibilidad temporal
- Añadir deprecation warnings para imports directos

#### Reestructuración del Sistema de Detección de Issues

##### [NEW] [checkers/__init__.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/checkers/__init__.py)

- Definir interfaz base `BaseChecker` con métodos:
  - `check(module_info: Dict) -> List[Issue]`
  - `get_severity() -> str`
  - `get_category() -> str`

##### [NEW] [checkers/security_checker.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/checkers/security_checker.py)

- Migrar lógica de detección de seguridad
- Implementar `SecurityChecker(BaseChecker)`

##### [NEW] [checkers/tech_debt_checker.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/checkers/tech_debt_checker.py)

- Migrar detección de deuda técnica
- Implementar `TechDebtChecker(BaseChecker)`

##### [NEW] [checkers/optimization_checker.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/checkers/optimization_checker.py)

- Migrar detección de oportunidades de optimización
- Implementar `OptimizationChecker(BaseChecker)`

##### [MODIFY] [issues.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/issues.py)

- Refactorizar para usar el sistema de checkers
- Implementar registro de checkers dinámico
- Mantener función wrapper para compatibilidad

---

### Fase 3: Externalización de Configuración

**Objetivo:** Hacer la herramienta configurable mediante archivos YAML en lugar de valores hardcodeados.

#### [MODIFY] [defaults.yaml](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/config/defaults.yaml)

Añadir nuevas secciones de configuración:

```yaml
# Umbrales de Calidad
quality_thresholds:
  complexity:
    warning: 10
    error: 15
  maintainability:
    warning: 65
    error: 50
  
# Pesos para Quality Score
quality_weights:
  complexity: 0.25
  maintainability: 0.20
  test_coverage: 0.15
  documentation: 0.15
  security: 0.25

# Patrones de Seguridad
security_patterns:
  dangerous_functions:
    - exec
    - eval
    - __import__
  dangerous_modules:
    - pickle
    - marshal
  sql_injection_indicators:
    - "execute("
    - "executemany("
    
# Configuración de Análisis
analysis:
  parallel_workers: auto  # 'auto' o número específico
  cache_enabled: true
  max_file_size_mb: 10
```

#### [MODIFY] [engine.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/engine.py)

- Cargar configuración desde `defaults.yaml` al inicio
- Pasar configuración relevante a cada módulo de análisis
- Permitir override desde `.ai-context/config.yaml` del proyecto

#### [MODIFY] [issues.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/issues.py)

- Recibir umbrales desde configuración en lugar de constantes
- Usar patrones de seguridad desde configuración

#### [NEW] [docs/CONFIGURATION.md](file:///home/jmbernales/qgispluginsdev/ai-context-core/docs/CONFIGURATION.md)

- Documentar todas las opciones de configuración disponibles
- Incluir ejemplos de configuraciones personalizadas
- Explicar jerarquía de configuración (defaults → proyecto → CLI)

---

### Fase 4: Mejora del Análisis de Dependencias

**Objetivo:** Corregir la clasificación de dependencias y generar grafos precisos.

#### [MODIFY] [dependencies.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/dependencies.py)

- Mejorar función `classify_dependency`:
  - Usar `sys.stdlib_module_names` para detectar stdlib (Python 3.10+)
  - Detectar dependencias internas comparando con `project_root`
  - Clasificar resto como terceros
- Corregir construcción del grafo de dependencias:
  - Incluir solo dependencias internas en el grafo principal
  - Crear grafo separado para dependencias externas si es necesario
  - Asegurar que todos los nodos estén conectados correctamente

#### [MODIFY] [formatters/mermaid.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/formatters/mermaid.py)

- Validar que el grafo generado sea conexo
- Añadir leyenda que explique los tipos de dependencias
- Mejorar layout para proyectos grandes

#### [NEW] [test_dependencies.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/tests/test_dependencies.py)

- Tests para clasificación de cada tipo de dependencia
- Tests para construcción correcta del grafo
- Tests con proyectos de ejemplo (stdlib, interno, terceros)

---

### Fase 5: Incremento de Cobertura de Documentación y Tests

**Objetivo:** Mejorar mantenibilidad a largo plazo mediante documentación y tests.

#### Documentación

##### [MODIFY] Múltiples archivos Python

- Añadir docstrings a todas las funciones y clases públicas en:
  - `ast_utils.py` y módulos derivados
  - `engine.py`
  - `dependencies.py`
  - `issues.py` y checkers
- Seguir formato Google Docstrings según [coding-standards](file:///home/jmbernales/qgispluginsdev/ai-context-core/.agent/skills/coding-standards/SKILL.md)

#### Tests

##### [NEW] [test_entry_points.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/tests/test_entry_points.py)

- Tests para cada tipo de entry point:
  - CLI entry points (`if __name__ == "__main__"`)
  - FastAPI/Flask endpoints
  - QGIS processing algorithms
  - Event handlers

##### [MODIFY] [.github/workflows/ci.yml](file:///home/jmbernales/qgispluginsdev/ai-context-core/.github/workflows/ci.yml)

- Añadir step de `ai-ctx audit` en CI/CD
- Establecer umbral mínimo de quality score (ej: 70)
- Fallar el build si el score está por debajo del umbral

---

## Verification Plan

### Automated Tests

```bash
# Ejecutar suite completa de tests
uv run pytest tests/ -v --cov=src/ai_context_core --cov-report=term-missing

# Verificar que no hay regresiones
uv run pytest tests/ -v

# Ejecutar análisis de calidad
uv run ai-ctx analyze

# Verificar que el quality score ha mejorado
uv run ai-ctx audit
```

### Manual Verification

1. **Auto-análisis sin falsos positivos:**
   ```bash
   uv run ai-ctx analyze
   ```
   - Verificar que no se reporten vulnerabilidades en las definiciones de patrones de seguridad
   - Confirmar que el grafo de dependencias muestra correctamente módulos internos conectados

2. **Configuración personalizada:**
   - Crear archivo `.ai-context/config.yaml` con umbrales personalizados
   - Verificar que la herramienta respeta la configuración personalizada

3. **Validación de modularización:**
   - Verificar que todos los imports funcionan correctamente
   - Confirmar que no hay imports circulares
   - Ejecutar `ruff check` y `black --check` para validar estilo

4. **Comparación de métricas:**
   - Ejecutar análisis antes y después de las optimizaciones
   - Documentar mejora en quality score (objetivo: pasar de 52.3 a >70)
   - Verificar reducción en falsos positivos de seguridad
