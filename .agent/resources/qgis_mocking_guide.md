# Recurso Técnico: Mocking de QGIS/PyQt

Guía rápida para aislar dependencias de QGIS en pruebas unitarias dentro de `ai-context-core`.

## Propósito
Permitir que los tests se ejecuten en entornos sin QGIS instalado (como contenedores de CI estándar o máquinas locales de desarrollo sin dependencias pesadas).

## Estrategia de Mocking

### 1. Mock de Geometrías
Cuando pruebes lógica que extrae datos de geometrías, no instancies `QgsGeometry`. Usa `unittest.mock.MagicMock`.

```python
from unittest.mock import MagicMock

def test_geometry_extraction():
    mock_geom = MagicMock()
    mock_geom.asWkt.return_value = "POINT(0 0)"
    # Tu lógica aquí
```

### 2. Simulación de Capas (QgsVectorLayer)
Usa diccionarios o mocks que simulen la interfaz de la capa.

```python
mock_layer = MagicMock()
mock_layer.name.return_value = "Capa_Test"
mock_layer.featureCount.return_value = 10
```

### 3. Manejo de Imports Fallidos
Para que los tests no exploten en entornos sin QGIS, usa bloques `try-except` en el código fuente o mocks dinámicos en los tests.

```python
try:
    from qgis.core import QgsGeometry
except ImportError:
    QgsGeometry = MagicMock()
```

## Reglas de Oro
1. **Aislamiento Total**: Un test de `analyzer` no debería depender de un binario de QGIS.
2. **Interfaces**: Mockea solo lo que necesitas (comportamiento), no toda la clase.
3. **Persistencia**: Si creas un mock complejo, guárdalo en `tests/conftest.py` como un fixture de pytest.
