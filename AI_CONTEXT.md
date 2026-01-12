# CONTEXTO PARA IA - ai-context-core
Generado automáticamente por Ai-Context-Core
## 📁 ESTRUCTURA DEL PROYECTO

./
    .gitignore
    AI_CONTEXT.md
    CHANGELOG.md
    PROJECT_SUMMARY.md
    README.md
    debug_issues.py
    project_context.json
    ... (+1 más)
    src/
        ai_context_core/
            __init__.py
            cli.py
            analyzer/
                ast_utils.py
                dependencies.py
                engine.py
                fs_utils.py
                issues.py
                metrics.py
                reporting.py
            context/
                manager.py
            config/
                defaults.yaml
                loader.py
                profiles/
                    qgis.yaml
            templates/
                initial_prompt.md
                workflows/
                    cierra-sesion.md
                    crea-el-comit.md
                    create-commit.md
                    end-session.md
                    inicia-sesion.md
                    start-session.md
                prompts/
        ai_context_core.egg-info/
            PKG-INFO
            SOURCES.txt
            dependency_links.txt
            entry_points.txt
            requires.txt
            top_level.txt
    docs/
        development/
            ARCHITEC


## 🎯 PUNTOS DE ENTRADA
- `src/ai_context_core/cli.py`


## 🏗️ PATRONES DETECTADOS

No se detectaron patrones de diseño claros.
## 📈 COMPLEJIDAD Y MÉTRICAS
- **Módulos totales**: 12
- **Líneas de código**: 2,064
- **Funciones**: 67
- **Clases**: 4
- **Complejidad promedio**: 32.1
- **Módulos más complejos**: src/ai_context_core/analyzer/ast_utils.py, src/ai_context_core/analyzer/fs_utils.py, src/ai_context_core/analyzer/dependencies.py

## 🔗 DEPENDENCIAS PRINCIPALES

### Third Party (más frecuentes):
- `config` (2 imports)
- `ai_context_core` (1 imports)
- `analyzer` (1 imports)
- `ast` (1 imports)
- `ast_utils` (1 imports)
- `click` (1 imports)
- `concurrent` (1 imports)
- `context` (1 imports)
- `dependencies` (1 imports)
- `fnmatch` (1 imports)
- `fs_utils` (1 imports)
- `issues` (1 imports)
- `metrics` (1 imports)
- `mmap` (1 imports)
- `reporting` (1 imports)

## 💡 RECOMENDACIONES DE OPTIMIZACIÓN

### src/ai_context_core/analyzer/ast_utils.py (Prioridad: ALTA)
- **refactorizacion_complejidad**: Alta complejidad (61) con 10 funciones

### src/ai_context_core/analyzer/issues.py (Prioridad: ALTA)
- **funciones_demasiado_largas**: Funciones muy largas (promedio 58.6 líneas/función)

### src/ai_context_core/analyzer/fs_utils.py (Prioridad: ALTA)
- **refactorizacion_complejidad**: Alta complejidad (61) con 15 funciones

### src/ai_context_core/context/manager.py (Prioridad: ALTA)
- **refactorizacion_complejidad**: Alta complejidad (33) con 12 funciones

### src/ai_context_core/analyzer/reporting.py (Prioridad: ALTA)
- **funciones_demasiado_largas**: Funciones muy largas (promedio 78.7 líneas/función)

## 🕸️  ESTRUCTURA DE DEPENDENCIAS
- **Nodos**: 12
- **Aristas**: 0
- **Densidad**: 0.000
- **Grafo acíclico**: Sí
- **Componentes conectados**: 12

## 🕸️ DIAGRAMA DE DEPENDENCIAS (Conceptuall)
```mermaid
graph TD
```

## 🔑 PALABRAS CLAVE DEL PROYECTO
- **Tecnologías**: .py, .pyc, .md, .sample, .txt, .json, .typed, .bat
- **Patrones**: 
