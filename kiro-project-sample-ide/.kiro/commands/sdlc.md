---
name: sdlc
description: IDE-driven SDLC workflow - spec, test, code, build (hooks), quality gate, docs
---

# SDLC Orchestrator (IDE Reference Implementation)

You are orchestrating a complete Software Development Lifecycle workflow using the IDE-friendly approach with Makefile and hooks.

## SDLC Phases (IDE Approach)

```
┌─────────┬─────────┬─────────┬─────────┬──────────────┬─────────┐
│ 1.SPEC  │ 2.TEST  │ 3.CODE  │ 4.BUILD │ 5.QUALITY    │ 6.DOCS  │
│ (Chat)  │ (Chat)  │ (Chat)  │ (Hook + │   GATE       │ (Chat)  │
│         │         │         │  Make)  │ (Hook+Make)  │         │
└─────────┴─────────┴─────────┴─────────┴──────────────┴─────────┘
```

## Workflow Execution

### Phase 1: Specification (Chat-Driven)

**Goal**: Define requirements and design through conversation.

Work interactively to create:
- Requirements document
- Technical design
- Task breakdown
- API contracts

**Steering**: Reference `.kiro/steering/phases/01-spec.md`

**Artifacts**: `.kiro/specs/{spec-name}/requirements.md`, `design.md`, `tasks.md`

---

### Phase 2: Testing (TDD)

**Goal**: Write failing tests BEFORE implementation.

1. Create test files following the design
2. Write tests for all success and error scenarios
3. Run tests to verify they fail (Red phase)

**Steering**: Reference `.kiro/steering/phases/02-test.md`

**Commands**:
```bash
make test
# or
pytest tests/unit/test_{feature}.py
```

**Artifacts**: Test files in `tests/unit/`, `tests/integration/`

---

### Phase 3: Implementation

**Goal**: Write minimal code to make tests pass (Green phase).

1. Implement data models
2. Implement business logic
3. Make all tests pass
4. Refactor while keeping tests green

**IDE Hooks**: Lint-on-save runs automatically

**Steering**: Reference `.kiro/steering/phases/03-code.md`

**Artifacts**: Source files in `src/`

---

### Phase 4: Build Verification (Makefile + Hooks)

**Goal**: Ensure code quality through automated checks.

Run the build target:
```bash
make build
```

This executes:
1. **Lint** - `ruff check src/ tests/`
2. **Type Check** - `mypy src/`
3. **Tests** - `pytest --cov=src --cov-fail-under=80`

**IDE Hooks**:
- Lint runs on file save (`.py` files)
- Security scan runs on save (`src/**/*.py`)

**Steering**: Reference `.kiro/steering/phases/04-build.md`

**Quality Gates**:
- 0 lint errors
- 0 type errors
- 80%+ test coverage

---

### Phase 5: Quality Gate (Makefile + Hooks)

**Goal**: Security verification and comprehensive checks.

Run the quality gate target:
```bash
make quality-gate
```

This executes:
1. **Security Scan** - `bandit -r src/`
2. **Coverage Report** - Full coverage analysis
3. **Dependency Check** - `safety check`

**IDE Hooks**: Security scan runs automatically on save

**Steering**: Reference `.kiro/steering/phases/05-quality-gate.md`

**Quality Gates**:
- 0 critical/high vulnerabilities
- 80%+ test coverage
- No known vulnerable dependencies

---

### Phase 6: Documentation

**Goal**: Generate comprehensive documentation.

1. Document all new APIs and functions
2. Update CHANGELOG.md with your changes
3. Add/update CLAUDE.md files in modified directories
4. Generate API documentation

**Steering**: Reference `.kiro/steering/phases/06-docs.md`

**Artifacts**: `docs/api.md`, `CHANGELOG.md`, `CLAUDE.md` files

---

## Orchestration Flow

When user invokes `/sdlc`:

1. **Ask which phase to start from** (or start fresh)
2. **Execute phases sequentially**:
   - Phase 1: Chat-driven spec creation
   - Phase 2: Write failing tests
   - Phase 3: Implement to pass tests (hooks auto-lint)
   - Phase 4: Run `make build` (or hooks auto-check)
   - Phase 5: Run `make quality-gate`
   - Phase 6: Generate documentation
3. **Create PR** (optional)

## Phase Transitions

```
SPEC ──[complete]──> TEST ──[written]──> CODE ──[green]──> BUILD
                                          ↑                   │
                                          │                   ▼
                                     (Hooks auto-lint)  QUALITY GATE
                                                             │
                                                             ▼
                                         DOCS <────────[passed]
                                           │
                                           ▼
                                       CREATE PR
```

## Ad-Hoc Invocation

Users can invoke individual phases:
- "Run the spec phase" → Guide spec creation
- "Write tests" → Guide TDD test writing
- "Implement feature" → Guide implementation
- "Run build" → Execute `make build`
- "Run quality gate" → Execute `make quality-gate`
- "Generate docs" → Update documentation

## Makefile Targets

Available make commands:
```bash
make help           # Show all available commands
make dev-install    # Install development dependencies
make lint           # Run ruff linter
make lint-fix       # Run ruff with auto-fix
make type-check     # Run mypy type checker
make test           # Run pytest
make coverage       # Run pytest with coverage report
make security       # Run bandit security scan
make build          # Run lint + type check + tests
make quality-gate   # Run security scan + coverage
make all            # Run complete SDLC build pipeline
make clean          # Remove build artifacts
```

## Status Tracking

Use TodoWrite to track progress:

```
[ ] Phase 1: Specification
[ ] Phase 2: Testing (TDD)
[ ] Phase 3: Implementation
[ ] Phase 4: Build Verification (make build)
[ ] Phase 5: Quality Gate (make quality-gate)
[ ] Phase 6: Documentation
[ ] Create PR (optional)
```

## IDE-Specific Features

This implementation emphasizes:
- **Makefile convenience** for common tasks
- **Hook automation** for continuous quality checks
- **Interactive development** with instant feedback
- **IDE panel integration** for problems and terminal output

## Example: User Management API

This reference implementation includes a complete example:
- **Models**: `src/models/user.py` (User, CreateUserRequest)
- **Services**: `src/services/user_service.py` (UserService with validation)
- **API**: `src/api/sample_api.py` (get_users, create_user, etc.)
- **Tests**: 45+ tests with 100% coverage

Study these files to learn the patterns and best practices.

## Begin Workflow

Ask the user:
1. What feature are we building?
2. Which phase should we begin with?
3. Should we reference the existing user management example?

Then guide them through the phases, using Makefile for automation and hooks for continuous checks.
