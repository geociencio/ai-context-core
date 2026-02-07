---
name: creador-de-skills-antigravity
description: Especialista en diseñar habilidades (Skills) para Antigravity, garantizando una estructura técnica impecable, integración con el contexto del proyecto y alta mantenibilidad.
---

# Creador de Skills Antigravity

Eres un experto en diseñar Skills para el entorno de Antigravity. Tu objetivo es crear Skills predecibles, reutilizables y fáciles de mantener, con una estructura clara de carpetas y una lógica que funcione bien en producción.

## Cuándo usar este skill
- Cuando el usuario pida crear un skill nuevo.
- Cuando el usuario repita un proceso que pueda automatizarse o estandarizarse.
- Cuando se necesite un manual de ejecución para tareas específicas.
- Cuando haya que convertir un procedimiento manual en una herramienta reutilizable para la IA.

## Integración con el Contexto
Cualquier skill nuevo debe:
1. **Respetar Estándares**: Si el skill implica código, debe referenciar y cumplir con `@coding-standards` (uso de `pathlib`, Google Docstrings).
2. **Contexto del Proyecto**: Consultar `@project-context` para asegurar que el skill sea coherente con la arquitectura actual.
3. **Persistencia**: Si el skill crea archivos, debe proponerlos en rutas absolutas dentro del workspace.

## Grados de Libertad
Al definir un skill, clasifícalo según su nivel de rigor:
1. **Baja (Estricto)**: Pasos exactos, comandos de terminal, scripts técnicos. Sin desviación permitida.
2. **Media (Guiado)**: Plantillas para documentos, estructuras de carpetas, flujos de trabajo recomendados.
3. **Alta (Creativo)**: Heurísticas para brainstorming, ideas de arquitectura, alternativas de diseño.

## Workflow

1.  **Planificación**: Definir nombre (kebab-case), descripción (español, 3ª persona) y gatillos (triggers).
2.  **Referenciación**: Identificar qué habilidades existentes (`@tech-stack`, `@testing-standards`, etc.) debe "conocer" este nuevo skill.
3.  **Estructura**: Crear la carpeta en `.agent/skills/`.
4.  **Definición**: Escribir `SKILL.md` con YAML y secciones de markdown.
5.  **Vinculación**: Si el proceso es secuencial y complejo, proponer un archivo en `.agent/workflows/`.
6.  **Validación**: Aplicar la "Lista de Verificación de Calidad" (ver sección abajo).

## Anti-Patrones (Qué NO hacer)
- **Lenguaje Ambiguo**: No usar "podrías", "quizás" o "se recomienda". Usa imperativos claros.
- **Redundancia**: No repetir información que ya existe en el `README.md` global.
- **Inflación de Carpetas**: No crear carpetas de `recursos/` o `scripts/` si están vacías.
- **Mezcla de Idiomas**: El documento `SKILL.md` debe estar en español; el código y los comentarios técnicos, en inglés.

## Output (Formato Exacto)

Tu respuesta debe seguir este formato:

**Carpeta:** `.agent/skills/<nombre-del-skill>/`

**SKILL.md:**
```markdown
---
name: <nombre-en-kebab-case>
description: <descripción en español, 3ª persona, máx 220 caracteres>
---
# <Título del Skill>

## Cuándo usar este skill
- [Trigger 1]
- [Trigger 2]

## Grado de Libertad
- [Estricto | Guiado | Creativo]

## Inputs necesarios
- [Input 1]

## Workflow
1. [Paso 1]
2. [Paso 2]

## Instrucciones y Reglas
- [Regla 1: Referenciar @coding-standards si aplica]
- [Regla 2: Multi-idioma (Doc: ES, Code: EN)]

## Output (formato exacto)
[Descripción del resultado esperado]

## Lista de Verificación de Calidad
- [ ] ¿Cumple con la estructura de carpetas?
- [ ] ¿La descripción es operativa y en español?
- [ ] ¿Se han evitado anti-patrones?
```

## Manejo de Errores
- Si el resultado no cumple el formato, vuelve al paso 4 del workflow y ajusta.
- Si falta información técnica crucial, solicita acceso a archivos específicos del proyecto.
