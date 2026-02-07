---
name: commit-standards
description: Directrices para mensajes de commit de Git siguiendo la especificación de Conventional Commits.
---

# Commit Standards

Garantiza un historial de Git limpio, legible y automatizable mediante el uso de Conventional Commits.

## Cuándo usar este skill
- Antes de realizar un commit.
- Al revisar Pull Requests.
- Al preparar una nueva versión (release).

## Grado de Libertad
- **Estricto**: El formato `<type>(<scope>): <subject>` no es negociable.

## Inputs necesarios
- Cambios realizados en el código.
- Áreas afectadas (scope).

## Workflow
1. **Identificación**: Determinar el tipo de cambio (`feat`, `fix`, `docs`, etc.).
2. **Contextualización**: Definir el `scope` basado en los módulos afectados.
3. **Redacción**: Escribir el mensaje en inglés, en presente e imperativo.
4. **Validación**: Ejecutar el workflow `/crea-el-comit` si está disponible.

## Instrucciones y Reglas

### 1. Formato Conventional Commits
- Estructura: `<type>(<scope>): <subject>`
- **Tipos**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`.
- **Scopes**: `core`, `cli`, `deps`, `docs`, `ci`, `analyzer`, `config`.

### 2. Reglas de Redacción
- **Idioma**: El mensaje de commit siempre en **Inglés**.
- **Estilo**: Empezar con minúscula el subject (opcional, pero consistente), no terminar con punto.

## Output (formato exacto)
Un mensaje de commit que cumpla estrictamente con la especificación.

## Lista de Verificación de Calidad
- [ ] ¿El mensaje sigue el formato `tipo(scope): descripción`?
- [ ] ¿El tipo es uno de los permitidos?
- [ ] ¿El scope es válido según el proyecto?
- [ ] ¿El mensaje está en inglés?
- [ ] ¿Se vinculó con un issue si es necesario?
