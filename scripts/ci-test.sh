#!/bin/bash
# CI/CD test execution script
# Optimized for continuous integration environments

set -e  # Exit on any error

echo "🚀 Starting CI test execution..."

# Check environment
echo "Python version: $(python --version)"
echo "UV version: $(uv --version)"

# Install dependencies
echo "📦 Installing dependencies..."
uv sync --group test

# Run full validation
echo "🔍 Running full validation suite..."

# Linting
echo "Running ruff linting..."
uv run ruff check src tests --output-format=github

# Type checking
echo "Running mypy type checking..."
uv run mypy src --show-error-codes

# Tests with coverage
echo "Running tests with coverage..."
uv run pytest \
    --cov=src \
    --cov-report=term-missing \
    --cov-report=xml:coverage.xml \
    --cov-report=json:coverage.json \
    --cov-fail-under=95 \
    --cov-branch \
    --tb=short \
    -v

# Generate coverage badge
echo "Generating coverage report..."
python scripts/coverage.py

echo "✅ All CI checks passed!"