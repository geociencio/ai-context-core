# Plan de Implementación: Fase 8 - Soporte Extendido de QGIS (Parte 1)

Este hito busca robustecer el análisis de plugins de QGIS detectando incompatibilidades de API y validando recursos esenciales más allá del código Python.

## Cambios Propuestos

### Componente: Visitors (Análisis AST)

#### [NEW] [qgis_api.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/visitors/qgis_api.py)
- Implementar `QGISApiChecker` para detectar:
  - **APIs Obsoletas (QGIS 3.x)**: `QgsMapLayerRegistry`, `QGis.unit_type`, `setDataProvider`.
  - **QGIS 4.x Readiness**: 
    - Bloqueo estricto de `PyQt5` (forzar migración a `PyQt6`).
    - Detección de uso de enumeraciones antiguas de Qt (migración a Enums de Python/Qt6).
    - Alertas sobre señales y slots con sintaxis legacy `SIGNAL()`/`SLOT()` (crítico para Qt6).
  - **Mejores Prácticas**: Uso de `QgsSettings` vs `QSettings`, `QgsProject.instance()` vs globales.

#### [MODIFY] [qgis_visitor.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/visitors/qgis_visitor.py)
- Registrar `QGISApiChecker` en la lista de chequeos activos.
- Inicializar `results` con `api_compatibility_issues`.

### Componente: Providers (Recursos Externos)

#### [NEW] [qgis_resources.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/providers/qgis_resources.py)
- Implementar extractor de metadatos de `plugin.xml`.
- Validar:
  - Correspondencia de versión entre `metadata.txt` y `plugin.xml` (si aplica).
  - Existencia de archivos de recursos declarados en `.qrc`.

## Parte 2: plugin.xml e Inconsistencias

### [MODIFY] [qgis_resources.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/providers/qgis_resources.py)
Añadir soporte para:
- Parsea `plugin.xml` usando `xml.etree.ElementTree`.
- Detecta inconsistencias (Nombre, Versión) entre `metadata.txt` y `plugin.xml`.
- Añade issues al objeto de resultados si hay discrepancias.

### [MODIFY] [aggregator_qgis.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/builders/aggregator_qgis.py)
- Reflejar hallazgos de `plugin.xml` en el reporte.
- Penalizar el `Compliance Score` si hay inconsistencias críticas.

## Verificación Plan
- Crear mock de `plugin.xml` con versión discrepante.
- Validar que el reporte señale la inconsistencia.

### Componente: Builders (Agregación)

#### [MODIFY] [aggregator_qgis.py](file:///home/jmbernales/qgispluginsdev/ai-context-core/src/ai_context_core/analyzer/builders/aggregator_qgis.py)
- Incorporar hallazgos de API y recursos en el cálculo del `compliance_score`.
- Actualizar el resumen visual (`QGISSummarizer`) para mostrar alertas de API.

## Plan de Verificación

### Pruebas Automatizadas
- Crear `tests/test_qgis_api_checker.py` con fragmentos de código que usen APIs obsoletas.
- Crear `tests/test_qgis_resources.py` con mocks de `plugin.xml` y `.qrc`.

```bash
uv run pytest tests/test_qgis_api_checker.py
uv run pytest tests/test_qgis_resources.py
```

### Verificación Manual
- Ejecutar `ai-ctx qgis` sobre un plugin de QGIS conocido por tener prácticas antiguas.
