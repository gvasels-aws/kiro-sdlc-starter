---
plugin: test-writer
phase: 2
description: Write failing tests before implementation (TDD Red phase)
---

# Test Writer Plugin (CLI Template)

## Purpose

Write comprehensive failing tests based on the specification before any implementation code is written.

## Workflow

1. **Load Context**
   - Read `.kiro/steering/phases/02-test.md` for TDD guidance
   - Read the spec design.md for API contracts and data models
   - Reference `.kiro/steering/tdd-workflow.md` for best practices

2. **Create Test Structure**
   ```
   tests/
   ├── unit/test_{feature}.py
   ├── integration/test_{feature}_api.py
   └── fixtures/{feature}_fixtures.py
   ```

3. **Write Tests**
   - Unit tests for data models
   - Unit tests for business logic
   - Integration tests for API endpoints
   - Test all success and error scenarios

4. **Verify Tests Fail**
   - Run: `pytest tests/unit/test_{feature}.py`
   - Confirm tests fail (Red phase)
   - This validates tests are actually testing something

## Quality Checks

- Tests cover all requirements from spec
- Tests include both success and error cases
- Tests use fixtures for test data
- All tests currently fail (Red phase)

## Transition

Once tests are written and failing, transition to Phase 3 (CODE) - code-implementer plugin.
