---
name: domain-logic
description: Business logic, data validation, and core processing for the analyzer engine.
trigger: when implementing new analysis rules, data validation, or core processing logic.
---

# Domain Logic (Analyzer)

Defines the rules for analysis processing, ensuring consistency and integrity through modular, decoupled components.

## When to use this skill
- When adding a new AST visitor or analysis rule.
- When modifying metric calculation in `builders/calculator.py`.
- When implementing config validation or data processing.

## Degree of Freedom
- **Strict**: The engine → providers → visitors/builders → reporting separation is mandatory.

## Workflow
1. **Model**: Define the concern with strict types and one visitor per concern.
2. **Detect**: Implement pure detection (no side effects, no I/O) in the visitor.
3. **Aggregate**: Compute derived metrics in `builders/`, not inline in visitors.
4. **Test**: Add a regression test for every new rule.

## Instructions and Rules

### Separation of Concerns
- **Pure visitors**: Visitors detect and record only; the engine reports.
- **Metric contract**: Register metrics using canonical keys from `builders/metric_keys.py`.
- **No I/O**: Never write files or read from disk inside an AST visitor.

### Decoupling
- **CLI stays thin**: No analysis logic in `cli/`.
- **Providers**: File scanning/caching lives in `providers/`, not visitors.

## Quality Checklist
- [ ] Is the visitor side-effect free?
- [ ] Are metrics registered via `metric_keys.py`?
- [ ] Is CLI/engine/visitor separation respected?
- [ ] Is there a test for the new rule?
