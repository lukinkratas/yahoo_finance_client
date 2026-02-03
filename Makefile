.PHONY: install install-editable format fmt lint lint-fix typechk fetch-mocks test test-int test-perf test-build test-all doc doc-serve build publish changelog clean-up

help:
	@echo "Available targets:"
	@echo "  install          - Install the package and its dependencies"
	@echo "  install-editable - Make the package installation editable"
	@echo "  fmt              - Format the code using ruff"
	@echo "  lint             - Check linting of the code using ruff"
	@echo "  lint-fix         - Check and fix linting of the code using ruff"
	@echo "  typechk          - Type check the code using mypy"
	@echo "  fetch-mocks      - Run script to fetch json mocks for fixtures"
	@echo "  test             - Run unit tests"
	@echo "  test-int         - Run integration tests"
	@echo "  test-perf        - Run performance tests"
	@echo "  test-build       - Test built package"
	@echo "  test-all         - Run all tests with html coverage"
	@echo "  clean-up         - Clean up - remove htmlcov, __pycache__, pytest mypy and ruff cache dirs"
	@echo "  doc              - build documentation html"
	@echo "  doc-serve        - serve documentation html"
	@echo "  build            - Build package - bdist wheel and sdist"
	@echo "  publish          - Publish the package to pypi.org"
	@echo "  changelog        - Create CHANGELOG.md from git log"
	@echo "  help             - Show this help message"

install:
	uv sync

install-editable:
	uv pip install -e .

fmt:
	uv run --dev ruff format

lint:
	uv run --dev ruff check

lint-fix:
	uv run --dev ruff check --fix

typechk:
	uv run --dev mypy .

fetch-mocks:
	uv run --dev python -m scripts.fetch_mocks

test:
	$(MAKE) install-editable
	uv run --dev pytest tests/unit --cov=yafin --cov-report=term-missing --cov-branch

test-int:
	$(MAKE) install-editable
	uv run --dev pytest tests/integration --cov=yafin --cov-report=term-missing --cov-branch

test-perf:
	$(MAKE) install-editable
	uv run --dev pytest tests/performance --benchmark-autosave

test-build:
	uv run --isolated --no-project --with dist/*.whl pytest tests/unit
	uv run --isolated --no-project --with dist/*.tar.gz pytest tests/unit

test-all:
	$(MAKE) install-editable
	uv run --dev pytest tests/ -m "not performance" --cov=yafin --cov-report=term-missing --cov-branch --cov-fail-under=95 --cov-report=html:htmlcov

clean-up:
	rm -rvf __pycache__ scripts/__pycache__ tests/__pycache__ tests/integration/__pycache__ tests/unit/__pycache__ yafin/__pycache__ .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov main.log dist yafin.egg-info site *.csv

doc:
	$(MAKE) install-editable
	uv run --group doc mkdocs build

doc-serve:
	uv run --group doc mkdocs serve

build:
	uv build

publish:
	[[ -n $UV_PUBLISH_TOKEN ]] && uv publish --token $UV_PUBLISH_TOKEN || echo "Env var UV_PUBLISH_TOKEN not set."

changelog:
	git log \
		--decorate-refs-exclude=HEAD \
		--decorate-refs-exclude="refs/remotes/*" \
		--decorate-refs-exclude="refs/heads/*" \
		--pretty=format:"%(decorate:prefix=%n,suffix=%n,separator=|,tag=##,pointer=) - %s" > CHANGELOG.md
