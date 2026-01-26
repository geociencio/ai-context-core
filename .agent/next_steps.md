# Próximos Pasos - ai-context-core

**Última actualización**: 2026-01-25

## Estado Actual

✅ **Fase 2 Completada**
- **Entry Points**: Soporte ampliado para Django, Flask, FastAPI, Click.
- **Patrones**: Singleton, Factory, Observer, Strategy, Decorator activos.
- **Dependencias**: Cálculo de acoplamiento (CBO) y detección de imports no usados.
- **Validación**: 40+ tests pasando (incluyendo nuevos de patrones y dependencias) ✅

## 🎯 Roadmap de Mejoras

### Fase 1: Correcciones Críticas (✅ COMPLETADO)
- [x] Entry Points Detection (QGIS, Click, Web)
- [x] Anti-Patrones (God Object, Magic Numbers, etc.)
- [x] Seguridad Mejorada (AST-based, SQLi, Asserts)
- [x] Corrección Docker Testing

### Fase 2: Análisis Avanzado (✅ COMPLETADO)
- [x] Patrones de Diseño (Singleton, Factory, Observer, Strategy, Decorator)
- [x] Dependencias Mejoradas (Acoplamiento CBO, Unused Imports)
- [x] Multi-Framework (Django, Flask, FastAPI, Click)

### Fase 3: Métricas y Contexto (13-15h) ⚡ SIGUIENTE

#### 7. Métricas Avanzadas (5-6h)
**Ampliar**: `src/ai_context_core/analyzer/metrics.py`
- Índice de Mantenibilidad (MI)
- Deuda Técnica en Horas
- Tendencia de Calidad (histórico)

#### 8. Git Integration (6-7h)
**Nuevo módulo**: `src/ai_context_core/analyzer/git_analysis.py`
- Hotspots, Churn Rate, Ownership

#### 9. Config Explícita (2h)
- Definición manual de entry points en config.yaml

### Fase 4: Optimización (26-33h) 🟢 BAJA PRIORIDAD
- Cache Incremental, Diagramas, IA Accionable

---

## Comando para Retomar

```bash
/inicia-sesion
```

## Próximos Pasos Inmediatos

1.  **Merge Phase 2**: Fusionar rama `feature/phase2-advanced-analysis` a `main`.
2.  **Iniciar Fase 3**: Crear rama `feature/phase3-metrics-and-git`.
3.  **Implementar Métricas Avanzadas**: Comenzar con el Índice de Mantenibilidad en `src/ai_context_core/analyzer/metrics.py`.

---

## Documentos de Referencia
- [Design Patterns Guide](file:///home/jmbernales/qgispluginsdev/ai-context-core/docs/PATTERNS_DETECTION.md)
- [Session Report Phase 1](file:///home/jmbernales/qgispluginsdev/ai-context-core/docs/sessions/session_2026-01-25_phase1_completion.md)
- [Analysis Report](file:///home/jmbernales/qgispluginsdev/ai-context-core/docs/AiContextCore_Analysis_Report.md)
