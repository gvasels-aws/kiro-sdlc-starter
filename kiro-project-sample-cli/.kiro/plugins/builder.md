---
plugin: builder
phase: 4
description: Run automated quality checks (lint, type check, test coverage)
---

# Builder Plugin (CLI Template)

## Purpose

Execute the build pipeline using shell scripts to ensure code quality.

## Workflow

1. **Load Context**
   - Read `.kiro/steering/phases/04-build.md` for build guidance

2. **Execute Build Script**
   ```bash
   ./scripts/build.sh
   ```

   This runs:
   - `./scripts/lint.sh` - Ruff linting
   - `./scripts/type-check.sh` - MyPy type checking
   - `./scripts/test.sh` - Pytest with 80%+ coverage

3. **Handle Failures**
   - If lint fails: Fix code style issues
   - If type check fails: Add/fix type hints
   - If tests fail: Fix implementation or tests
   - If coverage < 80%: Add more tests

## Quality Gates

- ✅ 0 lint errors
- ✅ 0 type errors
- ✅ All tests passing
- ✅ 80%+ test coverage

## Transition

Once build passes all quality gates, transition to Phase 5 (QUALITY_GATE) - security-checker plugin.
