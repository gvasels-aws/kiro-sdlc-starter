---
inclusion: manual
---

# Phase 3: Implementation (CODE)

**Mode**: Chat-driven
**Prerequisite**: Phase 2 (TEST) complete with failing tests

## Purpose

Write minimal code to make tests pass (TDD Green phase). Focus on making tests green, not on perfect code—refactoring comes after.

## The TDD Approach

```
Tests (failing) → Implementation → Tests (passing)
       ↑                                  ↑
  Phase 2 done                    YOU ARE HERE
```

## Implementation Order

Follow a layered approach, implementing bottom-up:

```
1. Models (no dependencies)
   ↓
2. Services (depends on models)
   ↓
3. API (depends on services)
```

## Workflow

### Step 1: Implement Models

```python
# src/models/user.py
"""User data models."""
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    """User entity."""
    id: str
    name: str
    email: str = ""

@dataclass
class CreateUserRequest:
    """Request model for creating a user."""
    name: str
    email: str

@dataclass
class UserResponse:
    """Response model for user operations."""
    id: str
    name: str
    email: str
```

Run model tests:
```bash
pytest tests/unit/test_user.py -v
# Should pass
```

### Step 2: Implement Services

```python
# src/services/user_service.py
"""User service with business logic."""
import re
import uuid
from typing import Optional
from src.models.user import User, CreateUserRequest

class UserService:
    """Service for user operations."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def create_user(self, request: CreateUserRequest) -> User:
        """Create a new user."""
        self._validate_request(request)

        user = User(
            id=self._generate_id(),
            name=request.name,
            email=request.email,
        )
        self._users[user.id] = user
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        return self._users.get(user_id)

    def add_user(self, user: User) -> None:
        """Add a user directly (for testing/migration)."""
        self._users[user.id] = user

    def list_users(self, limit: int = 10, offset: int = 0) -> list[User]:
        """List users with pagination."""
        users = list(self._users.values())
        return users[offset:offset + limit]

    def _generate_id(self) -> str:
        """Generate a unique user ID."""
        return f"usr_{uuid.uuid4().hex[:8]}"

    def _validate_request(self, request: CreateUserRequest) -> None:
        """Validate create user request."""
        if not request.name or not request.name.strip():
            raise ValueError("Name cannot be empty")

        if not self._is_valid_email(request.email):
            raise ValueError("Invalid email format")

    def _is_valid_email(self, email: str) -> bool:
        """Check if email format is valid."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
```

Run service tests:
```bash
pytest tests/unit/test_user_service.py -v
# Should pass
```

### Step 3: Implement API

```python
# src/api/sample_api.py
"""Sample API module."""
from typing import Optional
from src.models.user import User, CreateUserRequest
from src.services.user_service import UserService

# Module-level service instance
_service = UserService()

def get_users(limit: int = 10, offset: int = 0) -> list[dict]:
    """Get list of users with pagination."""
    users = _service.list_users(limit=limit, offset=offset)
    return [_user_to_dict(u) for u in users]

def get_user_by_id(user_id: str) -> Optional[dict]:
    """Get a single user by ID."""
    user = _service.get_user(user_id)
    if user is None:
        return None
    return _user_to_dict(user)

def create_user(name: str, email: str) -> dict:
    """Create a new user."""
    request = CreateUserRequest(name=name, email=email)
    user = _service.create_user(request)
    return _user_to_dict(user)

def _user_to_dict(user: User) -> dict:
    """Convert User to dictionary."""
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }
```

Run all tests:
```bash
pytest tests/ -v
# All should pass
```

## Implementation Principles

### Minimal Code

Only write code needed to pass tests:

```python
# BAD: Over-engineering
class UserService:
    def __init__(self, cache=None, validator=None, logger=None):
        self.cache = cache or RedisCache()
        self.validator = validator or EmailValidator()
        self.logger = logger or Logger()
        # ... complex setup not needed yet

# GOOD: Minimal implementation
class UserService:
    def __init__(self) -> None:
        self._users: dict[str, User] = {}
```

### Run Tests Frequently

After each change:
```bash
pytest tests/unit/test_user_service.py::TestUserService::test_create_user_success -v
```

### Refactor After Green

Once tests pass, improve code quality:

1. Extract helper methods
2. Improve naming
3. Add type hints
4. Remove duplication

```python
# Before refactor
def create_user(self, request):
    if not request.name:
        raise ValueError("Name cannot be empty")
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', request.email):
        raise ValueError("Invalid email")
    # ...

# After refactor
def create_user(self, request: CreateUserRequest) -> User:
    self._validate_request(request)
    # ...

def _validate_request(self, request: CreateUserRequest) -> None:
    if not request.name or not request.name.strip():
        raise ValueError("Name cannot be empty")
    if not self._is_valid_email(request.email):
        raise ValueError("Invalid email format")

def _is_valid_email(self, email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

## Exit Criteria

Before moving to Phase 4 (BUILD):
- [ ] All tests passing (Green phase)
- [ ] No test skipped or disabled
- [ ] Code follows project structure
- [ ] Basic refactoring complete
- [ ] **Task review triggered** (if task complete)

## 🔍 Review Checkpoint

**After completing a task in the CODE phase:**

1. Mark task as "completed" in TodoWrite
2. **Trigger "Task Review (PR Emulation)" manual hook**:
   - Open Agent Hooks panel
   - Find "Task Review (PR Emulation)"
   - Click ▷ (play button) to run
3. Review the generated report
4. If APPROVED: merge task branch to group branch
5. If CHANGES REQUESTED: fix issues and re-review

**Why review after CODE phase?**
- Catches issues while context is fresh
- Easier to fix problems immediately
- Prevents accumulation of technical debt

See: `docs/REVIEW_HOOKS_SETUP.md` for hook configuration

## Chat Invocation

```
# Reference this phase
#steering:phases/03-code

# Start implementation
"Implement the UserService to make the tests pass"
```
