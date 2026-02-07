---
description: "Audita la consistencia del sistema agentico (Skills y Workflows) contra el estándar maestro."
agent: Senior Architect
skills:
  - creador-de-skills-antigravity
  - project-context
validation:
  - ¿Todos los Skills tienen Checklist de Calidad?
  - ¿La documentación de los Skills está 100% en español?
  - ¿Los Workflows tienen secciones de Resultado Esperado?
---

# Workflow: Verificar Estándares Agenticos

Este flujo garantiza que el propio "cerebro" de la IA se mantenga ordenado, legible y bajo los estándares de calidad definidos en `docs/AGENTIC_STANDARDS_AND_SOURCES.md`.

## 1. Auditoría de Habilidades (Skills)

Revisar cada archivo en `.agent/skills/` buscando:
1.  **YAML**: Presencia de `name` y `description`.
2.  **Idioma**: Descripción y contenido principal en español.
3.  **Secciones**: Cuándo usar, Grado de Libertad, Workflow, Instrucciones, Output y Checklist.

## 2. Auditoría de Flujos (Workflows)

Revisar cada archivo en `.agent/workflows/` buscando:
1.  **YAML**: Descripción clara del objetivo.
2.  **Estructura**: Pasos numerados y uso de `// turbo` donde aplique.
3.  **Cierre**: Sección de "Resultado Esperado" al final.

## 3. Verificación de Memoria y Recursos

- Validar que `.agent/memory/AGENT_LESSONS.md` esté actualizado con las últimas lecciones del mes.
- Asegurar que `.agent/resources/` contenga guías técnicas actualizadas para los problemas detectados en la última semana.

## Resultado Esperado
- Informe detallado de desviaciones de estándar.
- Propuesta de corrección inmediata para skills u workflows obsoletos.
- Confirmación de que el sistema operará con máxima eficiencia.
