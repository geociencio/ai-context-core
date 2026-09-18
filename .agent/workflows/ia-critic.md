---
description: Workflow for critical review of implementation plans by the Agent Auditor
agent: auditor
skills: [coding-standards, project-context, agentic-memory]
validation: |
  - Verify that the plan complies with architectural boundaries
  - Validate that no obvious technical debt is introduced
  - Confirm that lessons from AGENT_LESSONS.md were taken into account
---

# Workflow: AI Critic (Implementation Plan Audit)

Execute this workflow after creating an `implementation_plan.md` but before starting EXECUTION.

### Steps

1. **Critical Context Loading**:
   🤖 **Agent Action**: Load `AGENT_LESSONS.md` and look for lessons relevant to the current plan.

2. **Compliance Analysis**:
   🤖 **Agent Action**: Contrast the plan against project standards (pathlib, typing, Google docstrings, metric key contract).

3. **Risk Detection**:
   - Does it introduce tight coupling between modules?
   - Does it break backward compatibility?
   - Is the verification plan sufficient to catch regressions?

4. **Verdict Issuance**:
   🤖 **Agent Action**: Generate an audit report indicating:
   - **PASSED**: The plan is solid.
   - **FAILED**: The plan requires specific corrections.
   - **OBSERVATIONS**: Non-critical improvement suggestions.

---

*Philosophy: It is better to find an error in the blueprint than in the building.*
