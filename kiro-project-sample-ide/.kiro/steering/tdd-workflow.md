---
inclusion: always
---

# Test-Driven Development (TDD) Workflow

## The Three Laws of TDD

1. **Write a failing test before writing any production code**
2. **Write only enough test to demonstrate a failure**
3. **Write only enough production code to make the test pass**

## RED → GREEN → REFACTOR Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   ┌─────────┐                                                   │
│   │   RED   │  Write a failing test                            │
│   │         │  • Test should fail for the right reason         │
│   └────┬────┘  • Error message should be clear                 │
│        │                                                        │
│        ▼                                                        │
│   ┌─────────┐                                                   │
│   │  GREEN  │  Make the test pass                              │
│   │         │  • Write minimal code                            │
│   └────┬────┘  • Don't over-engineer                           │
│        │                                                        │
│        ▼                                                        │
│   ┌─────────┐                                                   │
│   │REFACTOR │  Improve the code                                │
│   │         │  • Keep tests passing                            │
│   └────┬────┘  • Remove duplication                            │
│        │                                                        │
│        └──────────────────────────────────────────► (repeat)   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Python TDD Example

### Step 1: RED - Write a Failing Test

```python
# tests/unit/test_user_service.py
import pytest
from src.services.user_service import UserService
from src.models.user import CreateUserRequest

class TestUserService:
    @pytest.fixture
    def service(self) -> UserService:
        return UserService()

    def test_create_user_success(self, service: UserService) -> None:
        """Test creating a user with valid input."""
        request = CreateUserRequest(name="John Doe", email="john@example.com")

        user = service.create_user(request)

        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.id.startswith("usr_")
```

Run the test - it should fail:
```bash
pytest tests/unit/test_user_service.py -v
# FAILED - ModuleNotFoundError or AssertionError
```

### Step 2: GREEN - Make the Test Pass

```python
# src/models/user.py
from dataclasses import dataclass

@dataclass
class User:
    id: str
    name: str
    email: str = ""

@dataclass
class CreateUserRequest:
    name: str
    email: str
```

```python
# src/services/user_service.py
import uuid
from src.models.user import User, CreateUserRequest

class UserService:
    def create_user(self, request: CreateUserRequest) -> User:
        return User(
            id=f"usr_{uuid.uuid4().hex[:8]}",
            name=request.name,
            email=request.email,
        )
```

Run the test - it should pass:
```bash
pytest tests/unit/test_user_service.py -v
# PASSED
```

### Step 3: REFACTOR - Improve the Code

Now that tests pass, improve the implementation:

```python
# src/services/user_service.py
import uuid
from typing import Optional
from src.models.user import User, CreateUserRequest

class UserService:
    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def create_user(self, request: CreateUserRequest) -> User:
        """Create a new user and store it."""
        user = User(
            id=self._generate_id(),
            name=request.name,
            email=request.email,
        )
        self._users[user.id] = user
        return user

    def _generate_id(self) -> str:
        """Generate a unique user ID."""
        return f"usr_{uuid.uuid4().hex[:8]}"
```

Run tests again to ensure they still pass:
```bash
pytest tests/unit/test_user_service.py -v
# PASSED
```

## Test Categories

### Unit Tests (70% of tests)

Test individual functions and classes in isolation.

```python
def test_validate_email_valid(self) -> None:
    """Test email validation with valid email."""
    assert validate_email("user@example.com") is True

def test_validate_email_invalid(self) -> None:
    """Test email validation with invalid email."""
    assert validate_email("not-an-email") is False
```

### Integration Tests (20% of tests)

Test interactions between components.

```python
def test_create_and_retrieve_user(self, service: UserService) -> None:
    """Test creating then retrieving a user."""
    request = CreateUserRequest(name="Jane", email="jane@example.com")
    created = service.create_user(request)

    retrieved = service.get_user(created.id)

    assert retrieved is not None
    assert retrieved.id == created.id
```

### Edge Case Tests (10% of tests)

Test boundary conditions and error handling.

```python
@pytest.mark.parametrize("limit,offset,expected", [
    (5, 0, 5),      # Normal case
    (10, 8, 2),     # Partial page
    (100, 0, 10),   # More than available
    (5, 100, 0),    # Offset beyond data
])
def test_list_users_pagination(
    self, service: UserService, limit: int, offset: int, expected: int
) -> None:
    """Test pagination edge cases."""
    # Setup: add 10 users
    for i in range(10):
        service.add_user(User(id=f"usr_{i}", name=f"User {i}"))

    result = service.list_users(limit=limit, offset=offset)

    assert len(result) == expected
```

## pytest Fixtures

### Basic Fixture

```python
@pytest.fixture
def service() -> UserService:
    """Create a fresh service instance."""
    return UserService()
```

### Fixture with Cleanup

```python
@pytest.fixture
def service_with_users(service: UserService) -> UserService:
    """Service pre-populated with test users."""
    for i in range(5):
        service.add_user(User(id=f"usr_{i}", name=f"User {i}"))
    return service
```

### Shared Fixtures

```python
# tests/fixtures/user_fixtures.py
import pytest
from src.models.user import User

@pytest.fixture
def sample_user() -> User:
    """Create a sample user for testing."""
    return User(id="usr_123", name="Test User", email="test@example.com")

@pytest.fixture
def admin_user() -> User:
    """Create an admin user for testing."""
    return User(id="usr_admin", name="Admin", email="admin@example.com")
```

## Coverage Requirements

| Metric | Minimum | Target |
|--------|---------|--------|
| Line Coverage | 80% | 90%+ |
| Branch Coverage | 70% | 85%+ |
| Function Coverage | 90% | 100% |

Run with coverage:
```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

## Common Patterns

### Testing Exceptions

```python
def test_create_user_empty_name_raises(self, service: UserService) -> None:
    """Test that empty name raises ValueError."""
    request = CreateUserRequest(name="", email="test@example.com")

    with pytest.raises(ValueError, match="Name cannot be empty"):
        service.create_user(request)
```

### Testing with Mocks

```python
from unittest.mock import Mock, patch

def test_service_calls_validator(self, service: UserService) -> None:
    """Test that service calls email validator."""
    with patch.object(service, '_validate_email') as mock_validate:
        mock_validate.return_value = True
        request = CreateUserRequest(name="Test", email="test@example.com")

        service.create_user(request)

        mock_validate.assert_called_once_with("test@example.com")
```

### Testing None/Optional Returns

```python
def test_get_user_not_found_returns_none(self, service: UserService) -> None:
    """Test that non-existent user returns None."""
    result = service.get_user("nonexistent_id")

    assert result is None
```
