"""Project context and AI prompt management.

The AIContextManager identifies relevant context for specific tasks and
formats optimized prompts for various AI models (DeepSeek, GPT, Claude).
"""
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List


class AIContextManager:
    """Manages project context and optimizes prompts for different AI models.

    This manager loads existing context files (JSON, Markdown, YAML) and
    extracts relevant information based on specific tasks to create structured
    prompts for LLMs.

    Attributes:
        project_path: Path to the project root.
        contexts: Dictionary of loaded context contents.
    """

    def __init__(self, project_path: str):
        """Initializes the AIContextManager.

        Args:
            project_path: Directory path of the project.
        """
        self.project_path = Path(project_path)
        self.contexts = self._load_contexts()

    def _load_contexts(self) -> Dict[str, Any]:
        """Loads available project context files into memory.

        Returns:
            A dictionary mapping filenames to their parsed or raw content.
        """
        contexts = {}
        context_files = ["project_context.json", "AI_CONTEXT.md", ".ai-context.yaml"]

        for file in context_files:
            path = self.project_path / file
            if path.exists():
                contexts[file] = self._load_file(path)

        return contexts

    def _load_file(self, path: Path) -> Any:
        """Parses a file based on its extension or returns raw text.

        Args:
            path: Path to the file to load.

        Returns:
            Parsed JSON/YAML data or a raw string for Markdown/other files.
        """
        try:
            if path.suffix == ".json":
                return json.loads(path.read_text(encoding="utf-8"))
            elif path.suffix in [".yaml", ".yml"]:
                return yaml.safe_load(path.read_text(encoding="utf-8"))
            else:
                return path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"⚠️ Error loading {path}: {e}")
            return ""

    def create_optimized_prompt(
        self, task: str, ai_model: str = "deepseek-coder", max_tokens: int = 4000
    ) -> str:
        """Constructs an AI-ready prompt optimized for the specified model and task.

        Args:
            task: The engineering task to perform.
            ai_model: Identifier for the AI model (e.g., 'gpt-4', 'claude-3').
            max_tokens: Maximum allowed token limit for the total prompt.

        Returns:
            A fully structured and optimized prompt string.
        """
        # Extract keywords and find relevant context snippets
        base_context = self._extract_relevant_context(task)

        # Select template based on model characteristics
        if "deepseek" in ai_model.lower():
            prompt_template = self._deepseek_template()
        elif "gpt" in ai_model.lower():
            prompt_template = self._chatgpt_template()
        elif "claude" in ai_model.lower():
            prompt_template = self._claude_template()
        else:
            prompt_template = self._generic_template()

        # Build final instruction
        full_prompt = prompt_template.format(
            task=task,
            context=base_context[: max_tokens // 2],
            project_name=self.project_path.name,
        )

        return self._truncate_to_tokens(full_prompt, max_tokens)

    def _deepseek_template(self) -> str:
        """Returns a template optimized for DeepSeek Coder models.

        Returns:
            Markdown-formatted instruction string.
        """
        return """You are a Python expert analyzing the project: {project_name}

## PROJECT CONTEXT:
{context}

## ASSIGNED TASK:
{task}

## SPECIFIC INSTRUCTIONS FOR DEEPSEEK:
1. Focus on practical and efficient code
2. Suggest performance optimizations
3. Maintain compatibility with Python 3.8+
4. Include specific code examples
5. Prioritize solutions with standard libraries

## RESPONSE FORMAT:
```analysis
[Brief analysis of the problem]
suggestions
[Numbered list of suggestions]
code_examples
[Example code if applicable]
next_steps
[Recommended next steps]
```"""

    def _chatgpt_template(self) -> str:
        """Returns a concise template optimized for OpenAI GPT models.

        Returns:
            Markdown-formatted instruction string.
        """
        return """Act as a Senior Python Developer expert in project {project_name}.

RELEVANT CONTEXT:
{context}

YOUR TASK:
{task}

GUIDELINES:
- Be concise and direct.
- If you suggest changes, explain 'why'.
- Use markdown format for code.
"""

    def _claude_template(self) -> str:
        """Returns an architectural template optimized for Anthropic Claude models.

        Returns:
            Markdown-formatted instruction string.
        """
        return """System: You are an expert software architect analyzing {project_name}.

Context:
{context}

Task:
{task}

Please provide a detailed analysis, considering architectural implications and best practices.
"""

    def _generic_template(self) -> str:
        """Returns a basic boilerplate template for other models.

        Returns:
            Simplified instruction string.
        """
        return """Project: {project_name}

Context:
{context}

Task:
{task}
"""

    def _extract_relevant_context(self, task: str) -> str:
        """Identifies and extracts matching snippets from loaded contexts using keywords.

        Args:
            task: The task description to match against.

        Returns:
            A string containing identified relevant context chunks.
        """
        keywords = self._extract_keywords(task)
        relevant_parts = []

        if not keywords:
            return "No specific context identifiers identified in the task."

        # Search through all loaded contexts (JSON meta, MD reports, YAML profiles)
        for context_name, context_content in self.contexts.items():
            content_str = self._get_serializable_content(context_content)
            
            # Simple keyword matching for relevance
            if any(keyword.lower() in content_str.lower() for keyword in keywords):
                # Include a relevant snippet
                relevant_parts.append(f"=== {context_name} ===\n{content_str[:1000]}")

        return "\n\n".join(relevant_parts) if relevant_parts else "No specific project context matches found for this task."

    def _get_serializable_content(self, context_content: Any) -> str:
        """Recursively converts complex objects to strings for text analysis.

        Args:
            context_content: Dict, List, or raw string data.

        Returns:
            A string representation of the data.
        """
        if isinstance(context_content, (dict, list)):
            return json.dumps(context_content, ensure_ascii=False)
        return str(context_content)

    def _extract_keywords(self, text: str) -> List[str]:
        """Tokenizes text and filters out common stop words to find searchable terms.

        Args:
            text: Input string to process.

        Returns:
            A list of lowercase keywords longer than 3 characters.
        """
        # Common English stop words
        stop_words = {
            "the", "and", "for", "with", "from", "that", "this",
            "what", "how", "when", "where", "which", "who", "whom",
        }
        words = text.lower().split()
        return [w for w in words if w not in stop_words and len(w) > 3]

    def _truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Estimates and truncates text to fit within token limits.

        Approximate conversion: 1 token ≈ 4 characters.

        Args:
            text: Raw string to truncate.
            max_tokens: The target token limit.

        Returns:
            The truncated string with a trailing notification if cut.
        """
        max_chars = max_tokens * 4
        if len(text) <= max_chars:
            return text

        # Attempt to find a logical breaking point (period or newline)
        truncated = text[:max_chars]
        last_period = truncated.rfind(".")
        last_newline = truncated.rfind("\n")

        cutoff = max(last_period, last_newline)
        if cutoff > max_chars * 0.8:
            return truncated[: cutoff + 1] + "\n\n[Context truncated due to limits...]"

        return truncated + "\n\n[Context truncated due to limits...]"

    def update_context(self, new_info: Dict[str, Any]) -> None:
        """Persists new runtime discoveries into a YAML update file.

        Args:
            new_info: Dictionary of key-value pairs to add or update in context.
        """
        update_file = self.project_path / ".ai-context-updates.yaml"

        current = {}
        if update_file.exists():
            try:
                current = yaml.safe_load(update_file.read_text(encoding="utf-8")) or {}
            except Exception:
                current = {}

        # Merge updates into existing structure
        for key, value in new_info.items():
            if key in current:
                if isinstance(current[key], list) and isinstance(value, list):
                    current[key].extend(value)
                elif isinstance(current[key], dict) and isinstance(value, dict):
                    current[key].update(value)
                else:
                    current[key] = value
            else:
                current[key] = value

        # Save back to file
        with open(update_file, "w", encoding="utf-8") as f:
            yaml.dump(current, f, allow_unicode=True)

        print(f"✅ Context updated in {update_file}")
