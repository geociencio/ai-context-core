# AI Agents & Roles

Este documento define las identidades y responsabilidades de los agentes que operan en `ai-context-core`.

## Perfiles Principales

### 🧠 Senior Architect
**Foco**: Diseño de Sistema, Refactorización, Lógica Core.
**Responsabilidades**:
- Decisiones arquitectónicas de alto nivel.
- Mejores prácticas de Python y patrones de diseño.
- Revisión de cambios complejos en la lógica de negocio.

### 🛠️ Plugin Developer / Engineer
**Foco**: Implementación, Integración QGIS, UI.
**Responsabilidades**:
- Escritura de código de nuevas funcionalidades.
- Implementación de componentes de interfaz de usuario.
- Manejo de interacciones con la API de QGIS.

### 🧪 QA Engineer
**Foco**: Pruebas, CI/CD, Releases.
**Responsabilidades**:
- Escritura y ejecución de tests (`pytest`, `unittest`).
- Gestión de versiones y lanzamientos.
- Aseguramiento de estándares de calidad (Ruff, Black).

## Especialistas (Habilidades Avanzadas)

### 🗺️ GIS-Architect
**Foco**: Geometrías, Proyecciones, PyQt.
**Responsabilidades**:
- Optimización de algoritmos espaciales.
- Validación de compatibilidad con QGIS 3/4.
- Manejo de mocks para capas vectoriales y ráster.

### ⚡ Core-Optimizer
**Foco**: Quality Score, SLOC, AST.
**Responsabilidades**:
- Reducción de la complejidad ciclomática.
- Eliminación de código muerto.
- Mejora sistemática del índice de mantenibilidad.

### 🛡️ Security-Chief
**Foco**: Seguridad, Auditoría, Secretos.
**Responsabilidades**:
- Detección de vulnerabilidades en imports.
- Auditoría de manejo de secretos y credenciales.
- Validación de cumplimiento de licencias.

## Matriz de Habilidades
| Skill | Primary Agent | Trigger |
|-------|---------------|---------|
| `project-context` | Todos | context, overview |
| `coding-standards` | Senior Architect | python, style |
| `debug-specialist` | QA Engineer | fix, bug, error |
| `creador-de-skills` | Senior Architect | new skill |

<!-- SKILLS_TABLE_START -->
| Skill | Description | Trigger (Auto-invoke) |
| :--- | :--- | :--- |
| [coding-standards](file:///home/jmbernales/qgispluginsdev/ai-context-core/.agent/skills/coding-standards/SKILL.md) | Estándares de codificación del proyecto, enfocados en el uso de pathlib, docstrings de Google y tipado estricto. | N/A |
| [commit-standards](file:///home/jmbernales/qgispluginsdev/ai-context-core/.agent/skills/commit-standards/SKILL.md) | Directrices para mensajes de commit de Git siguiendo la especificación de Conventional Commits. | N/A |
| [creador-de-skills-antigravity](file:///home/jmbernales/qgispluginsdev/ai-context-core/.agent/skills/creador-de-skills-antigravity/SKILL.md) | Especialista en diseñar habilidades (Skills) para Antigravity, garantizando una estructura técnica impecable, integración con el contexto del proyecto y alta mantenibilidad. | N/A |
| [debug-specialist](file:///home/jmbernales/qgispluginsdev/ai-context-core/.agent/skills/debug-specialist/SKILL.md) | Especialista en resolución sistemática de errores mediante el método científico, asegurando que cada fix sea reproducible y no genere regresiones. | N/A |
| [project-context](file:///home/jmbernales/qgispluginsdev/ai-context-core/.agent/skills/project-context/SKILL.md) | Resumen del propósito, arquitectura y estructura del proyecto ai-context-core. | N/A |
| [tech-stack](file:///home/jmbernales/qgispluginsdev/ai-context-core/.agent/skills/tech-stack/SKILL.md) | Guía de la pila tecnológica, gestión de dependencias con uv y herramientas de calidad. | N/A |
| [testing-standards](file:///home/jmbernales/qgispluginsdev/ai-context-core/.agent/skills/testing-standards/SKILL.md) | Directrices para asegurar la estabilidad del código mediante pruebas automatizadas con Pytest y Docker. | N/A |
<!-- SKILLS_TABLE_END -->
