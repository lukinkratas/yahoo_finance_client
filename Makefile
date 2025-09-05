.PHONY: install install-extras install-dev install-test format format lint typecheck test 

help:
	@echo "Available targets:"
	@echo "  install        - Run tests without coverage"
	@echo "  install-extras - Run tests without coverage"
	@echo "  install-dev    - Run tests without coverage"
	@echo "  install-test   - Run tests without coverage"
	@echo "  format         - Run tests without coverage"
	@echo "  lint           - Run tests without coverage"
	@echo "  typecheck      - Run tests without coverage"
	@echo "  test           - Run tests without coverage"
	@echo "  help           - Show this help message"

install:
	uv sync

install-extras:
	uv sync --all-extras

install-dev:
	uv sync --extra dev

install-test:
	uv sync --extra test

format:
	uv run --dev ruff format

lint:
	uv run --dev ruff check --fix

typecheck:
	uv run --dev mypy

test:
	uv run --test pytest