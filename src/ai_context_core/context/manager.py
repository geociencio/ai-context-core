"""Project context and AI prompt management."""

import pathlib
from typing import Dict, Any


from .components import (
    ContextStore,
    ContextExtractor,
    GPTBuilder,
    DeepSeekBuilder,
    ClaudeBuilder,
)


class AIContextManager:
    """Manages project context and optimizes prompts.

    Delegates storage, extraction and builder selection to specialized components.
    """

    def __init__(self, project_path: str):
        """Initializes the context manager.

        Args:
            project_path: Path to the project root.
        """
        self.project_path = pathlib.Path(project_path)
        self.store = ContextStore(self.project_path)
        self.contexts = self.store.load_all()

    def create_optimized_prompt(
        self, task: str, model: str = "gpt", max_tokens: int = 4000
    ) -> str:
        """Creates an AI-optimized prompt with relevant context.

        Args:
            task: The user task.
            model: The target AI model name.
            max_tokens: Maximum context tokens allowed.

        Returns:
            The generated prompt string.
        """
        builders = {
            "deepseek": DeepSeekBuilder(),
            "gpt": GPTBuilder(),
            "claude": ClaudeBuilder(),
        }
        builder = next(
            (b for k, b in builders.items() if k in model.lower()), GPTBuilder()
        )

        ctx_str = ContextExtractor.extract_relevant(task, self.contexts)
        return builder.build(task, ctx_str[: max_tokens * 2], self.project_path.name)

    def update_context(self, info: Dict[str, Any]):
        """Updates the project context with new information.

        Args:
            info: Dictionary containing context updates.
        """
        self.store.update(info)
