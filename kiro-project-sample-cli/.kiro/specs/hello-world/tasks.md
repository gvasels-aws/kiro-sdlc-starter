# Tasks: Hello World Example

**Spec Name:** hello-world
**Total Tasks:** 6

## Task Breakdown

### Task 1: Data Models

**Priority:** High
**Estimated Effort:** Small
**Dependencies:** None

**Description:**
Create data models for greeting requests and responses.

**Files to Create:**
- `src/models/greeting.py`

**Implementation Details:**
- Create `GreetingRequest` dataclass
  - `name: str`
  - `greeting_type: Optional[str] = "Hello"`
- Create `GreetingResponse` dataclass
  - `message: str`
  - `name: str`
  - `greeting_type: str`

**Acceptance Criteria:**
- [ ] Both dataclasses defined with type hints
- [ ] Docstrings added
- [ ] File passes mypy type check

---

### Task 2: Greeting Service - Tests (TDD Red)

**Priority:** High
**Estimated Effort:** Small
**Dependencies:** Task 1

**Description:**
Write failing tests for the greeting service following TDD.

**Files to Create:**
- `tests/unit/test_greeting_service.py`
- `tests/fixtures/greeting_fixtures.py`

**Test Cases:**
1. `test_generate_greeting_success` - Valid name returns greeting
2. `test_generate_greeting_custom_type` - Custom greeting type
3. `test_generate_greeting_empty_name` - Empty name raises ValueError
4. `test_generate_greeting_whitespace` - Whitespace name raises ValueError

**Fixtures:**
- `greeting_service()` - Fresh service instance
- `valid_request()` - Valid greeting request

**Acceptance Criteria:**
- [ ] All 4 test cases written
- [ ] Tests fail appropriately (RED phase)
- [ ] Fixtures defined

---

### Task 3: Greeting Service - Implementation (TDD Green)

**Priority:** High
**Estimated Effort:** Medium
**Dependencies:** Task 2

**Description:**
Implement greeting service to make tests pass.

**Files to Create:**
- `src/services/greeting_service.py`

**Implementation:**
- `GreetingService` class
  - `generate_greeting(request: GreetingRequest) -> GreetingResponse`
  - `_validate_name(name: str) -> None` (private)

**Logic:**
```python
def generate_greeting(self, request: GreetingRequest) -> GreetingResponse:
    self._validate_name(request.name)
    message = f"{request.greeting_type}, {request.name.strip()}!"
    return GreetingResponse(
        message=message,
        name=request.name.strip(),
        greeting_type=request.greeting_type
    )

def _validate_name(self, name: str) -> None:
    if not name or not name.strip():
        raise ValueError("Name cannot be empty or whitespace")
```

**Acceptance Criteria:**
- [ ] All tests pass (GREEN phase)
- [ ] Code passes mypy type check
- [ ] Code passes ruff lint
- [ ] 100% coverage for service

---

### Task 4: Greeting API - Tests (TDD Red)

**Priority:** Medium
**Estimated Effort:** Small
**Dependencies:** Task 3

**Description:**
Write failing tests for the greeting API endpoint.

**Files to Create:**
- `tests/unit/test_greeting_api.py`

**Test Cases:**
1. `test_greet_endpoint_success` - Valid request returns 200
2. `test_greet_endpoint_missing_name` - Missing name returns 400
3. `test_greet_endpoint_custom_type` - Custom greeting type works

**Acceptance Criteria:**
- [ ] All 3 test cases written
- [ ] Tests fail appropriately (RED phase)

---

### Task 5: Greeting API - Implementation (TDD Green)

**Priority:** Medium
**Estimated Effort:** Medium
**Dependencies:** Task 4

**Description:**
Implement greeting API endpoint to make tests pass.

**Files to Create:**
- `src/api/greeting_api.py`

**Implementation:**
```python
def greet(name: Optional[str] = None, type: str = "Hello") -> dict:
    """Generate greeting via API."""
    if not name:
        return {
            "error": "Invalid request",
            "detail": "Name parameter is required"
        }, 400

    try:
        service = GreetingService()
        request = GreetingRequest(name=name, greeting_type=type)
        response = service.generate_greeting(request)

        return {
            "message": response.message,
            "name": response.name,
            "greeting_type": response.greeting_type
        }, 200
    except ValueError as e:
        return {
            "error": "Invalid request",
            "detail": str(e)
        }, 400
```

**Acceptance Criteria:**
- [ ] All tests pass (GREEN phase)
- [ ] Code passes type check and lint
- [ ] 90%+ coverage for API

---

### Task 6: Documentation & Quality Gate

**Priority:** Medium
**Estimated Effort:** Small
**Dependencies:** Task 5

**Description:**
Generate documentation and run full quality checks.

**Files to Create/Update:**
- `docs/api.md` - API documentation
- `CHANGELOG.md` - Add entry for hello-world feature

**Tasks:**
1. Generate API documentation
2. Update CHANGELOG.md
3. Run full build pipeline: `./scripts/build.sh`
4. Run quality gate: `./scripts/quality-gate.sh`

**Acceptance Criteria:**
- [ ] API documentation complete
- [ ] CHANGELOG entry added
- [ ] Build pipeline passes
- [ ] Quality gate passes
- [ ] Overall coverage 90%+

---

## Implementation Order

Follow this sequence for optimal TDD workflow:

1. **Task 1** (Models) - Foundation
2. **Task 2** (Service Tests) - TDD Red
3. **Task 3** (Service Implementation) - TDD Green
4. **Task 4** (API Tests) - TDD Red
5. **Task 5** (API Implementation) - TDD Green
6. **Task 6** (Documentation) - Complete

## Quality Checklist

Before marking complete, ensure:

- [ ] All tests pass: `pytest`
- [ ] 90%+ coverage: `pytest --cov=src --cov-fail-under=90`
- [ ] No lint errors: `./scripts/lint.sh`
- [ ] No type errors: `./scripts/type-check.sh`
- [ ] No security issues: `./scripts/security-scan.sh`
- [ ] Documentation complete
- [ ] CHANGELOG updated

## Notes

This is a reference implementation demonstrating:
- TDD workflow (Red → Green → Refactor)
- Layer architecture (Model → Service → API)
- Automated quality gates via scripts
- Spec-driven development with spec-workflow MCP
