"""Extracts relevant pieces of context based on task keywords."""

import json
from typing import Dict, Any

class ContextExtractor:
    """Logic for extracting relevant context from stored data."""

    @staticmethod
    def extract_relevant(task: str, contexts: Dict[str, Any]) -> str:
        """Extracts context matching keywords in the task.

        Args:
            task: The user task description.
            contexts: Dictionary of available context data.

        Returns:
            Formatted string of relevant context.
        """
        kws = [w.lower() for w in task.split() if len(w) > 3]
        found = []
        for name, content in contexts.items():
            s = (
                json.dumps(content)
                if isinstance(content, (dict, list))
                else str(content)
            )
            if any(k in s.lower() for k in kws):
                found.append(f"=== {name} ===\n{s[:1000]}")
        
        return "\n\n".join(found) if found else "No relevant context."
