"""Render context sections under a token budget and produce a token manifest."""

from typing import Any, Dict, List, Optional, Tuple

from .budget import TokenBudget, apply_budget, estimate_tokens

SectionLines = List[str]
Section = Tuple[str, SectionLines]


def render_sections(
    header: SectionLines,
    sections: List[Section],
    budget: TokenBudget,
) -> Tuple[List[str], Dict[str, Any]]:
    """Apply a budget to sections and return the final lines and manifest.

    Args:
        header: Document header lines (always kept, unless the cap is tiny).
        sections: Ordered ``(name, lines)`` sections.
        budget: Resolved token budget.

    Returns:
        ``(lines, manifest)`` where ``lines`` is the complete document body and
        ``manifest`` has exact per-section token deltas.
    """
    header_tokens = estimate_tokens("\n".join(header))
    counted, _pre, truncated = apply_budget(sections, budget, reserve=header_tokens)
    final: List[Section] = [(name, list(lines)) for name, lines, _ in counted]

    if budget.max_tokens is not None:
        final, truncated = enforce_hard_cap(final, budget.max_tokens, header, truncated)

    manifest = measure_manifest(header, final, truncated, budget.max_tokens)
    lines = header + [line for _name, section_lines in final for line in section_lines]
    return lines, manifest


def enforce_hard_cap(
    sections: List[Section],
    max_tokens: int,
    header: SectionLines,
    truncated: bool,
) -> Tuple[List[Section], bool]:
    """Trim trailing section lines until the rendered estimate fits the cap."""
    if estimate_tokens(_render(header, sections)) <= max_tokens:
        return sections, truncated

    marker = "... [truncated to fit token budget]"
    trimmed = [(name, list(lines)) for name, lines in sections]
    while trimmed:
        name, section_lines = trimmed[-1]
        if len(section_lines) > 1:
            trimmed[-1] = (name, section_lines[:-1])
        else:
            trimmed.pop()
        if estimate_tokens(_render(header, [*trimmed, ("truncated", [marker])])) <= max_tokens:
            break
    return [*trimmed, ("truncated", [marker])], True


def measure_manifest(
    header: SectionLines,
    sections: List[Section],
    truncated: bool,
    budget: Optional[int],
) -> Dict[str, Any]:
    """Measure exact per-section token deltas from the rendered sections.

    Deltas are cumulative so ``header_tokens + sum(sections) == total_tokens``.
    """
    running = list(header)
    cumulative = estimate_tokens("\n".join(running))
    section_tokens: Dict[str, int] = {}
    for name, section_lines in sections:
        running.extend(section_lines)
        new_cumulative = estimate_tokens("\n".join(running))
        section_tokens[name] = new_cumulative - cumulative
        cumulative = new_cumulative

    return {
        "total_tokens": estimate_tokens("\n".join(running)),
        "header_tokens": estimate_tokens("\n".join(header)),
        "budget": budget,
        "sections": section_tokens,
        "truncated": truncated,
    }


def _render(header: SectionLines, sections: List[Section]) -> str:
    """Render header + sections to text (used for measurements)."""
    return "\n".join(header + [line for _name, section_lines in sections for line in section_lines])
