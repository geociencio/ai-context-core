---
name: coding-standards
description: Project-specific coding guidelines (pathlib, Google Docstrings)
trigger: python, style, refactor, path
---

# Coding Standards

## Path Handling
**Strict Rule**: Use `pathlib` for file path manipulation (Modern Python).
- **Do**: `Path(dir) / file`
- **Avoid**: `os.path.join(dir, file)`

### QGIS/Qt Compatibility
When interacting with QGIS or Qt APIs that require strings:
- **Do**: `str(my_path_object)` or `my_path_object.as_posix()` explicitly.

## Documentation Style
**Docstrings**: Must follow [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

### Example
```python
def function_name(param1, param2):
    """Summary line.

    Extended description of function.

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.
    """
    return True
```

## Type Hinting
- Use explicit type hints for all function arguments and return values.
- Use `typing` module or built-ins (Python 3.9+).
