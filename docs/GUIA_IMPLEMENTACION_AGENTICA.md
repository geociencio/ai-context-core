# Guía de Implementación de Sistemas Agenticos (Antigravity)

Esta guía explica cómo portar la infraestructura de inteligencia (Skills, Workflows y Roles) de este proyecto a cualquier otro repositorio de Python o Plugin de QGIS para maximizar la productividad con IA.

## 1. Requisitos Previos

- **Antigravity CLI**: Instalado y configurado en tu entorno.
- **Acceso a Gemini (o LLM compatible)**: Con permisos de lectura/escritura en el workspace.
- **Estructura Base**: El proyecto debe tener un archivo `pyproject.toml` (preferiblemente gestionado con `uv`).

## 2. Inicialización de la Carpeta `.agent`

El "cerebro" del agente vive en la carpeta `.agent/`. Créala en la raíz de tu nuevo proyecto:

```bash
mkdir -p .agent/{skills,workflows,memory,resources}
```

### Archivo Maestro: `AGENTS.md`
Crea el archivo `.agent/AGENTS.md` definiendo los roles. Puedes copiar la estructura de este proyecto:

```markdown
# AI Agents & Roles
## Perfiles Principales
### 🧠 Senior Architect
**Foco**: Diseño de Sistema y Lógica Core.
...
```

## 3. Implementación de Habilidades (Skills)

Copia las habilidades esenciales desde este proyecto a tu nueva carpeta `.agent/skills/`. Los "imprescindibles" son:

1.  **coding-standards**: Define cómo quieres que la IA escriba el código (ej. usar `pathlib`).
2.  **commit-standards**: Asegura que el historial de Git sea legible.
3.  **project-context**: Ayuda a la IA a no "alucinar" sobre la arquitectura.
4.  **creador-de-skills-antigravity**: La herramienta para que la propia IA expanda sus capacidades.

*Importante: Ajusta las reglas de `coding-standards` si tu nuevo proyecto usa estándares diferentes (ej. Django vs Flask).*

## 4. Configuración de Flujos de Trabajo (Workflows)

Los workflows permiten automatizar procesos multietapa. Los mínimos recomendados en `.agent/workflows/` son:

- **inicia-sesion.md**: Sincroniza el contexto y verifica el entorno.
- **cierra-sesion.md**: Documenta el progreso y garantiza persistencia.
- **run-tests.md**: Automatiza la verificación de calidad.

## 5. Diferencias por Tipo de Proyecto

### Proyecto Python Estándar
- Foco en **Tech Stack**: Asegura que el skill `tech-stack` refleje tu gestor de paquetes (uv, poetry, pip).
- Foco en **Tests**: Configura `run-tests.md` para tu framework (pytest, nose, unittest).

### Plugin de QGIS
- **Recursos**: Es vital incluir una guía de **Mocking de QGIS** en `.agent/resources/` para que la IA pueda testear sin el binario de QGIS.
- **Validación**: Añade un workflow de liberación (`release-package.md`) que verifique el archivo `metadata.txt` y empaquete el ZIP correctamente.
- **Roles**: Activa el rol de **GIS-Architect** para manejar específicamente lógica espacial y PyQt.

## 6. Mejores Prácticas para el Éxito

1.  **Persistent Memory**: Mantén siempre un archivo `.agent/memory/AGENT_LESSONS.md` actualizado. Es donde la IA guarda tus caprichos y preferencias de diseño "fuera de manual".
2.  **Auditabilidad**: Usa el workflow `verificar-estandares.md` una vez a la semana para asegurar que el sistema no se degrade.
3.  **Idioma**: Mantén la documentación del agente en un solo idioma (preferiblemente Español) para evitar confusión en los tokens.

---
*Manual generado para: Ecosistema Antigravity*
*Versión: 1.1*
