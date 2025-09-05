#!/bin/bash
# Test execution script for YFAS project
# Provides easy test execution with various options

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
COVERAGE=true
HTML_REPORT=false
VERBOSE=false
FAIL_FAST=false
MARKERS=""
TEST_PATH=""
FULL_VALIDATION=false

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -v, --verbose       Verbose output"
    echo "  -x, --fail-fast     Stop on first failure"
    echo "  -c, --no-coverage   Skip coverage reporting"
    echo "  -H, --html          Generate HTML coverage report"
    echo "  -m, --markers EXPR  Run tests matching marker expression"
    echo "  -p, --path PATH     Run specific test path"
    echo "  -f, --full          Run full validation suite"
    echo ""
    echo "Examples:"
    echo "  $0                           # Run all tests with coverage"
    echo "  $0 -v -H                     # Verbose with HTML report"
    echo "  $0 -m \"not slow\"             # Skip slow tests"
    echo "  $0 -p tests/test_client.py   # Run specific test file"
    echo "  $0 -f                        # Full validation (lint + type + test)"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -x|--fail-fast)
            FAIL_FAST=true
            shift
            ;;
        -c|--no-coverage)
            COVERAGE=false
            shift
            ;;
        -H|--html)
            HTML_REPORT=true
            shift
            ;;
        -m|--markers)
            MARKERS="$2"
            shift 2
            ;;
        -p|--path)
            TEST_PATH="$2"
            shift 2
            ;;
        -f|--full)
            FULL_VALIDATION=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Check if we're in the project root
if [[ ! -f "pyproject.toml" ]]; then
    print_status $RED "Error: Must be run from project root directory"
    exit 1
fi

# Check if uv is available
if ! command -v uv &> /dev/null; then
    print_status $RED "Error: uv is not installed or not in PATH"
    exit 1
fi

print_status $BLUE "🧪 YFAS Test Runner"
print_status $BLUE "=================="

# Run full validation if requested
if [[ "$FULL_VALIDATION" == "true" ]]; then
    print_status $YELLOW "Running full validation suite..."
    
    # Run linting
    print_status $BLUE "🔍 Running linting..."
    if uv run ruff check src tests; then
        print_status $GREEN "✅ Linting passed"
    else
        print_status $RED "❌ Linting failed"
        exit 1
    fi
    
    # Run type checking
    print_status $BLUE "🔎 Running type checking..."
    if uv run mypy src; then
        print_status $GREEN "✅ Type checking passed"
    else
        print_status $RED "❌ Type checking failed"
        exit 1
    fi
fi

# Build pytest command
PYTEST_CMD="uv run pytest"

# Add test path if specified
if [[ -n "$TEST_PATH" ]]; then
    PYTEST_CMD="$PYTEST_CMD $TEST_PATH"
fi

# Add markers if specified
if [[ -n "$MARKERS" ]]; then
    PYTEST_CMD="$PYTEST_CMD -m \"$MARKERS\""
fi

# Add fail-fast option
if [[ "$FAIL_FAST" == "true" ]]; then
    PYTEST_CMD="$PYTEST_CMD -x"
fi

# Add verbosity
if [[ "$VERBOSE" == "true" ]]; then
    PYTEST_CMD="$PYTEST_CMD -v"
else
    PYTEST_CMD="$PYTEST_CMD -q"
fi

# Add coverage options
if [[ "$COVERAGE" == "true" ]]; then
    PYTEST_CMD="$PYTEST_CMD --cov=src --cov-report=term-missing:skip-covered --cov-report=json:coverage.json --cov-fail-under=95 --cov-branch"
    
    if [[ "$HTML_REPORT" == "true" ]]; then
        PYTEST_CMD="$PYTEST_CMD --cov-report=html:htmlcov"
    fi
fi

# Run the tests
print_status $BLUE "🧪 Running tests..."
print_status $YELLOW "Command: $PYTEST_CMD"

START_TIME=$(date +%s)

if eval $PYTEST_CMD; then
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    print_status $GREEN "✅ Tests passed in ${DURATION}s"
    
    # Open HTML report if requested and available
    if [[ "$HTML_REPORT" == "true" && -f "htmlcov/index.html" ]]; then
        print_status $BLUE "📊 Opening HTML coverage report..."
        if command -v open &> /dev/null; then
            open htmlcov/index.html
        elif command -v xdg-open &> /dev/null; then
            xdg-open htmlcov/index.html
        else
            print_status $YELLOW "HTML report generated at htmlcov/index.html"
        fi
    fi
    
    exit 0
else
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    print_status $RED "❌ Tests failed after ${DURATION}s"
    exit 1
fi