#!/usr/bin/env bash
# Lint Python code using ruff

set -euo pipefail

echo "=== Running Ruff Linter ==="

# Check if ruff is installed
if ! command -v ruff &> /dev/null; then
    echo "Error: ruff is not installed"
    echo "Install with: pip install ruff"
    exit 2
fi

# Run ruff check on src and tests
if ruff check src/ tests/; then
    echo "✓ Lint check passed"
    exit 0
else
    echo "✗ Lint check failed"
    exit 1
fi
