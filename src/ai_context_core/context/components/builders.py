"""Prompt building strategies for different AI models."""


class PromptBuilder:
    """Strategy for building model-specific prompts."""

    def build(self, task: str, ctx: str, proj: str) -> str:
        """Builds a model-specific prompt.

        Args:
            task: The user task.
            ctx: Extracted context.
            proj: Project name.

        Returns:
            The formatted prompt.
        """
        raise NotImplementedError


class DeepSeekBuilder(PromptBuilder):
    """Builder for DeepSeek model."""

    def build(self, task: str, ctx: str, proj: str) -> str:
        return f"You are a Python expert analyzing {proj}\n\nCTX:\n{ctx}\n\nTASK:\n{task}\n\nFocus on efficiency."


class GPTBuilder(PromptBuilder):
    """Builder for GPT model."""

    def build(self, task: str, ctx: str, proj: str) -> str:
        return f"Act as Senior Dev for {proj}\n\nContext:\n{ctx}\n\nTask:\n{task}\n\nBe concise."


class ClaudeBuilder(PromptBuilder):
    """Builder for Claude model."""

    def build(self, task: str, ctx: str, proj: str) -> str:
        return f"System: Expert Architect for {proj}\n\nContext:\n{ctx}\n\nTask:\n{task}\n\nDetailed analysis."
