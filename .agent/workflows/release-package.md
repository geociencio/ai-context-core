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

2.  **Versionado (Bump Version)**:
    Actualiza la versión en `pyproject.toml`.
    *Reemplaza `NEW_VERSION` con la versión real (ej: 1.2.0).*
    ```bash
    # Ejemplo manual o con sed si se confirma la versión
    # sed -i 's/^version = "OLD"/version = "NEW"/' pyproject.toml
    ```

3.  **Actualización de Changelog**:
    *   Mueve `[Unreleased]` a `[VERSION] - FECHA`.
    *   Genera Release Notes en `docs/releases/notes/vVERSION.md`.

4.  **Git Operations**:
    Etiqueta la versión en el control de versiones.
    ```bash
    git add pyproject.toml CHANGELOG.md README.md
    git commit -m "chore(release): prepare vVERSION"
    git tag -a "vVERSION" -m "Release vVERSION"
    git push origin main
    git push origin "vVERSION"
    ```

5.  **Build & Distribution**:
    Genera los artefactos distribuibles.
    // turbo
    ```bash
    uv build
    ls -la dist/
    ```

6.  **GitHub Release**:
    Crea el draft release.
    ```bash
    gh release create "vVERSION" --title "vVERSION" --notes-file docs/releases/notes/vVERSION.md --draft
    gh release upload "vVERSION" dist/* --clobber
    ```
