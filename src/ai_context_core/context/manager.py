import json
import yaml
from pathlib import Path
from typing import Dict, Any, List


class AIContextManager:
    """Manages optimized context for different AIs."""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.contexts = self._load_contexts()

    def _load_contexts(self) -> Dict[str, Any]:
        """Loads existing contexts."""
        contexts = {}
        context_files = ["project_context.json", "AI_CONTEXT.md", ".ai-context.yaml"]

        for file in context_files:
            path = self.project_path / file
            if path.exists():
                contexts[file] = self._load_file(path)

        return contexts

    def _load_file(self, path: Path) -> Any:
        """Loads file content based on its extension."""
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
        """Creates optimized prompt for the specific task."""
        # Project base context
        base_context = self._extract_relevant_context(task)

        # Optimize based on AI model
        if "deepseek" in ai_model.lower():
            prompt_template = self._deepseek_template()
        elif "gpt" in ai_model.lower():
            prompt_template = self._chatgpt_template()
        elif "claude" in ai_model.lower():
            prompt_template = self._claude_template()
        else:
            prompt_template = self._generic_template()

        # Assemble final prompt
        full_prompt = prompt_template.format(
            task=task,
            context=base_context[: max_tokens // 2],
            project_name=self.project_path.name,
        )

        return self._truncate_to_tokens(full_prompt, max_tokens)

    def _deepseek_template(self) -> str:
        """Optimized template for DeepSeek."""
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
        """Optimized template for ChatGPT."""
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
        """Optimized template for Claude."""
        return """System: You are an expert software architect analyzing {project_name}.

Context:
{context}

Task:
{task}

Please provide a detailed analysis, considering architectural implications and best practices.
"""

    def _generic_template(self) -> str:
        """Generic template."""
        return """Project: {project_name}

Context:
{context}

Task:
{task}
"""

    def _extract_relevant_context(self, task: str) -> str:
        """Extracts relevant context for the specific task."""
        keywords = self._extract_keywords(task)
        relevant_parts = []

        # Search in existing contexts
        for context_name, context_content in self.contexts.items():
            if isinstance(context_content, dict):
                content_str = json.dumps(context_content)
            else:
                content_str = str(context_content)

            # Check relevance
            if any(keyword.lower() in content_str.lower() for keyword in keywords):
                relevant_parts.append(f"=== {context_name} ===\n{content_str[:1000]}")

        return "\n\n".join(relevant_parts) if relevant_parts else "No specific context found"

    def _extract_keywords(self, text: str) -> List[str]:
        """Extracts keywords from text."""
        # Common stop words to ignore
        stop_words = {
            "the",
            "and",
            "for",
            "with",
            "from",
            "that",
            "this",
            "what",
            "how",
            "when",
            "where",
            "which",
            "who",
            "whom",
        }
        words = text.lower().split()
        return [w for w in words if w not in stop_words and len(w) > 3]

    def _truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncates text approximating tokens."""
        # Simple estimation: 1 token ≈ 4 characters
        max_chars = max_tokens * 4
        if len(text) <= max_chars:
            return text

        # Truncate at logical point
        truncated = text[:max_chars]
        last_period = truncated.rfind(".")
        last_newline = truncated.rfind("\n")

        cutoff = max(last_period, last_newline)
        if cutoff > max_chars * 0.8:
            return truncated[: cutoff + 1] + "\n\n[Context truncated due to limits...]"

        return truncated + "\n\n[Context truncated due to limits...]"

    def update_context(self, new_info: Dict[str, Any]) -> None:
        """Updates context with new information."""
        update_file = self.project_path / ".ai-context-updates.yaml"

        current = {}
        if update_file.exists():
            try:
                current = yaml.safe_load(update_file.read_text(encoding="utf-8")) or {}
            except Exception:
                current = {}

        # Merge new information
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

        # Save
        with open(update_file, "w", encoding="utf-8") as f:
            yaml.dump(current, f, allow_unicode=True)

        print(f"✅ Context updated in {update_file}")
