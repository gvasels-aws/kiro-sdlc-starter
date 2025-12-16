# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-15

### Added

- **Project Structure**
  - Kiro SDLC sample project initialized
  - `.kiro/` directory with steering, specs, settings, and hooks
  - `src/` directory with api, models, and services layers
  - `tests/` directory with unit and integration tests
  - `docs/` directory for documentation

- **Steering Documents**
  - `product.md` - SDLC workflow definition with 6 phases
  - `tech.md` - Python 3.11+ stack documentation
  - `structure.md` - Directory layout and naming conventions
  - `tdd-workflow.md` - RED-GREEN-REFACTOR cycle guide
  - Phase-specific steering (01-spec through 06-docs)

- **Specifications**
  - Spec 1: Kiro IDE SDLC Replication (requirements, design, tasks)
  - Spec 2: Kiro CLI SDLC with spec-workflow MCP integration

- **User Management API**
  - `User` dataclass with id, name, email fields
  - `CreateUserRequest` dataclass for input validation
  - `UserService` with create, get, add, list operations
  - Email validation with regex pattern matching
  - Name validation (non-empty requirement)
  - Pagination support for list_users

- **API Functions**
  - `get_users(limit, offset)` - List users with pagination
  - `get_user_by_id(user_id)` - Get single user
  - `create_user(name, email)` - Create new user
  - `validate_input(data)` - Input validation helper

- **Testing**
  - 39 tests (unit and integration)
  - 100% code coverage
  - pytest with coverage configured
  - Test fixtures for reusable test data

- **Configuration**
  - `pyproject.toml` with pytest, ruff, mypy, bandit config
  - `.kiro/settings/mcp.json` with docs-mcp, context7, spec-workflow servers
  - Hook documentation in `.kiro/hooks/README.md`

### Technical Details

- **Quality Gates**: ruff (lint), mypy (types), pytest (tests), bandit (security)
- **Coverage Threshold**: 80% minimum, achieved 100%
- **MCP Integration**: spec-workflow for specification management

[Unreleased]: https://github.com/user/repo/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/user/repo/releases/tag/v0.1.0
