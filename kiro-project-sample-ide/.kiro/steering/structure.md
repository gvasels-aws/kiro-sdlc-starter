---
inclusion: always
---

# Project Structure

## Directory Layout

```
kiro-project-sample-ide/
├── .kiro/                           # Kiro configuration
│   ├── steering/                    # AI context documents
│   │   ├── product.md               # Product vision & SDLC workflow
│   │   ├── tech.md                  # Technology stack
│   │   ├── structure.md             # This file
│   │   ├── tdd-workflow.md          # TDD best practices
│   │   └── phases/                  # Phase-specific instructions
│   │       ├── 01-spec.md
│   │       ├── 02-test.md
│   │       ├── 03-code.md
│   │       ├── 04-build.md
│   │       ├── 05-quality-gate.md
│   │       └── 06-docs.md
│   ├── specs/                       # Feature specifications
│   │   └── {feature-name}/
│   │       ├── requirements.md
│   │       ├── design.md
│   │       └── tasks.md
│   ├── settings/
│   │   └── mcp.json                 # MCP server configuration
│   └── hooks/
│       └── README.md                # Hook documentation
│
├── src/                             # Source code
│   ├── __init__.py
│   ├── api/                         # API layer (routes/handlers)
│   │   ├── __init__.py
│   │   └── {module}_api.py
│   ├── models/                      # Data models (dataclasses)
│   │   ├── __init__.py
│   │   └── {entity}.py
│   └── services/                    # Business logic
│       ├── __init__.py
│       └── {entity}_service.py
│
├── tests/                           # Test files
│   ├── __init__.py
│   ├── unit/                        # Unit tests
│   │   ├── __init__.py
│   │   └── test_{module}.py
│   ├── integration/                 # Integration tests
│   │   ├── __init__.py
│   │   └── test_{module}_integration.py
│   └── fixtures/                    # Test fixtures
│       ├── __init__.py
│       └── {entity}_fixtures.py
│
├── docs/                            # Documentation
│   ├── api.md                       # API documentation
│   └── {topic}.md
│
├── pyproject.toml                   # Project configuration
├── requirements.txt                 # Production dependencies
├── requirements-dev.txt             # Development dependencies
├── CHANGELOG.md                     # Change log
└── README.md                        # Project overview
```

## Naming Conventions

### Files

| Type | Pattern | Example |
|------|---------|---------|
| Source module | `{name}.py` | `user_service.py` |
| Test file | `test_{module}.py` | `test_user_service.py` |
| Fixture file | `{entity}_fixtures.py` | `user_fixtures.py` |
| API file | `{module}_api.py` | `sample_api.py` |

### Classes

| Type | Pattern | Example |
|------|---------|---------|
| Data model | `{Entity}` | `User`, `CreateUserRequest` |
| Service | `{Entity}Service` | `UserService` |
| Exception | `{Name}Error` | `ValidationError` |

### Functions

| Type | Pattern | Example |
|------|---------|---------|
| Public | `snake_case` | `get_user_by_id` |
| Private | `_snake_case` | `_validate_email` |
| Test | `test_{description}` | `test_create_user_success` |

### Variables

| Type | Pattern | Example |
|------|---------|---------|
| Constant | `UPPER_SNAKE_CASE` | `MAX_USERS` |
| Private | `_snake_case` | `_user_cache` |
| Parameter | `snake_case` | `user_id` |

## Layer Architecture

```
┌─────────────────────────────────┐
│           API Layer             │  src/api/
│   (HTTP handlers, validation)   │
├─────────────────────────────────┤
│         Service Layer           │  src/services/
│   (Business logic, operations)  │
├─────────────────────────────────┤
│          Model Layer            │  src/models/
│   (Data structures, types)      │
└─────────────────────────────────┘
```

### Import Rules

1. **API** can import from **Services** and **Models**
2. **Services** can import from **Models** only
3. **Models** should not import from other layers
4. No circular imports between modules

```python
# Good: api imports from service
from src.services.user_service import UserService

# Good: service imports from models
from src.models.user import User, CreateUserRequest

# Bad: models importing from services (avoid)
# from src.services.user_service import UserService  # Don't do this!
```

## Test Organization

### Mirror Source Structure

```
src/                          tests/unit/
├── models/                   ├── test_user.py
│   └── user.py
├── services/                 ├── test_user_service.py
│   └── user_service.py
└── api/                      └── test_sample_api.py
    └── sample_api.py
```

### Test Class Structure

```python
class TestUserService:
    """Test suite for UserService."""

    # Fixtures
    @pytest.fixture
    def service(self) -> UserService: ...

    # Happy path tests
    def test_create_user_success(self, service): ...
    def test_get_user_exists(self, service): ...

    # Error cases
    def test_create_user_invalid_email(self, service): ...
    def test_get_user_not_found(self, service): ...

    # Edge cases
    @pytest.mark.parametrize("limit,offset,expected", [...])
    def test_list_users_pagination(self, service, limit, offset, expected): ...
```
