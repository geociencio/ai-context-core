# Task Breakdown - ai-context-core Improvements

Basado en: [implementation_plan_improvements.md](file:///home/jmbernales/qgispluginsdev/ai-context-core/docs/implementation_plan_improvements.md)

## Fase 1: Correcciones Críticas (11-15 horas)

### Mejora 1: Entry Points Detection (4-6h)
- [x] Analizar código actual de `ast_utils.py`
- [x] Implementar `is_entry_point()` con soporte para:
  - [x] QGIS `classFactory(iface)`
  - [x] Click `@click.command`
  - [x] Flask `@app.route`
  - [x] FastAPI `@app.get/post`
- [x] Refactorizar `has_main_guard()` como parte de `is_entry_point()`
- [x] Actualizar `engine.py` para usar nueva función
- [x] Crear `tests/test_entry_points.py`
  - [x] Test para QGIS plugin
  - [x] Test para Click CLI
  - [x] Test para Flask app
  - [x] Test para FastAPI app
- [x] Documentar en README.md

### Mejora 5: Anti-Patrones (4-5h)
- [x] Crear `src/ai_context_core/analyzer/antipatterns.py`
- [x] Implementar detectores:
  - [x] `detect_god_object()` - Clases con >20 métodos
  - [x] `detect_spaghetti_code()` - Funciones CC >25
  - [x] `detect_magic_numbers()` - Constantes hardcodeadas
  - [x] `detect_dead_code()` - Código nunca importado
- [x] Integrar en `engine.py`
- [x] Agregar sección "Anti-Patterns" en templates
- [x] Crear `tests/test_antipatterns.py`
  - [x] Test para God Object
  - [x] Test para Spaghetti Code
  - [x] Test para Magic Numbers
  - [x] Test para Dead Code
- [x] Actualizar `AI_CONTEXT.md` template

### Mejora 6: Seguridad Mejorada (3-4h)
- [x] Modificar `src/ai_context_core/analyzer/issues.py`
- [x] Agregar detecciones:
  - [x] Llamadas peligrosas (`eval`, `exec`, `pickle.loads`, etc.)
  - [x] SQL injection (f-strings con SELECT)
  - [x] Excepciones genéricas (`except:`)
  - [x] `assert` en producción
- [x] Crear `tests/test_security_enhanced.py`
  - [x] Test para cada tipo de detección
- [x] Actualizar documentación de seguridad

---

## Fase 2: Análisis Avanzado (19-22 horas)

### Mejora 2: Patrones de Diseño (8h)
- [x] Crear `src/ai_context_core/analyzer/patterns.py`
- [ ] Implementar detectores de patrones:
  - [x] `detect_singleton()` - Confianza 90%
  - [x] `detect_factory()` - Confianza 70%
  - [x] `detect_observer_pattern()` - Confianza 85%
  - [x] `detect_strategy_pattern()` - Confianza 75%
  - [x] `detect_decorator_pattern()` - Confianza 80%
- [x] Integrar en `engine.py` (`_aggregate_results()`)
- [x] Reemplazar `"patterns": {}` con resultados reales
- [x] Crear `tests/test_patterns.py`
  - [x] Test para cada patrón
  - [x] Test para niveles de confianza
- [x] Crear `docs/PATTERNS_DETECTION.md`

### Mejora 4: Dependencias Mejoradas (6-8h)
- [x] Modificar `src/ai_context_core/analyzer/dependencies.py`
- [x] Implementar funciones:
  - [x] `detect_circular_dependencies()` - Algoritmo de grafos (Optimizado)
  - [x] `calculate_coupling_metrics()` - CBO
  - [x] `find_unused_imports()` - Análisis de referencias (en ast_utils)
- [x] Agregar métricas al reporte
- [x] Crear `tests/test_dependencies_advanced.py`
- [x] Actualizar visualización de grafos en reportes (insights agregados)

### Mejora 10: Multi-Framework (5-6h)
- [x] Modificar `src/ai_context_core/analyzer/ast_utils.py`
- [x] Implementar `detect_framework_entry_points()` (Integrado en `is_entry_point`)
- [x] Agregar soporte para:
  - [x] Django (`settings.py`, `INSTALLED_APPS`, `urlpatterns`, `wsgi/asgi application`)
  - [x] Flask (`@app.route`, `app = Flask(...)`)
  - [x] FastAPI (`@app.get`, `@app.post`, `app = FastAPI(...)`)
  - [x] Click (`@click.command`)
- [x] Integrar con detección de entry points
- [x] Crear tests para cada framework
- [x] Documentar frameworks soportados

---

## Fase 3: Métricas y Contexto (13-15 horas)

### Mejora 7: Métricas Avanzadas (5-6h)
- [ ] Modificar `src/ai_context_core/analyzer/metrics.py`
- [ ] Implementar funciones:
  - [ ] `calculate_maintainability_index()` - Fórmula MI
  - [ ] `estimate_technical_debt_hours()` - Estimación en horas
  - [ ] `compare_with_history()` - Tendencias
- [ ] Crear `.ai-context/metrics_history.json` para tracking
- [ ] Agregar métricas al reporte
- [ ] Crear `tests/test_metrics_advanced.py`
- [ ] Crear `docs/METRICS_GUIDE.md`

### Mejora 9: Git Integration (6-7h)
- [ ] Crear `src/ai_context_core/analyzer/git_analysis.py`
- [ ] Implementar funciones:
  - [ ] `analyze_git_hotspots()` - Archivos con más commits
  - [ ] `calculate_churn_rate()` - Frecuencia de cambios
  - [ ] `get_file_ownership()` - Autores principales
- [ ] Integrar en `engine.py` (opcional si es repo Git)
- [ ] Agregar sección "Git Insights" en reportes
- [ ] Crear `tests/test_git_analysis.py` (requiere repo de prueba)
- [ ] Documentar requisitos de Git

### Mejora 3: Config Explícita (2h)
- [ ] Modificar `src/ai_context_core/config/loader.py`
- [ ] Agregar soporte para campo `entry_points` en config
- [ ] Actualizar schema de configuración
- [ ] Modificar `engine.py` para combinar entry points
- [ ] Crear ejemplo en documentación
- [ ] Agregar test de configuración

---

## Fase 4: Optimización y Futuro (26-33 horas)

### Mejora 12: Cache Incremental (8-10h)
- [ ] Crear `src/ai_context_core/analyzer/cache.py`
- [ ] Implementar sistema de hash de archivos
- [ ] Implementar `analyze_with_cache()`
- [ ] Agregar opción CLI `--use-cache`
- [ ] Crear tests de performance
- [ ] Documentar mejoras de velocidad

### Mejora 8: Diagramas Arquitectónicos (8-10h)
- [ ] Modificar `src/ai_context_core/analyzer/reporting.py`
- [ ] Implementar generación de:
  - [ ] Diagrama de clases (Mermaid)
  - [ ] Diagrama de componentes (Mermaid)
  - [ ] Heatmap de complejidad
- [ ] Agregar diagramas a `AI_CONTEXT.md`
- [ ] Crear tests de generación
- [ ] Documentar sintaxis Mermaid

### Mejora 11: Múltiples Formatos (6-8h)
- [ ] Crear directorio `src/ai_context_core/exporters/`
- [ ] Implementar exportadores:
  - [ ] `html_exporter.py` - HTML con Chart.js
  - [ ] `pdf_exporter.py` - PDF con reportlab
  - [ ] `sarif_exporter.py` - SARIF para VSCode
  - [ ] `badge_exporter.py` - SVG badges
- [ ] Agregar opción CLI `--format`
- [ ] Crear tests para cada formato
- [ ] Documentar formatos disponibles

### Mejora 13: IA Accionable (12-15h)
- [ ] Crear `src/ai_context_core/analyzer/ai_recommendations.py`
- [ ] Implementar integración con LLMs
- [ ] Implementar `generate_ai_recommendations()`
- [ ] Agregar casos de uso:
  - [ ] Sugerencias de refactoring
  - [ ] Generación de docstrings
  - [ ] Mejora de nombres de variables
- [ ] Configurar API keys y modelos
- [ ] Crear tests (mocked)
- [ ] Documentar uso de IA

---

## Testing General

### Cobertura de Tests
- [ ] Fase 1: Alcanzar >75% cobertura
- [ ] Fase 2: Alcanzar >80% cobertura
- [ ] Fase 3: Alcanzar >85% cobertura
- [ ] Fase 4: Mantener >85% cobertura

### CI/CD
- [ ] Configurar GitHub Actions
- [ ] Agregar workflow de tests automáticos
- [ ] Agregar workflow de coverage reporting
- [ ] Configurar pre-commit hooks

---

## Documentación

### Documentos Nuevos
- [ ] `docs/PATTERNS_DETECTION.md`
- [ ] `docs/ANTIPATTERNS_GUIDE.md`
- [ ] `docs/SECURITY_ANALYSIS.md`
- [ ] `docs/METRICS_GUIDE.md`

### Documentos a Actualizar
- [ ] `README.md` - Ejemplos de nuevas features
- [ ] `docs/user_guide/QUICK_START.md` - Nuevas configuraciones
- [ ] `docs/development/ARCHITECTURE.md` - Nuevos módulos
- [ ] `CHANGELOG.md` - Después de cada fase

---

## Releases

### Versionado
- [ ] Fase 1 completada → Release v1.1.0
- [ ] Fase 2 completada → Release v1.2.0
- [ ] Fase 3 completada → Release v1.3.0
- [ ] Fase 4 completada → Release v2.0.0

### Proceso de Release
- [ ] Actualizar `CHANGELOG.md`
- [ ] Actualizar versión en `pyproject.toml`
- [ ] Crear tag Git
- [ ] Build con `uv build`
- [ ] Publicar en PyPI (si aplica)
- [ ] Crear release notes en GitHub

---

## Notas

> **Prioridad Actual**: Comenzar con Fase 2 (Mejoras 2, 4, 10)
> 
> **Próximo Paso**: Implementar detección de patrones de diseño en `src/ai_context_core/analyzer/patterns.py`
