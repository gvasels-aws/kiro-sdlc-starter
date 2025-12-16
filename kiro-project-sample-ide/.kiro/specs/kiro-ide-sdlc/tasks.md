# Kiro IDE SDLC Replication - Tasks

## Group 1: Project Foundation

### 1.1 Create directory structure
**Status:** [ ] Pending
**Description:** Create the complete project directory structure for the Kiro SDLC sample project.
**Files:** All directories under `kiro-project-sample-ide/`

### 1.2 Create pyproject.toml
**Status:** [ ] Pending
**Description:** Configure Python project with pytest, ruff, mypy, bandit settings.
**Files:** `pyproject.toml`

### 1.3 Create requirements files
**Status:** [ ] Pending
**Description:** Create production and development dependency files.
**Files:** `requirements.txt`, `requirements-dev.txt`

### 1.4 Configure MCP servers
**Status:** [ ] Pending
**Description:** Set up MCP server configuration for docs, context7, and spec-workflow.
**Files:** `.kiro/settings/mcp.json`

---

## Group 2: Core Steering Documents

### 2.1 Create product.md
**Status:** [ ] Pending
**Description:** Define product vision, SDLC workflow, and quality gates.
**Files:** `.kiro/steering/product.md`

### 2.2 Create tech.md
**Status:** [ ] Pending
**Description:** Document Python 3.11+ stack with pytest, ruff, mypy, bandit.
**Files:** `.kiro/steering/tech.md`

### 2.3 Create structure.md
**Status:** [ ] Pending
**Description:** Document directory layout and naming conventions.
**Files:** `.kiro/steering/structure.md`

### 2.4 Create tdd-workflow.md
**Status:** [ ] Pending
**Description:** Document RED-GREEN-REFACTOR cycle for Python/pytest.
**Files:** `.kiro/steering/tdd-workflow.md`

---

## Group 3: Phase Steering Documents

### 3.1 Create 01-spec.md
**Status:** [ ] Pending
**Description:** SPEC phase instructions (requirements gathering, design, task breakdown).
**Files:** `.kiro/steering/phases/01-spec.md`
**Maps to:** Claude Code `spec-writer.md` plugin

### 3.2 Create 02-test.md
**Status:** [ ] Pending
**Description:** TEST phase instructions (TDD, pytest patterns, fixture creation).
**Files:** `.kiro/steering/phases/02-test.md`
**Maps to:** Claude Code `test-writer.md` + `test-engineer` agent

### 3.3 Create 03-code.md
**Status:** [ ] Pending
**Description:** CODE phase instructions (minimal implementation, layer-by-layer).
**Files:** `.kiro/steering/phases/03-code.md`
**Maps to:** Claude Code `code-implementer.md` + `implementation-agent`

### 3.4 Create 04-build.md
**Status:** [ ] Pending
**Description:** BUILD phase instructions (lint, type check, coverage).
**Files:** `.kiro/steering/phases/04-build.md`
**Maps to:** Claude Code `builder.md` plugin

### 3.5 Create 05-quality-gate.md
**Status:** [ ] Pending
**Description:** QUALITY GATE phase (security scan + code review combined).
**Files:** `.kiro/steering/phases/05-quality-gate.md`
**Maps to:** Claude Code `security-checker.md` + `code-reviewer` skill

### 3.6 Create 06-docs.md
**Status:** [ ] Pending
**Description:** DOCS phase instructions (API docs, CHANGELOG, README).
**Files:** `.kiro/steering/phases/06-docs.md`
**Maps to:** Claude Code `docs-generator.md` + `documentation-generator` agent

---

## Group 4: Hook Configuration

### 4.1 Configure Lint on Save hook
**Status:** [ ] Pending
**Description:** Set up hook to run `ruff check` on Python file save.
**Trigger:** File Save
**Pattern:** `**/*.py`

### 4.2 Configure Security Scan hook
**Status:** [ ] Pending
**Description:** Set up hook to run `bandit` on source file save.
**Trigger:** File Save
**Pattern:** `src/**/*.py`

### 4.3 Configure TDD Reminder hook
**Status:** [ ] Pending
**Description:** Set up hook to remind about TDD on new source file creation.
**Trigger:** File Create
**Pattern:** `src/**/*.py`

### 4.4 Configure Code Review hook
**Status:** [ ] Pending
**Description:** Set up manual hook for code review checklist.
**Trigger:** Manual

### 4.5 Document hooks
**Status:** [ ] Pending
**Description:** Create hook documentation in README.
**Files:** `.kiro/hooks/README.md`

---

## Group 5: Sample TDD Implementation

### 5.1 Write User model tests
**Status:** [ ] Pending
**Description:** Create failing tests for User dataclass.
**Files:** `tests/unit/test_user.py`

### 5.2 Write UserService tests
**Status:** [ ] Pending
**Description:** Create failing tests for UserService methods.
**Files:** `tests/unit/test_user_service.py`

### 5.3 Write API integration tests
**Status:** [ ] Pending
**Description:** Create failing tests for API endpoints.
**Files:** `tests/integration/test_api.py`

### 5.4 Create test fixtures
**Status:** [ ] Pending
**Description:** Create shared test fixtures for users.
**Files:** `tests/fixtures/user_fixtures.py`

### 5.5 Implement User model
**Status:** [ ] Pending
**Description:** Create User and CreateUserRequest dataclasses.
**Files:** `src/models/user.py`

### 5.6 Implement UserService
**Status:** [ ] Pending
**Description:** Create UserService with CRUD operations.
**Files:** `src/services/user_service.py`

### 5.7 Implement API endpoints
**Status:** [ ] Pending
**Description:** Create API functions using UserService.
**Files:** `src/api/sample_api.py`

### 5.8 Verify 80%+ coverage
**Status:** [ ] Pending
**Description:** Run pytest with coverage and verify threshold met.
**Command:** `pytest --cov=src --cov-fail-under=80`

---

## Group 6: Documentation

### 6.1 Generate API documentation
**Status:** [ ] Pending
**Description:** Create API documentation for all endpoints.
**Files:** `docs/api.md`

### 6.2 Create CHANGELOG
**Status:** [ ] Pending
**Description:** Create CHANGELOG with initial version.
**Files:** `CHANGELOG.md`

### 6.3 Create README
**Status:** [ ] Pending
**Description:** Create project README with setup and usage instructions.
**Files:** `README.md`

---

## Progress Summary

| Group | Tasks | Completed |
|-------|-------|-----------|
| 1. Project Foundation | 4 | 0 |
| 2. Core Steering | 4 | 0 |
| 3. Phase Steering | 6 | 0 |
| 4. Hook Configuration | 5 | 0 |
| 5. TDD Implementation | 8 | 0 |
| 6. Documentation | 3 | 0 |
| **Total** | **30** | **0** |
