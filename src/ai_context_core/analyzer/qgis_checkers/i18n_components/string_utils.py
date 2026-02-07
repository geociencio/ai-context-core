"""Utilities for identifying translatable strings."""

def is_translatable_string(text: str) -> bool:
    """Checks if a string is likely translatable (not a path, URL, or placeholder).

    Args:
        text: The string to check.

    Returns:
        True if the string is likely human-readable text.
    """
    val = text.strip()
    if not val or len(val) <= 1:
        return False
        
    is_path = val.startswith(("/", "./", "../")) or "\\" in val
    is_url = val.startswith(("http://", "https://", "ftp://"))
    is_placeholder = val.replace("{}", "").replace("%s", "").strip() == ""
    
    if is_path or is_url or is_placeholder:
        return False
        
    return " " in val or any(c in val for c in ".,!?;")
