---
name: project-context
description: Resumen del propósito, arquitectura y estructura del proyecto ai-context-core.
---

# Project Context

Define el núcleo de conocimiento sobre `ai-context-core`: su arquitectura, componentes clave y flujo de operación.

## Cuándo usar este skill
- Al iniciar sesión en el proyecto.
- Al explicar la arquitectura a un nuevo colaborador (humano o IA).
- Cuando haya dudas sobre la ubicación de archivos o responsabilidades de módulos.
- Para orientar el desarrollo hacia las metas del proyecto.

## Grado de Libertad
- **Guiado**: La estructura del proyecto y los comandos son fijos, pero la interpretación de los flujos es abierta.

## Inputs necesarios
- Acceso a la estructura de directorios y archivos de configuración (`pyproject.toml`).

## Workflow
1. **Identificación**: Localizar los componentes principales (`src`, `docs`, `.agent`).
2. **Contextualización**: Entender la relación entre el análisis AST y los perfiles.
3. **Persistencia**: Mantener actualizados los archivos `.ai-context`.

## Instrucciones y Reglas

### 1. Propósito Central
- `ai-context-core` es el motor central para flujos de trabajo de codificación asistida por IA.
- Proporciona análisis profundo de AST y gestión de contexto basada en perfiles (Python genérico, plugins de QGIS).

### 2. Estructura del Proyecto
- `src/ai_context_core`: Fuente principal del paquete.
- `docs/`: Documentación técnica.
- `.agent/`: Configuración del framework agentic (skills, workflows).
- `pyproject.toml`: Configuración global y dependencias (uv).

### 3. Comandos Críticos
- `ai-ctx init --profile [profile]`: Inicializa un nuevo proyecto.
- `ai-ctx analyze`: Actualiza el contexto manualmente.

## Output (formato exacto)
Información actualizada y veraz sobre el estado y estructura del proyecto.

## Lista de Verificación de Calidad
- [ ] ¿Se menciona la arquitectura basada en perfiles?
- [ ] ¿La descripción de la estructura es precisa?
- [ ] ¿Se han incluido los comandos de terminal correctos?
- [ ] ¿El tono es operativo y profesional?
- [ ] ¿Se referencian correctamente las rutas del workspace?
