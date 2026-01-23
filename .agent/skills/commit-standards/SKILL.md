---
name: commit-standards
description: Git commit message guidelines (Conventional Commits)
trigger: commit, git, pr, merge
---

# Commit Standards

## Conventional Commits
All commits must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

**Format**:
`<type>(<scope>): <subject>`

**Types**:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools and libraries such as documentation generation

## Examples
- `feat(auth): add google login support`
- `fix(ui): fix button alignment on mobile`
- `docs(readme): update installation instructions`

## Workflow
- Use `/crea-commit` workflow (if available) to ensure standards are met.
