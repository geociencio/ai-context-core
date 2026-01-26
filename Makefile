# Makefile for ai-context-core

.PHONY: help install test lint build docker-build docker-test docker-lint docker-shell docker-clean

help:
	@echo "Makefile for ai-context-core"
	@echo ""
	@echo "Usage:"
	@echo "  make install        - Install dependencies"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Run linter"
	@echo "  make build          - Build the package"
	@echo ""
	@echo "Docker commands:"
	@echo "  make docker-build   - Build Docker images"
	@echo "  make docker-test    - Run tests in Docker"
	@echo "  make docker-lint    - Run linter in Docker"
	@echo "  make docker-shell   - Open interactive shell in Docker"
	@echo "  make docker-clean   - Clean Docker images and containers"
	@echo ""

install:
	uv sync --all-extras

test:
	uv run pytest --cov=src/ai_context_core --cov-report=term-missing

lint:
	uv run ruff check .
	uv run ruff format .

build:
	uv build

# Docker targets
docker-build:
	docker build --target development -t ai-ctx:dev .
	docker build --target test -t ai-ctx:test .
	docker build --target production -t ai-ctx:prod .

docker-test:
	docker run --rm -v $(CURDIR)/src:/app/src -v $(CURDIR)/tests:/app/tests -e PYTHONPATH=/app/src ai-ctx:test

docker-lint:
	docker run --rm -v $(CURDIR)/src:/app/src -v $(CURDIR)/tests:/app/tests ai-ctx:dev sh -c "uv run ruff check . && uv run ruff format --check ."

docker-shell:
	docker run --rm -it -v $(CURDIR)/src:/app/src -v $(CURDIR)/tests:/app/tests ai-ctx:dev /bin/bash

docker-clean:
	docker rmi -f ai-ctx:dev ai-ctx:test ai-ctx:prod 2>/dev/null || true
