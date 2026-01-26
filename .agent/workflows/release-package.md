---
description: "Automatiza el proceso de release: validación de calidad, versionado, git tagging y build."
agent: QA Engineer
skills:
  - project-context
  - tech-stack
  - commit-standards
---

# Workflow: Release Package

Este workflow estandariza el proceso de liberación de una nueva versión de `ai-context-core`.

## Fases del Release

1.  **Validación de Calidad**:
    Antes de versionar, aseguramos que el código cumpla los estándares.
    // turbo
    ```bash
    uv run ai-ctx analyze
    uv run ruff check .
    uv run python -m unittest discover tests
    ```
    > **Check**: El score debe ser alto (>90%) y los tests deben pasar (100%).

2.  **Versionado y Nombramiento (Bump Version)**:
    Actualiza la versión en `pyproject.toml` y define un título para el lanzamiento.
    *Reemplaza `NEW_VERSION` con la versión real (ej: 2.5.0) y `VERSION_TITLE` (ej: Performance and GIS Edition).*
    ```bash
    # sed -i 's/^version = "OLD"/version = "NEW_VERSION"/' pyproject.toml
    ```

3.  **Actualización de Documentos**:
    *   **README.md**: Actualizar insignias de versión y secciones clave si hay nuevos features.
    *   **Changelog**: 
        - Mover `[Unreleased]` a `[NEW_VERSION] - FECHA - VERSION_TITLE`.
        - Asegurar que cada sección (Added, Fixed, Optimized) tenga títulos descriptivos.
    *   **Release Notes**: Generar `docs/releases/notes/vNEW_VERSION.md` con el título del release en el encabezado #1.

4.  **Git Operations**:
    Etiqueta la versión en el control de versiones.
    ```bash
    git add pyproject.toml CHANGELOG.md README.md docs/
    git commit -m "chore(release): prepare vNEW_VERSION - VERSION_TITLE"
    git tag -a "vNEW_VERSION" -m "vNEW_VERSION - VERSION_TITLE"
    git push origin main
    git push origin "vNEW_VERSION"
    ```

5.  **Build & Distribution**:
    Genera los artefactos distribuibles.
    // turbo
    ```bash
    uv build
    ls -la dist/
    ```

6.  **GitHub Release**:
    Crea el draft release con el título oficial.
    ```bash
    gh release create "vNEW_VERSION" --title "vNEW_VERSION - VERSION_TITLE" --notes-file docs/releases/notes/vNEW_VERSION.md --draft
    gh release upload "vNEW_VERSION" dist/* --clobber
    ```
