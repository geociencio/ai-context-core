# Próximos Pasos - ai-context-core

**Última actualización**: 2026-01-25

## Estado Actual

✅ **Fase 1 Completada**
- **Entry Points**: Soporte para QGIS, Click, Flask, FastAPI implementado.
- **Anti-Patrones**: Detección de God Object, Spaghetti Code, etc. activa.
- **Seguridad**: Escaneo mejorado con AST.
- **Validación**: 25/25 tests pasando (Coverage ~70%) ✅
- **Docker**: Entorno de testing corregido y funcional.

## 🎯 Roadmap de Mejoras

### Fase 1: Correcciones Críticas (✅ COMPLETADO)
- [x] Entry Points Detection (QGIS, Click, Web)
- [x] Anti-Patrones (God Object, Magic Numbers, etc.)
- [x] Seguridad Mejorada (AST-based, SQLi, Asserts)
- [x] Corrección Docker Testing

### Fase 2: Análisis Avanzado (19-22h) 🔥 ALTA PRIORIDAD (SIGUIENTE)

#### 4. Patrones de Diseño (8h)
**Nuevo módulo**: `src/ai_context_core/analyzer/patterns.py`

Detectar patrones:
- Singleton (confianza 90%)
- Factory (confianza 70%)
- Observer (confianza 85%)
- Strategy (confianza 75%)
- Decorator (confianza 80%)

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
- Configuración explícita en frameworks

### Fase 3: Métricas y Contexto (13-15h) ⚡ MEDIA PRIORIDAD

#### 7. Métricas Avanzadas (5-6h)
- Índice de Mantenibilidad (MI)
- Deuda Técnica en Horas

#### 8. Git Integration (6-7h)
- Hotspots, Churn Rate, Ownership

#### 9. Config Explícita (2h)
- Definición manual de entry points

### Fase 4: Optimización (26-33h) 🟢 BAJA PRIORIDAD

- Cache Incremental, Diagramas, IA Accionable

---

## Comando para Retomar

```bash
/inicia-sesion
```

## Próximos Pasos Inmediatos

1.  **Merge Phase 1**: Fusionar rama `feature/phase1-improvements` a `main`.
2.  **Iniciar Fase 2**: Crear rama `feature/phase2-advanced-analysis`.
3.  **Implementar Patrones de Diseño**: Comenzar con `src/ai_context_core/analyzer/patterns.py`.

---

## Documentos de Referencia
- [Session Report Phase 1](file:///home/jmbernales/qgispluginsdev/ai-context-core/docs/sessions/session_2026-01-25_phase1_completion.md)
- [Analysis Report](file:///home/jmbernales/qgispluginsdev/ai-context-core/docs/AiContextCore_Analysis_Report.md)
