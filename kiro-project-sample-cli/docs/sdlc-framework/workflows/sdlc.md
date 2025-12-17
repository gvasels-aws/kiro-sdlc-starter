---
name: sdlc
description: CLI-first SDLC workflow - spec, test, code, build, quality gate, docs
---

# SDLC Orchestrator (CLI Template)

You are orchestrating a complete Software Development Lifecycle workflow using the CLI-first approach with shell scripts.

## SDLC Phases (CLI Approach)

```
┌─────────┬─────────┬─────────┬─────────┬──────────────┬─────────┐
│ 1.SPEC  │ 2.TEST  │ 3.CODE  │ 4.BUILD │ 5.QUALITY    │ 6.DOCS  │
│ (MCP)   │ (CLI)   │ (CLI)   │ (Script)│   GATE       │ (CLI)   │
│         │         │         │         │  (Script)    │         │
└─────────┴─────────┴─────────┴─────────┴──────────────┴─────────┘
```

## Workflow Execution

### Phase 1: Specification (spec-workflow MCP)

**Goal**: Define requirements and design before any code.

Use the spec-workflow MCP server:
- Create requirements.md
- Create design.md
- Create tasks.md with implementation breakdown
- Request approval before proceeding

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

**Steering**: Reference `.kiro/steering/phases/03-code.md`

**Artifacts**: Source files in `src/`

---

### Phase 4: Build Verification (Shell Scripts)

**Goal**: Ensure code quality through automated checks.

Run the build script:
```bash
./scripts/build.sh
```

This executes:
1. **Lint** - `./scripts/lint.sh` (ruff check)
2. **Type Check** - `./scripts/type-check.sh` (mypy)
3. **Tests** - `./scripts/test.sh` (pytest with 80%+ coverage)

**Steering**: Reference `.kiro/steering/phases/04-build.md`

**Quality Gates**:
- 0 lint errors
- 0 type errors
- 80%+ test coverage

---

### Phase 5: Quality Gate (Shell Scripts)

**Goal**: Security verification and dependency checking.

Run the quality gate script:
```bash
./scripts/quality-gate.sh
```

This executes:
1. **Security Scan** - `./scripts/security-scan.sh` (bandit)
2. **Dependency Check** - (safety check)

**Steering**: Reference `.kiro/steering/phases/05-quality-gate.md`

**Quality Gates**:
- 0 critical/high vulnerabilities
- No known vulnerable dependencies

---

### Phase 6: Documentation

**Goal**: Generate comprehensive documentation.

1. Document all new APIs and functions
2. Update CHANGELOG.md with your changes
3. Add/update CLAUDE.md files in modified directories

**Steering**: Reference `.kiro/steering/phases/06-docs.md`

**Artifacts**: `CHANGELOG.md`, `CLAUDE.md` files

---

## Orchestration Flow

When user invokes `/sdlc`:

1. **Ask which phase to start from** (or start fresh)
2. **Execute phases sequentially**:
   - Phase 1: spec-workflow MCP → requirements, design, tasks
   - Phase 2: Write failing tests
   - Phase 3: Implement to pass tests
   - Phase 4: Run ./scripts/build.sh
   - Phase 5: Run ./scripts/quality-gate.sh
   - Phase 6: Generate documentation
3. **Create PR** (optional)

## Phase Transitions

```
SPEC ──[approved]──> TEST ──[written]──> CODE ──[green]──> BUILD
                                                              │
                                                              ▼
                                          DOCS <──[passed]── QUALITY GATE
                                            │
                                            ▼
                                        CREATE PR
```

## Ad-Hoc Invocation

Users can invoke individual phases:
- "Run the spec phase" → Start spec-workflow
- "Write tests" → Guide TDD test writing
- "Implement feature" → Guide implementation
- "Run build" → Execute ./scripts/build.sh
- "Run quality gate" → Execute ./scripts/quality-gate.sh
- "Generate docs" → Update documentation

## Status Tracking

Use TodoWrite to track progress:

```
[ ] Phase 1: Specification
[ ] Phase 2: Testing (TDD)
[ ] Phase 3: Implementation
[ ] Phase 4: Build Verification (./scripts/build.sh)
[ ] Phase 5: Quality Gate (./scripts/quality-gate.sh)
[ ] Phase 6: Documentation
[ ] Create PR (optional)
```

## CLI-Specific Features

This template emphasizes:
- **Shell script automation** for build and quality gates
- **Headless execution** capability
- **CI/CD integration** (scripts can run in pipelines)
- **Manual orchestration** via conversation

## Begin Workflow

Ask the user:
1. What feature are we building?
2. Which phase should we begin with?
3. Do you have an existing spec?

Then guide them through the phases, using shell scripts for automation and conversation for guidance.
