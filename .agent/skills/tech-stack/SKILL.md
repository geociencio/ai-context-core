---
name: tech-stack
description: Guía de la pila tecnológica, gestión de dependencias con uv y herramientas de calidad.
---

# Tech Stack

Define el ecosistema de herramientas y librerías que sustentan el desarrollo de `ai-context-core`.

## Cuándo usar este skill
- Al instalar nuevas dependencias.
- Al configurar el entorno de desarrollo.
- Al ejecutar herramientas de linting o formateo.
- Al verificar la compatibilidad de versiones de Python.

## Grado de Libertad
- **Estricto**: El uso de `uv` como gestor de paquetes es obligatorio.

## Inputs necesarios
- `pyproject.toml` para verificar configuración.

## Workflow
1. **Gestión**: Usar `uv` para cualquier operación de paquetes.
2. **Sincronización**: Mantener el entorno al día con `uv sync`.
3. **Calidad**: Ejecutar `ruff` para validación estática.

## Instrucciones y Reglas

### 1. Tecnologías Base
- **Python**: >= 3.9
- **Gestor**: `uv` (reemplaza a pip/poetry).
- **Calidad**: `ruff` (configurado en `pyproject.toml`).

### 2. Gestión de Dependencias
- **Añadir**: `uv add [package]`
- **Desarrollo**: `uv add --dev [package]`
- **Instalar**: `uv sync`

### 3. Calidad de Código
- **Lint**: `uv run ruff check .`
- **Formateo**: `uv run ruff format .` (o `uv run black .` según preferencia de usuario).

## Output (formato exacto)
Un entorno de desarrollo coherente y dependencias correctamente registradas.

## Lista de Verificación de Calidad
- [ ] ¿Se prioriza el uso de `uv`?
- [ ] ¿Se mencionan los comandos exactos de ruff/black?
- [ ] ¿La versión de Python es correcta?
- [ ] ¿Se ha evitado el uso de herramientas obsoletas (pip/venv)?
- [ ] ¿El documento está en español?
