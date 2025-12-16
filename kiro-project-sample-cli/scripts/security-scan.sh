#!/usr/bin/env bash
# Run security analysis using bandit

set -euo pipefail

echo "=== Running Bandit Security Scanner ==="

# Check if bandit is installed
if ! command -v bandit &> /dev/null; then
    echo "Error: bandit is not installed"
    echo "Install with: pip install bandit"
    exit 2
fi

# Run bandit on src
# -ll: Only report issues of medium severity or higher
# -r: Recursive
if bandit -r src/ -ll; then
    echo "✓ Security scan passed"
    exit 0
else
    echo "✗ Security scan found issues"
    exit 1
fi
