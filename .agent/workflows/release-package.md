---
description: "Automatiza el proceso de release: validación de calidad, versionado, git tagging y build."
agent: QA Engineer
skills:
  - project-context
  - tech-stack
  - commit-standards
---

# Workflow: Liberar Versión (Release)

Este workflow asegura que cada versión pública de `ai-context-core` sea estable, esté documentada y sea trazable.

## 1. Auditoría de Calidad (Puerta de Enlace)

Antes de cualquier cambio de versión, el sistema debe ser auditado.

// turbo
```bash
uv run ai-ctx audit --threshold 90
uv run ruff check .
make docker-test
```

> **STOP**: No procedas si el score es <90 o si hay fallos en los tests.

## 2. Preparación del Release

1.  **Versionado**: Actualiza `version` en `pyproject.toml`. Asegúrate de actualizar también el `__version__` de fallback en `src/ai_context_core/__init__.py` (aunque la CLI lo extrae dinámicamente, el fallback es vital para desarrollo local).
2.  **Changelog**: Mueve `[Unreleased]` a la nueva versión con la fecha actual.
3.  **Release Notes**: Crea `docs/releases/notes/v[VERSION].md`.

## 3. Operaciones de Git

Estandariza los mensajes y etiquetas.

```bash
git add pyproject.toml CHANGELOG.md README.md docs/
git commit -m "chore(release): prepare v[VERSION] - [Título]"
git tag -a "v[VERSION]" -m "v[VERSION] - [Título]"
git push origin main --tags
```

## 4. Construcción y Publicación

Genera los artefactos y prepara la release en GitHub.

// turbo
```bash
uv build
gh release create "v[VERSION]" --title "v[VERSION] - [Título]" --notes-file docs/releases/notes/v[VERSION].md --draft
gh release upload "v[VERSION]" dist/*
```

## Resultado Esperado
- Versión actualizada en `pyproject.toml`.
- Etiqueta de Git creada y subida al remoto.
- Draft release en GitHub con artefactos `.whl` y `.tar.gz`.
