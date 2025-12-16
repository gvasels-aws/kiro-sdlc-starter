#!/usr/bin/env bash
# Quality gate: security scan + dependency checks

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================"
echo "  SDLC QUALITY GATE"
echo "======================================"
echo ""

# Step 1: Security scan
echo "Step 1/2: Security scanning..."
if ! "$SCRIPT_DIR/security-scan.sh"; then
    echo ""
    echo "✗ Quality gate failed at security scan"
    exit 1
fi
echo ""

# Step 2: Dependency check (if requirements.txt exists)
echo "Step 2/2: Checking dependencies..."
if [ -f "requirements.txt" ]; then
    if command -v safety &> /dev/null; then
        if safety check -r requirements.txt; then
            echo "✓ No known vulnerabilities in dependencies"
        else
            echo "✗ Vulnerable dependencies found"
            exit 1
        fi
    else
        echo "⚠ safety is not installed, skipping dependency check"
        echo "  Install with: pip install safety"
    fi
else
    echo "⚠ requirements.txt not found, skipping dependency check"
fi
echo ""

echo "======================================"
echo "✓ QUALITY GATE PASSED"
echo "======================================"
exit 0
