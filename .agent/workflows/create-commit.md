---
description: Creates commit ensuring quality (Ruff), metrics, and changelog.
agent: QA Engineer
skills:
  - commit-standards
  - tech-stack
  - project-context
validation: |
  - Verify that ruff and black pass without errors
  - Confirm that ai-ctx analyze executed correctly
  - Validate that commit message follows Conventional Commits
---

This workflow is the gold standard for saving changes. It not only commits but cleans the code, updates project memory, and ensures documentation.

## Workflow Steps

1.  **Preparation and Cleanup (Automatic)**:
    
    🤖 **Agent Action**: Ensure code meets quality standards.
    
    Ensures code meets ruff and black standards to avoid hook failures.
    // turbo
    ```bash
    uv run ruff check --fix .
    uv run ruff format .
    uv run black .
    ```

2.  **Stage Changes**:
    Add the files you want to commit.
    ```bash
    git add .
    ```

3.  **Quality Sync (Guardian)**:
    
    🤖 **Agent Action**: Analyze quality metrics and alert on regressions.
    
    Records the impact of changes in the Project Brain before saving.
    // turbo
    ```bash
    uv run python -m ai_context_core.cli analyze
    ```
    
    🤖 **Agent Action**: Analyze quality metrics and alert if:
    - Cyclomatic complexity increased significantly
    - Code coverage decreased
    - New security issues or technical debt detected

4.  **Update CHANGELOG.md**:
    
    🤖 **Agent Action**: Insert entry in `[Unreleased]` section.
    
    *   Check `git status` and `git diff --cached`.
    *   Insert a concise line in the `[Unreleased]` section of `CHANGELOG.md` describing the value added.

5.  **Message Proposal (AI-Assisted)**:
    
    🤖 **Agent Action**: Use **commit-standards** skill to:
    - Analyze staged changes (`git diff --cached`)
    - Generate 2-3 message options following Conventional Commits
    - Validate format: correct type, appropriate scope, English, imperative
    - Suggest scope based on modified files (core, cli, analyzer, config, etc.)
    - Alert if there are breaking changes requiring `!` or footer
    
    Example suggestions:
    ```text
    Option 1: feat(cli): add --output flag for custom report location
    Option 2: refactor(analyzer): extract complexity calculation to separate module
    Option 3: fix(config): resolve profile loading error for custom paths
    ```

6.  **Commit**:
    Execute the commit with the approved message.
    ```bash
    git commit -m "type(scope): description" -m "detailed body"
    ```
    
    *If the pre-commit hook persists in failing:*
    1. Review the detected error messages.
    2. Execute `git add` again if there were automatic changes.
    3. Repeat the commit.

## Important Notes

- If `ruff` or `black` modified files in step 1, those changes will be included automatically in the commit.
- The message must follow **Conventional Commits** (see `docs/COMMIT_GUIDELINES.md`).
- If the generated message doesn't convince you, edit it before approving the final command.

**Philosophy**: Each commit is a unit of clean, documented, and metrically validated value.

