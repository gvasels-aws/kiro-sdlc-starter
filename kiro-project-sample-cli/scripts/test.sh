#!/usr/bin/env bash
# Run tests with coverage reporting

set -euo pipefail

echo "=== Running Tests with Coverage ==="

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "Error: pytest is not installed"
    echo "Install with: pip install pytest pytest-cov"
    exit 2
fi

# Run pytest with coverage
if pytest --cov=src --cov-report=term-missing --cov-fail-under=80; then
    echo "✓ Tests passed with 80%+ coverage"
    exit 0
else
    echo "✗ Tests failed or coverage below 80%"
    exit 1
fi
