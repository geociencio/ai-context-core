# 0004. Estrategia de Detección Heterogénea de Entry Points

**Estado**: Aceptado

**Fecha**: 2026-01-25

**Autores**: Equipo ai-context-core

**Decisores**: Equipo de desarrollo

---

## Contexto y Problema

Identificar los puntos de entrada (Entry Points) de un proyecto es vital para entender su arquitectura. Sin embargo, cada framework utiliza mecanismos diferentes:
- QGIS: Firmas de funciones específicas (`classFactory`).
- Click: Decoradores propietarios (`@click.command`).
- Flask/FastAPI: Decoradores y asignaciones de variables de aplicación.
- Django: Archivos específicos y variables mágicas (`urlpatterns`, `INSTALLED_APPS`).

## Factores de Decisión

- **Bajo Acoplamiento**: El analizador no debe requerir que los frameworks estén instalados.
- **Precisión**: No debe reportar archivos auxiliares como entry points.
- **Mantenibilidad**: La lógica de detección debe estar centralizada.

## Opciones Consideradas

### Opción 1: Detección por Nombres de Archivo
**Descripción**: Confiar en nombres como `main.py`, `app.py`, `wsgi.py`.
- **Pros**: Extremadamente rápido.
- **Contras**: Muy impreciso; muchos proyectos no siguen estas convenciones.

### Opción 2: Detección Heterogénea por Patrones AST (Elegida)
**Descripción**: Analizar el interior de cada archivo buscando firmas específicas de frameworks (decoradores, nombres de variables en el scope global, nombres de argumentos en funciones).
- **Pros**: Muy preciso, independiente del nombre del archivo, detecta múltiples frameworks simultáneamente.
- **Contras**: Requiere un caminante de AST robusto y conocimiento profundo de las APIs de los frameworks.

## Decisión

Implementar una función modular `is_entry_point` en `ast_utils.py` que aplique una batería de tests sobre el módulo analizado:
1. **Guarda de main**: `if __name__ == "__main__"`.
2. **Firmas de Funciones**: Ej: `def classFactory(iface)`.
3. **Firmas de Decoradores**: Ej: `@app.route`, `@click.command`.
4. **Firmas de Variables**: Ej: `urlpatterns = [...]`, `application = get_wsgi_application()`.

## Consecuencias

### Positivas
- ✅ **Soporte Universal**: El analizador entiende proyectos web, plugins y CLIs automáticamente.
- ✅ **Cero Dependencias**: La detección es puramente textual/estructural (AST), sin importar librerías.

### Negativas
- ❌ **Complejidad AST**: La lógica debe manejar casos como decoradores llamados vs no llamados (`@app.get` vs `@app.get()`).
