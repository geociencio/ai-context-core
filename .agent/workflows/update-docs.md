---
description: "Genera y actualiza la documentación del proyecto."
agent: Plugin Developer
skills:
  - project-context
  - tech-stack
---

# Workflow: Actualizar Documentación

Mantiene la documentación técnica y de usuario sincronizada con el estado real del código.

## 1. Actualización Automática

Regenera los archivos de contexto y resúmenes de arquitectura.

// turbo
```bash
uv run ai-ctx analyze
```

## 2. Auditoría de Documentos

1.  **`CHANGELOG.md`**: Verificar que todas las features nuevas estén en `[Unreleased]`.
2.  **`README.md`**: Actualizar ejemplos de uso si la API ha cambiado.
3.  **Logs de Sesión**: Asegurar que cada sesión importante tenga su resumen en `docs/sessions/`.

## 3. Consistencia
- Las rutas mencionadas en la documentación deben ser **absolutas** o relativas al root del proyecto.
- El lenguaje de la documentación técnica debe ser profesional y seguir los estándares de `project-context`.
