# Multi-stage Dockerfile for ai-context-core
# Optimized for development, testing, and production

# ============================================================================
# Stage 1: Base - Python + uv
# ============================================================================
FROM python:3.11-slim AS base

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash appuser

WORKDIR /app

# ============================================================================
# Stage 2: Development - Full environment with dev dependencies
# ============================================================================
FROM base AS development

# Copy project files (as root first)
COPY pyproject.toml ./
COPY README.md ./
COPY MANIFEST.in ./
COPY src/ ./src/
COPY tests/ ./tests/

# Install all dependencies (including dev) as root
RUN uv sync --all-extras

# Change ownership to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Default command for development
CMD ["/bin/bash"]

# ============================================================================
# Stage 3: Test - Run tests with coverage
# ============================================================================
FROM development AS test

# Run tests with coverage
CMD ["uv", "run", "pytest", "--cov=src/ai_context_core", "--cov-report=term-missing", "-v"]

# ============================================================================
# Stage 4: Production - Minimal runtime image
# ============================================================================
FROM base AS production

# Copy only necessary files
COPY pyproject.toml ./
COPY README.md ./
COPY MANIFEST.in ./
COPY src/ ./src/

# Install only runtime dependencies as root
RUN uv sync --no-dev

# Change ownership to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set entrypoint to ai-ctx CLI
ENTRYPOINT ["uv", "run", "ai-ctx"]
CMD ["--help"]
