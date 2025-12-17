---
inclusion: manual
---

# Phase 6: Documentation (DOCS)

**Mode**: Chat-driven
**Prerequisite**: Phase 5 (QUALITY GATE) passed

## Purpose

Generate comprehensive documentation before marking the feature complete. This ensures the codebase is well-documented and changes are tracked.

## Artifacts Produced

| Artifact | Location | Purpose |
|----------|----------|---------|
| API Documentation | `docs/api.md` | Endpoint documentation |
| CHANGELOG | `CHANGELOG.md` | Change history |
| README | `README.md` | Project overview |

## Workflow

### Step 1: Generate API Documentation

Document all public API endpoints:

```markdown
# API Documentation

## Endpoints

### GET /users

Retrieve a list of users with pagination.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| limit | int | No | 10 | Maximum users to return |
| offset | int | No | 0 | Number of users to skip |

**Response:**
```json
[
  {
    "id": "usr_abc123",
    "name": "John Doe",
    "email": "john@example.com"
  }
]
```

**Example:**
```bash
curl "http://localhost:8000/users?limit=5&offset=0"
```

### GET /users/{user_id}

Retrieve a single user by ID.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| user_id | string | Yes | The user's unique identifier |

**Response (200):**
```json
{
  "id": "usr_abc123",
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Response (404):**
```json
{
  "error": "User not found"
}
```

### POST /users

Create a new user.

**Request Body:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

**Response (201):**
```json
{
  "id": "usr_xyz789",
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

**Response (400):**
```json
{
  "error": "Invalid email format"
}
```
```

### Step 2: Update CHANGELOG

Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- User management API with CRUD operations
- User model with id, name, and email fields
- UserService with create, get, list, and add operations
- Email validation for user creation
- Pagination support for listing users
- Comprehensive test suite with 80%+ coverage

### Changed
- (none)

### Fixed
- (none)

### Security
- Input validation on all user endpoints
- Email format validation
```

### Step 3: Update README

```markdown
# Kiro SDLC Sample Project

A sample Python project demonstrating the Kiro SDLC workflow with Test-Driven Development.

## Features

- User management API (create, read, list)
- Email validation
- Pagination support
- Comprehensive test coverage (80%+)

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Run Linting

```bash
ruff check src/ tests/
```

### Run Type Check

```bash
mypy src/
```

## Project Structure

```
├── src/
│   ├── api/          # API endpoints
│   ├── models/       # Data models
│   └── services/     # Business logic
├── tests/
│   ├── unit/         # Unit tests
│   └── integration/  # Integration tests
└── docs/             # Documentation
```

## SDLC Workflow

This project follows a 6-phase SDLC:

1. **SPEC** - Define requirements and design
2. **TEST** - Write failing tests (TDD)
3. **CODE** - Implement to pass tests
4. **BUILD** - Lint, type check, coverage
5. **QUALITY GATE** - Security scan, code review
6. **DOCS** - Generate documentation

## License

MIT
```

### Step 4: Add Code Documentation

Ensure all public functions have docstrings:

```python
def create_user(self, request: CreateUserRequest) -> User:
    """Create a new user.

    Args:
        request: The user creation request containing name and email.

    Returns:
        The created User instance with generated ID.

    Raises:
        ValueError: If name is empty or email format is invalid.

    Example:
        >>> service = UserService()
        >>> request = CreateUserRequest(name="John", email="john@example.com")
        >>> user = service.create_user(request)
        >>> user.name
        'John'
    """
```

## Documentation Checklist

### API Documentation
- [ ] All endpoints documented
- [ ] Request/response formats specified
- [ ] Error responses documented
- [ ] Examples provided

### CHANGELOG
- [ ] All changes categorized (Added, Changed, Fixed, Security)
- [ ] Clear descriptions
- [ ] Version section (Unreleased or versioned)

### README
- [ ] Project description
- [ ] Installation instructions
- [ ] Usage examples
- [ ] Project structure

### Code Documentation
- [ ] All public functions have docstrings
- [ ] Complex logic explained
- [ ] Type hints complete

## Exit Criteria

Feature is complete when:
- [ ] API documentation generated
- [ ] CHANGELOG.md updated
- [ ] README.md updated
- [ ] All public functions documented
- [ ] All previous phases verified
- [ ] **Spec review triggered** (if all spec tasks complete)

## 🔍 Review Checkpoint

**After completing the DOCS phase:**

### If This is the Last Task in the Spec:

1. **Trigger "Spec Review (Full Validation)" manual hook**:
   - Open Agent Hooks panel
   - Find "Spec Review (Full Validation)"
   - Click ▷ (play button) to run
2. Review comprehensive spec-level report including:
   - All spec tasks completion status
   - Full test suite with coverage
   - Complete security scan
   - All changes since spec started
   - API contract validation
   - Documentation completeness
3. Address any findings
4. If READY FOR PR: Create PR to main branch
5. If NEEDS WORK: Address issues and re-review

### If More Tasks Remain:

1. **Trigger "Task Review (PR Emulation)" manual hook**
2. If APPROVED: merge task branch to group branch
3. Continue with remaining tasks

**Spec Review = Final Gate Before Production**
- Validates entire feature is production-ready
- Ensures all quality gates passed across all tasks
- Final check before deployment

See: `docs/REVIEW_HOOKS_SETUP.md` for hook configuration

## Chat Invocation

```
# Reference this phase
#steering:phases/06-docs

# Generate documentation
"Generate API documentation and update CHANGELOG"
```
