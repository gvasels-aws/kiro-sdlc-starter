#!/usr/bin/env bash
# Full build pipeline: lint + type check + tests

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================"
echo "  SDLC BUILD PIPELINE"
echo "======================================"
echo ""

# Step 1: Lint
echo "Step 1/3: Linting..."
if ! "$SCRIPT_DIR/lint.sh"; then
    echo ""
    echo "✗ Build failed at linting stage"
    exit 1
fi
echo ""

# Step 2: Type check
echo "Step 2/3: Type checking..."
if ! "$SCRIPT_DIR/type-check.sh"; then
    echo ""
    echo "✗ Build failed at type checking stage"
    exit 1
fi
echo ""

# Step 3: Tests
echo "Step 3/3: Running tests..."
if ! "$SCRIPT_DIR/test.sh"; then
    echo ""
    echo "✗ Build failed at testing stage"
    exit 1
fi
echo ""

echo "======================================"
echo "✓ BUILD PIPELINE COMPLETED SUCCESSFULLY"
echo "======================================"
exit 0
