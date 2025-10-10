.PHONY: install install-all install-dev install-test format format lint typecheck test test-int test-full

help:
	@echo "Available targets:"
	@echo "  install        - Install the package and its dependencies"
	@echo "  install-all    - Install the package with all extras"
	@echo "  install-dev    - Install the package with dev dependencies"
	@echo "  install-test   - Install the package with test dependencies"
	@echo "  format         - Format the code using ruff"
	@echo "  lint           - Lint the code using ruff"
	@echo "  typecheck      - Type check the code using mypy"
	@echo "  test           - Run unit tests"
	@echo "  test-int       - Run integration tests"
	@echo "  test-full      - Run all tests with html coverage"
	@echo "  clean          - Removes htmlcov, __pycache__, pytest mypy and ruff cache dirs"
	@echo "  help           - Show this help message"

install:
	uv sync

install-all:
	uv sync --all-extras

install-dev:
	uv sync --extra dev

install-test:
	uv sync --extra test

format:
	uv run --group dev ruff format

lint:
	uv run --group dev ruff check --fix

typecheck:
	uv run --group dev mypy .

test:
	uv run --group test pytest -m "not integration" -p no:warnings

test-int:
	uv run --group test pytest -m integration -p no:warnings

test-full:
	uv run --group test pytest --cov-report=html:htmlcov --cov-fail-under=95

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache htmlcov .ruff_cache
