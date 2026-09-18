---
name: coding-standards
description: Project coding standards (pathlib, Google docstrings, strict typing) for ai-context-core.
trigger: when writing Python code, refactoring, or defining file paths.
---

# Coding Standards

Establishes the technical rules for clean, readable, and modern Python code that integrates with the analyzer engine and the QGIS ecosystem.

## When to use this skill
- When writing new functions or classes.
- When refactoring existing code.
- When performing code quality audits.
- When integrating new libraries or dependencies.

## Degree of Freedom
- **Strict**: path handling (`pathlib`) and Google-style docstrings are mandatory.

## Workflow
1. **Path validation**: Ensure no `os.path` calls remain.
2. **Documentation**: Apply Google-style docstrings to every public node.
3. **Typing**: Verify that all arguments and returns have type hints.
4. **Compatibility**: Convert paths to `str` when passing to Qt/QGIS APIs.

## Instructions and Rules

### 1. Path Handling (pathlib)
- **Golden rule**: Always use `pathlib.Path`.
- **Do**: `Path(dir) / file`
- **Avoid**: `os.path.join(dir, file)`
- **Conversion**: Use `str(path_obj)` when interacting with APIs that do not accept Path objects.

### 2. Documentation (Google Style)
Docstrings must follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

```python
def example_function(param1: int) -> bool:
    """Summary of the function.

    Args:
        param1: Description of param1.

    Returns:
        True if successful, False otherwise.
    """
    return True
```

### 3. Strict Typing
- Use type hints on all arguments and return values.
- Prefer built-in types (Python 3.9+).

### 4. Import Order
- stdlib → third-party → local (absolute imports `from ai_context_core...`).

## Quality Checklist
- [ ] Is `pathlib` used exclusively for paths?
- [ ] Do all docstrings follow the Google format?
- [ ] Are there type hints for every input and output?
- [ ] Is the project context respected (@project-context)?
