---
inclusion: always
---

# Technology Stack

## Language

- **Python 3.11+**
- Type hints required for all public functions
- Dataclasses for data models
- Google-style docstrings

## Testing Framework

### pytest

Primary testing framework with these conventions:

```python
# Test file naming: test_<module>.py
# Test function naming: test_<description>

import pytest
from src.services.user_service import UserService

class TestUserService:
    """Test suite for UserService."""

    @pytest.fixture
    def service(self) -> UserService:
        """Create a fresh service instance."""
        return UserService()

    def test_create_user_success(self, service: UserService) -> None:
        """Test creating a user with valid input."""
        # Arrange
        request = CreateUserRequest(name="John", email="john@example.com")

        # Act
        user = service.create_user(request)

        # Assert
        assert user.name == "John"
        assert user.id.startswith("usr_")
```

### Coverage Requirements

- **Minimum**: 80% line coverage
- **Target**: 90%+ for critical paths
- **Enforcement**: `pytest --cov-fail-under=80`

### Test Categories

| Category | Location | Purpose |
|----------|----------|---------|
| Unit | `tests/unit/` | Individual functions/classes |
| Integration | `tests/integration/` | API endpoints, service interactions |
| Fixtures | `tests/fixtures/` | Shared test data and helpers |

## Linting

### ruff

Fast Python linter with these rules enabled:

```toml
[tool.ruff]
select = ["E", "F", "I", "N", "W", "B", "C4", "UP"]
```

| Rule | Description |
|------|-------------|
| E | pycodestyle errors |
| F | Pyflakes |
| I | isort (imports) |
| N | pep8-naming |
| W | pycodestyle warnings |
| B | flake8-bugbear |
| C4 | flake8-comprehensions |
| UP | pyupgrade |

## Type Checking

### mypy

Strict type checking enabled:

```toml
[tool.mypy]
python_version = "3.11"
strict = true
```

All public functions must have type annotations:

```python
def get_user(self, user_id: str) -> Optional[User]:
    """Get a user by ID."""
    return self._users.get(user_id)
```

## Security Scanning

### bandit

Static security analysis for Python:

```bash
bandit -r src/
```

Common issues detected:
- Hardcoded passwords/secrets
- SQL injection risks
- Shell injection risks
- Weak cryptographic functions

### safety

Dependency vulnerability scanning:

```bash
safety check -r requirements.txt
```

## Build Commands

```bash
# Install dependencies
pip install -e ".[dev]"

# Lint
ruff check src/ tests/

# Type check
mypy src/

# Run tests with coverage
pytest

# Security scan
bandit -r src/
safety check -r requirements.txt

# Full quality check
ruff check src/ tests/ && mypy src/ && pytest && bandit -r src/
```

## Code Style

- Line length: 100 characters
- Indentation: 4 spaces
- String quotes: Double quotes preferred
- Import order: stdlib → third-party → local (enforced by ruff)
