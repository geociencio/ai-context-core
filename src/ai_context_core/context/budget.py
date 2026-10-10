"""Token budget estimation and deterministic truncation for context artifacts.

The estimator is a heuristic (``chars / 4``) by default; ``tiktoken`` is an
optional accelerator selected via ``[context.budget].tokenizer = "tiktoken"``
when the package is installed.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

CHARS_PER_TOKEN = 4

SectionLines = List[str]
CountedSection = Tuple[str, SectionLines, int]


def estimate_tokens(text: str) -> int:
    """Estimate the token count of a string.

    Uses the ``chars / 4`` heuristic; deterministic and dependency-free.

    Args:
        text: Input text.

    Returns:
        Estimated token count (0 for empty input).
    """
    if not text:
        return 0
    return (len(text) + CHARS_PER_TOKEN - 1) // CHARS_PER_TOKEN


@dataclass
class TokenBudget:
    """Resolved token budget for a context render.

    Attributes:
        max_tokens: Global cap for the whole document, or ``None`` for unlimited.
        per_section: Optional per-section caps keyed by section name.
    """

    max_tokens: Optional[int] = None
    per_section: Dict[str, int] = field(default_factory=dict)

    @property
    def enabled(self) -> bool:
        """Whether any cap is configured."""
        return self.max_tokens is not None or bool(self.per_section)


def budget_from_config(
    config: Optional[Dict[str, Any]], max_tokens: Optional[int] = None
) -> TokenBudget:
    """Build a :class:`TokenBudget` from config, with a CLI override.

    Args:
        config: Analyzer configuration (``[context.budget]``).
        max_tokens: CLI override; wins over the configured value when given.

    Returns:
        The resolved budget.
    """
    context_cfg = _as_dict(config).get("context")
    budget_cfg = _as_dict(context_cfg).get("budget")

    configured_max = _as_dict(budget_cfg).get("max_tokens")
    resolved_max = max_tokens if max_tokens is not None else configured_max

    raw_sections = _as_dict(_as_dict(budget_cfg).get("sections"))
    per_section = {name: int(value) for name, value in raw_sections.items() if value}

    return TokenBudget(
        max_tokens=int(resolved_max) if resolved_max else None,
        per_section=per_section,
    )


def _as_dict(value: Any) -> Dict[str, Any]:
    """Return ``value`` if it is a dict, else an empty dict."""
    if isinstance(value, dict):
        return value
    return {}


def truncate_lines(lines: SectionLines, limit: Optional[int]) -> Tuple[SectionLines, int, bool]:
    """Truncate a section's lines to a token limit, deterministically.

    Whole lines are kept in order until the estimated limit is reached; a
    truncation marker counts toward the result. A single oversized first line is
    always kept.

    Args:
        lines: Section lines.
        limit: Maximum tokens, or ``None`` for no limit.

    Returns:
        ``(kept_lines, token_count, was_truncated)`` where ``token_count`` equals
        the estimate for the exact rendered section text.
    """
    if limit is None:
        return lines, estimate_tokens("\n".join(lines)), False

    kept: SectionLines = []
    for index, line in enumerate(lines):
        omitted = len(lines) - index
        marker = f"... [truncated: {omitted} lines omitted]"
        candidate = [*kept, line, marker]
        if kept and estimate_tokens("\n".join(candidate)) > limit:
            kept.append(marker)
            return kept, estimate_tokens("\n".join(kept)), True
        kept.append(line)

    return kept, estimate_tokens("\n".join(kept)), False


def apply_budget(
    sections: List[Tuple[str, SectionLines]],
    budget: TokenBudget,
    reserve: int = 0,
) -> Tuple[List[CountedSection], int, bool]:
    """Apply a token budget to an ordered list of sections.

    Sections are processed in order; the global cap subtracts already-consumed
    tokens (plus the reserved header). Once the cap is exhausted, remaining
    sections are dropped. Per-section caps truncate individual sections.

    Args:
        sections: Ordered ``(name, lines)`` pairs.
        budget: The resolved budget.
        reserve: Tokens reserved up-front (e.g. the document header).

    Returns:
        ``(counted_sections, total_tokens, truncated)``.
    """
    if not budget.enabled:
        counted = [(name, lines, estimate_tokens("\n".join(lines))) for name, lines in sections]
        return counted, sum(tokens for _, _, tokens in counted), False

    remaining: Optional[int] = None
    if budget.max_tokens is not None:
        remaining = max(0, budget.max_tokens - reserve)

    counted: List[CountedSection] = []
    truncated = False

    for name, lines in sections:
        if remaining is not None and remaining <= 0:
            truncated = True
            break

        limit = budget.per_section.get(name)
        if remaining is not None:
            limit = remaining if limit is None else min(limit, remaining)

        kept, tokens, did_truncate = truncate_lines(lines, limit)

        # A section whose truncated form still does not fit is dropped entirely.
        if remaining is not None and tokens > remaining:
            truncated = True
            break

        counted.append((name, kept, tokens))
        truncated = truncated or did_truncate

        if remaining is not None:
            remaining -= tokens
            if remaining <= 0:
                truncated = True
                break

    total = sum(tokens for _, _, tokens in counted)
    return counted, total, truncated
