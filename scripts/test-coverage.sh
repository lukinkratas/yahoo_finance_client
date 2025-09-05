#!/bin/bash
# Test coverage script for YFAS project

set -e

echo "🧪 Running tests with coverage..."

# Run tests with coverage
uv run pytest \
    --cov=src \
    --cov-report=term-missing \
    --cov-report=html:htmlcov \
    --cov-report=xml:coverage.xml \
    --cov-report=json:coverage.json \
    --cov-fail-under=95 \
    --cov-branch

echo ""
echo "📊 Coverage reports generated:"
echo "  - Terminal: displayed above"
echo "  - HTML: htmlcov/index.html"
echo "  - XML: coverage.xml"
echo "  - JSON: coverage.json"

# Check if HTML report exists and provide helpful message
if [ -f "htmlcov/index.html" ]; then
    echo ""
    echo "🌐 To view detailed HTML coverage report:"
    echo "  open htmlcov/index.html"
fi

echo ""
echo "✅ Coverage check completed successfully!"