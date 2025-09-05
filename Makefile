.PHONY: install install-extras install-dev install-test format format lint typecheck test test-cov

help:
	@echo "Available targets:"
	@echo "  install        - Install the package and its dependencies"
	@echo "  install-extras - Install the package with all extras"
	@echo "  install-dev    - Install the package with dev dependencies"
	@echo "  install-test   - Install the package with test dependencies"
	@echo "  format         - Format the code using ruff"
	@echo "  lint           - Lint the code using ruff"
	@echo "  typecheck      - Type check the code using mypy"
	@echo "  test           - Run tests"
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
	uv run --dev mypy .

test:
	uv run --group test pytest tests/ --cov=yafin

test-cov:
	uv run --group test pytest tests/ --cov=yafin --cov-report=term-missing --cov-report=html:htmlcov --cov-fail-under=95 --cov-branch
