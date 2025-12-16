#!/usr/bin/env bash
# Type check Python code using mypy

set -euo pipefail

echo "=== Running Mypy Type Checker ==="

# Check if mypy is installed
if ! command -v mypy &> /dev/null; then
    echo "Error: mypy is not installed"
    echo "Install with: pip install mypy"
    exit 2
fi

# Run mypy on src
if mypy src/; then
    echo "✓ Type check passed"
    exit 0
else
    echo "✗ Type check failed"
    exit 1
fi
