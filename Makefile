.PHONY: test test-cov test-cov-html test-cov-report clean-cov help

# Default target
help:
	@echo "Available targets:"
	@echo "  test           - Run tests without coverage"
	@echo "  test-cov       - Run tests with coverage reporting"
	@echo "  test-cov-html  - Run tests with coverage and open HTML report"
	@echo "  test-cov-report- Generate detailed coverage report with badge"
	@echo "  clean-cov      - Clean coverage files"
	@echo "  help           - Show this help message"

# Run tests without coverage
test:
	uv run pytest

# Run tests with coverage
test-cov:
	uv run pytest \
		--cov=src \
		--cov-report=term-missing \
		--cov-report=html:htmlcov \
		--cov-report=xml:coverage.xml \
		--cov-report=json:coverage.json \
		--cov-fail-under=95 \
		--cov-branch

# Run tests with coverage and open HTML report
test-cov-html: test-cov
	@if [ -f "htmlcov/index.html" ]; then \
		echo "Opening HTML coverage report..."; \
		open htmlcov/index.html; \
	else \
		echo "HTML coverage report not found!"; \
	fi

# Generate detailed coverage report with badge
test-cov-report:
	uv run python scripts/coverage.py

# Clean coverage files
clean-cov:
	rm -rf htmlcov/
	rm -f .coverage coverage.xml coverage.json coverage_badge.txt

# Install development dependencies
install-dev:
	uv sync --group test

# Run tests using the new test runner
test-runner:
	python scripts/test_runner.py

# Run tests using shell script
test-shell:
	./scripts/run-tests.sh

# Run full validation suite
test-full:
	python scripts/test_runner.py --full

# Run fast tests (excluding slow ones)
test-fast:
	./scripts/run-tests.sh -m "not slow"

# Run tests with verbose output and HTML report
test-dev:
	./scripts/run-tests.sh -v -H