# Próximos Pasos - ai-context-core

**Última actualización**: 2026-01-25

## Estado Actual

✅ **Análisis completado**
- Reporte de mejoras analizado: [AiContextCore_Analysis_Report.md](file:///home/jmbernales/qgispluginsdev/ai-context-core/docs/AiContextCore_Analysis_Report.md)
- Plan de implementación creado: 13 mejoras en 4 fases
- Tests: 7/7 pasando ✅
- Quality Score: 67.5/100

## 🎯 Nuevo Roadmap de Mejoras

Basado en análisis exhaustivo del código, se identificaron **13 mejoras críticas** organizadas en 4 fases.

### Fase 1: Correcciones Críticas (11-15h) 🔥 ALTA PRIORIDAD

#### 1. Entry Points Detection (4-6h)
**Problema**: Solo detecta `if __name__ == "__main__"`, ignora QGIS plugins y frameworks web.

**Solución**: Ampliar `ast_utils.py` para detectar:
- `classFactory(iface)` para QGIS
- `@click.command` para Click
- `@app.route` para Flask
- `@app.get/post` para FastAPI

**Archivos**: `src/ai_context_core/analyzer/ast_utils.py`, `engine.py`

#### 2. Anti-Patrones (4-5h)
**Nuevo módulo**: `src/ai_context_core/analyzer/antipatterns.py`

Detectar:
- God Object (clases con >20 métodos)
- Spaghetti Code (funciones CC >25)
- Magic Numbers (constantes hardcodeadas)
- Dead Code (código nunca importado)

#### 3. Seguridad Mejorada (3-4h)
**Ampliar**: `src/ai_context_core/analyzer/issues.py`

Nuevas detecciones:
- Llamadas peligrosas: `eval`, `exec`, `pickle.loads`, `os.system`
- SQL injection: f-strings con "SELECT"
- Excepciones genéricas: `except:` sin tipo
- `assert` en código de producción

---

### Fase 2: Análisis Avanzado (19-22h) 🔥 ALTA PRIORIDAD

#### 4. Patrones de Diseño (8h)
**Nuevo módulo**: `src/ai_context_core/analyzer/patterns.py`

Detectar patrones:
- Singleton (confianza 90%)
- Factory (confianza 70%)
- Observer (confianza 85%)
- Strategy (confianza 75%)
- Decorator (confianza 80%)

**Beneficio**: Información arquitectónica rica para LLMs y desarrolladores

#### 5. Dependencias Mejoradas (6-8h)
**Ampliar**: `src/ai_context_core/analyzer/dependencies.py`

Nuevas funcionalidades:
- Detectar dependencias circulares
- Calcular métricas de acoplamiento (CBO)
- Identificar imports no utilizados

#### 6. Multi-Framework (5-6h)
**Ampliar**: `src/ai_context_core/analyzer/ast_utils.py`

Soporte para:
- Django (`settings.py`, `INSTALLED_APPS`)
- Flask (`@app.route`)
- FastAPI (`@app.get`, `@app.post`)
- Click (`@click.command`)

---

### Fase 3: Métricas y Contexto (13-15h) ⚡ MEDIA PRIORIDAD

#### 7. Métricas Avanzadas (5-6h)
**Ampliar**: `src/ai_context_core/analyzer/metrics.py`

Nuevas métricas:
- Índice de Mantenibilidad (MI)
- Deuda Técnica en Horas
- Tendencia de Calidad (histórico)

#### 8. Git Integration (6-7h)
**Nuevo módulo**: `src/ai_context_core/analyzer/git_analysis.py`

Análisis:
- Hotspots (archivos con más commits)
- Churn Rate (frecuencia de cambios)
- Ownership (autores principales)

#### 9. Config Explícita (2h)
**Ampliar**: `src/ai_context_core/config/loader.py`

Permitir definir entry points manualmente en `.ai-context/config.yaml`

---

### Fase 4: Optimización (26-33h) 🟢 BAJA PRIORIDAD / 🚀 FUTURO

- Cache Incremental (8-10h)
- Diagramas Arquitectónicos (8-10h)
- Múltiples Formatos de Export (6-8h)
- IA Accionable (12-15h)

---

## Comando para Retomar

```bash
/inicia-sesion
```

## Próximos Pasos Inmediatos

### Opción A: Comenzar Fase 1 (Recomendado)
```bash
# 1. Crear rama para desarrollo
git checkout -b feature/phase1-critical-fixes

# 2. Comenzar con Entry Points Detection
# Editar: src/ai_context_core/analyzer/ast_utils.py
```

### Opción B: Configurar CI/CD primero
```bash
# Crear .github/workflows/ci.yml
# Configurar tests automáticos antes de implementar mejoras
```

### Opción C: Corregir Docker Issue
```bash
# Investigar problema con `make docker-test`
# Error: unknown flag: --rm
```

---

## Contexto de la Sesión Actual

**Tema**: `analysis_report_implementation_planning`

**Logros**:
- ✅ Análisis completo del reporte de mejoras
- ✅ Plan de implementación creado (13 mejoras, 4 fases)
- ✅ Task breakdown detallado
- ✅ Timeline estimado (6-7 semanas para fases 1-3)

**Archivos clave creados**:
- `.gemini/antigravity/brain/.../implementation_plan.md`
- `.gemini/antigravity/brain/.../task.md`

**Métricas actuales**:
- Tests: 7/7 ✅
- Quality Score: 67.5/100
- LOC: 3,196
- Módulos con CC >15: 6

**Deuda técnica identificada**:
- `fs_utils.py`: CC 52
- `ast_utils.py`: CC 51
- `dependencies.py`: CC 44
- `reporting.py`: CC 38
- `issues.py`: CC 35
- `context/manager.py`: CC 28

---

## Referencias

- [Analysis Report](file:///home/jmbernales/qgispluginsdev/ai-context-core/docs/AiContextCore_Analysis_Report.md)
- [Implementation Plan](file:///home/jmbernales/qgispluginsdev/ai-context-core/docs/implementation_plan_improvements.md)
- [Task Breakdown](file:///home/jmbernales/qgispluginsdev/ai-context-core/.agent/task_improvements.md)
- [Executive Summary](file:///home/jmbernales/qgispluginsdev/ai-context-core/docs/executive_summary_improvements.md)

---

## Decisión Requerida

> **¿Qué deseas hacer a continuación?**
> 
> 1. **Comenzar Fase 1** - Implementar Entry Points Detection
> 2. **Configurar CI/CD** - Preparar infraestructura de testing
> 3. **Corregir Docker** - Solucionar issue con `make docker-test`
> 4. **Otra tarea** - Especificar
