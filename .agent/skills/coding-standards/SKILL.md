---
name: coding-standards
description: Estándares de codificación del proyecto, enfocados en el uso de pathlib, docstrings de Google y tipado estricto.
---

# Coding Standards

Establece las reglas técnicas para mantener un código limpio, legible y compatible con el ecosistema Python moderno y QGIS.

## Cuándo usar este skill
- Al escribir nuevas funciones o clases.
- Al refactorizar código existente.
- Al realizar auditorías de calidad de código.
- Al integrar nuevas librerías o dependencias.

## Grado de Libertad
- **Estricto**: El manejo de rutas (`pathlib`) y el formato de docstrings son obligatorios.

## Inputs necesarios
- Código Python para analizar o escribir.

## Workflow
1. **Validación de Rutas**: Asegurar que no existan llamadas a `os.path`.
2. **Documentación**: Aplicar el formato Google Docstrings a cada nodo público.
3. **Tipado**: Verificar que todos los argumentos y retornos tengan Type Hints.
4. **Compatibilidad**: Validar que las rutas se conviertan a `str` si se pasan a APIs de Qt/QGIS.

## Instrucciones y Reglas

### 1. Manejo de Rutas (Pathlib)
- **Regla de Oro**: Usa siempre `pathlib.Path`.
- **Hacer**: `Path(dir) / file`
- **Evitar**: `os.path.join(dir, file)`
- **Conversión**: Usa `str(path_obj)` al interactuar con QGIS/Qt si la API no acepta objetos Path.

### 2. Documentación (Google Style)
- Los docstrings deben seguir la [Guía de Estilo de Google](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
- Ejemplo:
```python
def example_function(param1: int) -> bool:
    """Summary of the function.

    Args:
        param1: Description of param1.

    Returns:
        True if successful, False otherwise.
    """
    return True
```

### 3. Tipado Estricto
- Usa Type Hints en todos los argumentos y valores de retorno.
- Preferir tipos integrados (Python 3.9+).

## Output (formato exacto)
Código Python formateado con `black` y validado según estas reglas.

## Lista de Verificación de Calidad
- [ ] ¿Se usa `pathlib` exclusivamente para rutas?
- [ ] ¿Todos los docstrings siguen el formato Google?
- [ ] ¿Existen Type Hints para cada entrada y salida?
- [ ] ¿La documentación está en el idioma correcto (Código: EN, Skill: ES)?
- [ ] ¿Se respeta el contexto del proyecto (@project-context)?
