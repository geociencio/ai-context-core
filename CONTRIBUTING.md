# Contributing to AI Context Core

We love your input! We want to make contributing to `ai-context-core` as easy and transparent as possible.

## 🛠️ Development Setup

This project uses `uv` for dependency management, ensuring fast and reliable builds.

1.  **Install uv** (if you haven't):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Clone and Sync**:
    ```bash
    git clone https://github.com/geociencio/ai-context-core.git
    cd ai-context-core
    uv sync
    ```

3.  **Activate the virtual environment**:
    ```bash
    source .venv/bin/activate
    ```

4.  **Run tool locally**:
    ```bash
    ai-ctx --help
    ```

## 🧪 Testing

We use `pytest` for testing and `pytest-cov` to measure code coverage. We aim for high test coverage.

1.  **Run tests**:
    ```bash
    uv run pytest
    ```

2.  **Run tests with coverage report**:
    ```bash
    uv run pytest --cov=src/ai_context_core --cov-report=term-missing
    ```

## 🎨 Code Style

We use `ruff` to keep the code clean and consistent.

- **Check code**:
    ```bash
    uv run ruff check .
    ```
- **Format code**:
    ```bash
    uv run ruff format .
    ```

## 🪝 Pre-commit Hooks

We use `pre-commit` to automatically run `ruff` before each commit. This helps to maintain code quality and prevent bugs from being introduced into the codebase.

1.  **Install the pre-commit hooks**:
    ```bash
    uv run pre-commit install
    ```

Now, `ruff` will run automatically on every commit.

## 📝 Commit Messages

We follow the **Conventional Commits** specification. This allows us to automate versioning and changelogs.

Format: `<type>(<scope>): <subject>`

**Types**:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools and libraries such as documentation generation

**Example**:
```
feat(cli): add new 'profiles' command to list available configs
fix(engine): resolve timeout issue on large files
docs: update architecture details
```

## 🚀 Submitting Pull Requests

1.  **Create a new branch**:
    ```bash
    git checkout -b feat/my-new-feature
    ```
2.  **Make your changes and commit them**:
    ```bash
    git commit -am 'feat(scope): add my new feature'
    ```
3.  **Push to your fork**:
    ```bash
    git push origin feat/my-new-feature
    ```
4.  **Create a pull request** on the `main` branch of the original repository.

Please provide a clear and descriptive pull request title and description. Explain the problem you are solving and the changes you have made.
