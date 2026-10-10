# Comparison with Other Tools (internal)

> **Internal document.** This is a working comparison kept out of the public
> `README.md`. It reflects positioning notes for the context-only contract
> (v5.0.0, see [ADR-0008](adr/0008-context-only-contract.md)) and may lag the
> public surface; treat the README/CHANGELOG as the source of truth.

`ai-context-core` is a **context compiler**, not a code packager or an analyzer:
it maximizes context fidelity for LLMs by extracting **semantic structure** and
producing versioned, provenance-tagged artifacts.

## How It Differs

| Aspect | `ai-context-core` |
| :--- | :--- |
| **Primary Goal** | **Compile context** (`source → transform → render → verify`), not analyze. |
| **Sources** | `qgis-plugin-analyzer` output (external) or a built-in AST fallback. |
| **Outputs** | `AI_CONTEXT.md`, `project_context.json` (with `_meta` provenance). |
| **Analysis Depth** | Delegated: hygiene, QGIS, i18n, security and CC gates live in `qgis-plugin-analyzer`. |
| **Git Awareness** | Hotspots / churn, rendered into the context. |
| **Dependencies / Graph** | Import graph, unused imports, coupling, Mermaid diagram. |
| **Language Scope** | Python. |

> **Scope note:** `ai-context-core` is a **consumer** of analysis. By design it no
> longer performs security scanning, QGIS/i18n compliance, design-pattern
> detection or quality gates — those are owned by `qgis-plugin-analyzer`. It
> focuses on producing compact, versioned, provenance-tagged context artifacts
> for AI agents.

## Why `ai-context-core`?

### 1. Pluggable Context Compilation
Point it at `qgis-plugin-analyzer` output (`--source external`) or let it run its
built-in engine (`--source builtin`); either way you get the same rendered context
with provenance recorded in `project_context.json`.

### 2. Clean Ecosystem Boundaries
Hygiene (QGIS, i18n, security, quality gates) is single-sourced in
`qgis-plugin-analyzer`; scaffolding in `agentic-forge`. `ai-context-core` stays
focused on the context it compiles.

### 3. Actionable Technical Debt Identification
By combining **Git Churn/Hotspots** with **Cyclomatic Complexity**, the
`ai-ctx roadmap` command surfaces "Biological Debt" — files that are both complex
and frequently modified — guiding the AI assistant to the most critical areas for
refactoring.

## When to Choose

- ✅ **Choose `ai-context-core`** for professional Python/QGIS development,
  context compilation, verifiable/budgeted context artifacts, and high-fidelity
  AI pairing where structural context is critical.
- ❌ **Choose alternatives** for quick, one-off code dumps (Gitingest), real-time
  interactive terminal editing (Aider), or simple multi-language packaging
  (Repomix). For plugin hygiene/quality gates, use `qgis-plugin-analyzer`.
