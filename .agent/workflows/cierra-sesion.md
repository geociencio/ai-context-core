---
description: "Finaliza sesión: corre tests, actualiza logs, regenera contexto IA y propone commit de cierre."
agent: QA Engineer
skills:
  - project-context
  - commit-standards
validation:
  - ¿Todos los logs (DEVELOPMENT_LOG, CHANGELOG) están actualizados?
  - ¿Se ha rotado el archivo next_steps.md al historial?
  - ¿Los tests pasan antes de realizar el commit de cierre?
---

# Workflow: Finalizar Sesión

Este workflow asegura un cierre limpio, documentado y listo para que cualquier agente (o tú mismo) retome el trabajo.

## 1. Calidad y Formato

Asegura consistencia en el estilo del código.
```bash
uv run black .
```

## 2. Validación de Salida (Tests)

**Check Final (Docker):**
// turbo
```bash
make docker-test
```

## 3. Documentación y Memoria

Este paso es **CRÍTICO** para la persistencia del conocimiento.

1.  **`.agent/next_steps.md`**: Define qué falta, qué errores hay pendientes y cómo retomar.
2.  **Historial**: Copia `next_steps.md` a `.agent/history/next_steps/next_steps_YYYY-MM-DD.md`.
3.  **Logs**: Actualiza `docs/DEVELOPMENT_LOG.md` con un resumen técnico del día.
4.  **Changelog**: Registra cambios en la sección `[Unreleased]`.

## 4. Sincronización de Contexto

Actualiza las métricas y la memoria de largo plazo.

// turbo
```bash
uv run ai-ctx audit --threshold 50
uv run ai-ctx analyze
```

## 5. Commit de Cierre

Usa el skill `commit-standards` para generar el mensaje.
```bash
git add .
git commit -m "chore(docs): close session [tema_descriptivo]"
```

## Resultado Esperado
- Suite de pruebas: **7 tests OK**.
- Archivos de documentación actualizados y sincronizados.
- Historial de sesión preservado en `.agent/history/`.
- Commit de cierre realizado siguiendo estándares.
