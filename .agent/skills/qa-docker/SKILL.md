---
name: qa-docker
description: Dockerized testing and clean-environment validation for ai-context-core.
trigger: when running integration tests or validating the package in clean environments.
---

# QA & Docker Standards

Ensures `ai-context-core` works correctly across environments and Python versions using isolated Docker containers.

## Core Principles
- **Isolation**: Tests run in clean environments to avoid "works on my machine" issues.
- **Reproducibility**: Dockerfiles versioned and stable.
- **Multi-version**: Validate against multiple Python versions (3.9+).

## Docker Workflow

### 1. Build Verification
```bash
make docker-build
```

### 2. Integration Tests
Run the suite inside a container:
```bash
make docker-test
```

### 3. Lint in Docker
```bash
make docker-lint
```

## Standards for Dockerfiles
- Use official `python:3.x-slim` images to minimize size.
- Install `uv` for fast dependency management.
- Copy only necessary files (use `.dockerignore`).

## Quality Gates
- All tests must pass in the Docker container.
- No permission issues when running as a non-root user.
- Package size within expected limits.
