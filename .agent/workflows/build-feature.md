---
description: Start the Autonomous AI Developer Pipeline sequence for a new feature.
agent: architect
skills: [domain-logic, qa-docker, coding-standards]
---

# Build Feature Autonomous Pipeline

When the user types `/build-feature <requirement>`, orchestrate the development process strictly using the root `AGENTS.md` and the modular `.agent/skills/`.

### Execution Sequence:

1. **Strategic Planning Mode**
   Act as the `@architect`. Deeply analyze the `<requirement>` using `domain-logic` and `coding-standards` to draft a robust implementation plan.
   - **Important**: Save this plan as `docs/plans/Technical_Specification.md`.
   - **Approval Gate**: Pause and eagerly ask the user: "Do you approve of this architecture?"
   *(Wait for explicit "Approved" before moving to step 2.)*

1.5. **Technical Critique (Architect vs. Auditor)**
   - Activate the `@auditor` role.
   - **Challenge the Plan**: Identify 3 potential failure points or edge cases.
   - **Mitigation**: The `@architect` must address these before presenting to the user.
   - **Hallucination Hunt**: Verify all proposed tool calls and file paths are valid.

2. **Autonomous Execution Phase**
   Act as the `@architect` (developer), strictly following the approved `Technical_Specification.md`. Write backend logic and CLI components according to project standards (typing, pathlib, ruff).

3. **Autonomous QA & Bug-Hunting Phase**
   Act as the `@qa_engineer`. Write isolated unit/integration tests, run the full suite, and fix edge cases until all tests pass.

4. **Integration & Handover**
   Act as the `@auditor`. Review that the code maintains the `AGENTS.md` metrics (complexity limits, docstring coverage). Confirm the feature is ready to commit.
