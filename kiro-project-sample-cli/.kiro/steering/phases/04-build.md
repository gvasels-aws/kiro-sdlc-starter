---
inclusion: fileMatch: "*.py"
---

# Phase 4: Build Verification (BUILD)

**Mode**: Hook-assisted (automated on file save)
**Prerequisite**: Phase 3 (CODE) complete with passing tests

## Purpose

Verify code quality through automated checks. This phase runs lint, type checks, tests with coverage, ensuring the codebase meets quality standards.

## Automated Hooks

These hooks run automatically:

| Hook | Trigger | Command |
|------|---------|---------|
| Lint on Save | File Save (`**/*.py`) | `ruff check {file}` |
| Type Check | Manual / Build | `mypy src/` |
| Test + Coverage | Manual / Build | `pytest --cov` |

## Quality Gates

| Check | Threshold | Command |
|-------|-----------|---------|
| Lint | 0 errors | `ruff check src/ tests/` |
| Type Check | 0 errors | `mypy src/` |
| Tests | 100% pass | `pytest` |
| Coverage | 80%+ | `pytest --cov-fail-under=80` |

## Workflow

### Step 1: Lint Check

```bash
ruff check src/ tests/
```

Expected output:
```
All checks passed!
```

Common fixes:
```python
# E501: Line too long
# Fix: Break into multiple lines

# F401: Imported but unused
# Fix: Remove unused import

# I001: Import order
# Fix: Run `ruff check --fix`
```

Auto-fix safe issues:
```bash
ruff check src/ tests/ --fix
```

### Step 2: Type Check

```bash
mypy src/
```

Expected output:
```
Success: no issues found in X source files
```

Common fixes:
```python
# error: Missing return type annotation
def get_user(self, user_id):  # Bad
def get_user(self, user_id: str) -> Optional[User]:  # Good

# error: Incompatible return type
def get_user(self) -> User:
    return None  # Bad: should return Optional[User]
```

### Step 3: Test Suite

```bash
pytest tests/ -v
```

Expected output:
```
tests/unit/test_user.py::TestUser::test_user_creation PASSED
tests/unit/test_user_service.py::TestUserService::test_create_user_success PASSED
...
======================== X passed in 0.XXs ========================
```

### Step 4: Coverage Report

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

Expected output:
```
Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
src/__init__.py                   0      0   100%
src/api/sample_api.py            15      0   100%
src/models/user.py               10      0   100%
src/services/user_service.py     25      2    92%   45-46
-----------------------------------------------------------
TOTAL                            50      2    96%

Required test coverage of 80% reached. Total coverage: 96%
```

### Step 5: Full Build Verification

Run all checks in sequence:
```bash
ruff check src/ tests/ && mypy src/ && pytest --cov=src --cov-fail-under=80
```

Or use a Makefile target:
```makefile
# Makefile
.PHONY: build
build:
	ruff check src/ tests/
	mypy src/
	pytest --cov=src --cov-fail-under=80
```

## Failure Handling

### Lint Failures

1. Read error message
2. Fix in source file
3. Re-run lint check
4. Hook will auto-check on save

### Type Check Failures

1. Add missing type annotations
2. Fix incompatible types
3. Use `Optional[]` for nullable returns
4. Re-run mypy

### Test Failures

**Go back to Phase 3 (CODE)**
1. Read failing test
2. Fix implementation
3. Re-run specific test
4. Re-run full suite

### Coverage Failures

**Go back to Phase 2 (TEST)**
1. Identify uncovered lines
2. Write additional tests
3. Re-run coverage

## Exit Criteria

Before moving to Phase 5 (QUALITY GATE):
- [ ] `ruff check` passes with 0 errors
- [ ] `mypy` passes with 0 errors
- [ ] All tests pass (100%)
- [ ] Coverage >= 80%

## Chat Invocation

```
# Reference this phase
#steering:phases/04-build

# Run build verification
"Run the full build verification"
```
