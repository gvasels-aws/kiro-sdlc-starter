---
inclusion: manual
---

# Phase 2: Testing (TEST)

**Mode**: Chat-driven
**Prerequisite**: Phase 1 (SPEC) complete with design.md containing data models and API contracts

## Purpose

Write failing tests BEFORE implementation (TDD Red phase). Tests define the expected behavior and serve as executable specifications.

## The TDD Approach

```
Design → Tests → Implementation
         ↑
    YOU ARE HERE
```

Tests are written from the design specifications:
- Data model tests from dataclass definitions
- Service tests from business logic requirements
- API tests from OpenAPI contracts

## Artifacts Produced

| Artifact | Location | Purpose |
|----------|----------|---------|
| Unit tests | `tests/unit/test_*.py` | Test individual functions/classes |
| Integration tests | `tests/integration/test_*.py` | Test API endpoints |
| Fixtures | `tests/fixtures/*_fixtures.py` | Shared test data |

## Workflow

### Step 1: Analyze Design

Read `design.md` to understand:
- Data models (dataclasses)
- Service methods required
- API endpoints and contracts

### Step 2: Write Model Tests

```python
# tests/unit/test_user.py
import pytest
from src.models.user import User, CreateUserRequest

class TestUser:
    """Tests for User model."""

    def test_user_creation(self) -> None:
        """Test creating a User instance."""
        user = User(id="usr_123", name="Test", email="test@example.com")

        assert user.id == "usr_123"
        assert user.name == "Test"
        assert user.email == "test@example.com"

    def test_user_default_email(self) -> None:
        """Test User with default empty email."""
        user = User(id="usr_123", name="Test")

        assert user.email == ""
```

### Step 3: Write Service Tests

```python
# tests/unit/test_user_service.py
import pytest
from src.services.user_service import UserService
from src.models.user import User, CreateUserRequest

class TestUserService:
    """Tests for UserService."""

    @pytest.fixture
    def service(self) -> UserService:
        return UserService()

    # Happy path
    def test_create_user_success(self, service: UserService) -> None:
        request = CreateUserRequest(name="John", email="john@example.com")
        user = service.create_user(request)
        assert user.name == "John"
        assert user.id.startswith("usr_")

    def test_get_user_exists(self, service: UserService) -> None:
        # Setup
        test_user = User(id="usr_123", name="Test", email="test@example.com")
        service.add_user(test_user)

        # Act
        result = service.get_user("usr_123")

        # Assert
        assert result is not None
        assert result.id == "usr_123"

    # Error cases
    def test_get_user_not_found(self, service: UserService) -> None:
        result = service.get_user("nonexistent")
        assert result is None

    def test_create_user_invalid_email_raises(self, service: UserService) -> None:
        request = CreateUserRequest(name="Test", email="invalid")
        with pytest.raises(ValueError, match="Invalid email"):
            service.create_user(request)

    # Edge cases
    @pytest.mark.parametrize("limit,offset,expected", [
        (5, 0, 5),
        (10, 0, 10),
        (10, 8, 2),
        (100, 0, 10),
    ])
    def test_list_users_pagination(
        self, service: UserService, limit: int, offset: int, expected: int
    ) -> None:
        for i in range(10):
            service.add_user(User(id=f"usr_{i}", name=f"User {i}"))

        result = service.list_users(limit=limit, offset=offset)
        assert len(result) == expected
```

### Step 4: Write Integration Tests

```python
# tests/integration/test_api.py
import pytest
from src.api.sample_api import get_users, get_user_by_id, create_user

class TestUserAPI:
    """Integration tests for User API."""

    def test_get_users_returns_list(self) -> None:
        result = get_users(limit=5, offset=0)
        assert isinstance(result, list)
        assert len(result) <= 5

    def test_get_user_by_id_found(self) -> None:
        result = get_user_by_id("usr_123")
        assert result is not None
        assert "id" in result

    def test_get_user_by_id_not_found(self) -> None:
        result = get_user_by_id("not_found")
        assert result is None

    def test_create_user_success(self) -> None:
        result = create_user(name="Test", email="test@example.com")
        assert "id" in result
        assert result["name"] == "Test"
```

### Step 5: Create Fixtures

```python
# tests/fixtures/user_fixtures.py
import pytest
from src.models.user import User, CreateUserRequest

@pytest.fixture
def sample_user() -> User:
    """Standard test user."""
    return User(id="usr_test", name="Test User", email="test@example.com")

@pytest.fixture
def create_user_request() -> CreateUserRequest:
    """Standard create user request."""
    return CreateUserRequest(name="New User", email="new@example.com")

@pytest.fixture
def user_list() -> list[User]:
    """List of test users."""
    return [
        User(id=f"usr_{i}", name=f"User {i}", email=f"user{i}@example.com")
        for i in range(10)
    ]
```

## Test Categories

| Category | Coverage | Focus |
|----------|----------|-------|
| Unit Tests | 70% | Individual functions, edge cases |
| Integration Tests | 20% | API endpoints, component interaction |
| Fixtures | - | Reusable test data |

## Verify Tests Fail

After writing tests, run them to confirm they fail:

```bash
pytest tests/ -v
```

Expected output:
```
FAILED tests/unit/test_user_service.py::TestUserService::test_create_user_success
FAILED tests/unit/test_user_service.py::TestUserService::test_get_user_exists
...
```

**Tests MUST fail before implementation.** This validates they're testing real behavior.

## Exit Criteria

Before moving to Phase 3 (CODE):
- [ ] Unit tests written for all service methods
- [ ] Integration tests written for all API endpoints
- [ ] All tests fail (Red phase confirmed)
- [ ] Test coverage structure mirrors source structure

## Chat Invocation

```
# Reference this phase
#steering:phases/02-test

# Start test writing
"Write tests for the user service based on the design"
```
