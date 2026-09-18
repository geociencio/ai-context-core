---
name: agentic-memory
description: Manages semantic memory (lessons, patterns, user preferences) to improve long-term effectiveness.
trigger: at the end of each significant session, when detecting repetitive error patterns or user preferences.
---

# Skill: Agentic Memory (Brain)

Enables the agent to manage its own semantic memory by extracting lessons, patterns, and user preferences.

## Extraction Guidelines

Actively look for:
1. **Error patterns**: Solutions to bugs that took more than 3 attempts or deep investigation.
2. **Implicit preferences**: Style or architectural decisions the user repeatedly approves.
3. **Technical hotspots**: Areas of code that are difficult to test or refactor.
4. **Design decisions**: Justifications for why one implementation was chosen over another.

## Update Protocol (`AGENT_LESSONS.md`)

At the end of each significant session:
1. **Verify path**: Persist only in `.agent/` (never scaffold files).
2. **Target metrics**: Update `.agent/memory/agent_metrics.json`.
3. **Synthesize**: Summarize findings in entries of at most 3 lines.
4. **Categorize**: Use `[TECHNICAL]`, `[USER_PREFERENCE]`, `[ARCHITECTURE]`.
5. **Structure**: Maintain a YAML-friendly format for future RAG integrations.

## Structured Entry Example

```yaml
- date: 2026-09-17
  category: TECHNICAL
  topic: Metric keys
  lesson: "Metric consumers read canonical keys from metric_keys.py."
  action: "Always use metric_keys constants, never ad-hoc literals."
```

## Pre-flight Self-Audit

Before concluding any task:
1. **Lessons check**: "Have I applied relevant lessons from `AGENT_LESSONS.md`?"
2. **Context integrity**: "Does my solution follow the project's architectural standards?"
3. **Structured output**: "Does my final response provide a clear, structured summary?"
