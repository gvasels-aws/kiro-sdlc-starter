# Kiro CLI SDLC Replication - Tasks

## Group 1: CLI Infrastructure

### 1.1 Design CLI argument parser
**Status:** [ ] Pending
**Description:** Design command structure with argparse/click for SDLC workflow.
**Components:**
- Main `sdlc` command
- Subcommands: `status`, `resume`
- Flags: `--interactive`, `--headless`, `--spec`, `--phase`, `--dry-run`, `--verbose`, `--output`

### 1.2 Implement mode handler
**Status:** [ ] Pending
**Description:** Create mode handler that switches between interactive and headless execution.
**Files:** `cli/mode_handler.py`

### 1.3 Implement phase executor framework
**Status:** [ ] Pending
**Description:** Create base executor with phase registration and prerequisite checking.
**Files:** `cli/phase_executor.py`

### 1.4 Implement configuration loader
**Status:** [ ] Pending
**Description:** Load and validate `.kiro/cli-config.json` with defaults.
**Files:** `cli/config.py`

---

## Group 2: Spec-Workflow MCP Integration

### 2.1 Implement MCP client wrapper
**Status:** [ ] Pending
**Description:** Create wrapper for spec-workflow MCP server communication.
**Files:** `cli/mcp_client.py`
**MCP Tools:**
- `spec-workflow-guide`
- `steering-guide`
- `spec-status`
- `approvals`
- `log-implementation`

### 2.2 Integrate spec-workflow-guide
**Status:** [ ] Pending
**Description:** Load and apply workflow guide during SPEC phase.
**Usage:** Phase 1 initialization

### 2.3 Integrate spec-status
**Status:** [ ] Pending
**Description:** Check and display spec progress for status command.
**Usage:** `kiro sdlc status`, resume functionality

### 2.4 Integrate approvals
**Status:** [ ] Pending
**Description:** Request and check approvals at phase transitions.
**Usage:** Phase transitions, interactive confirmations

### 2.5 Integrate log-implementation
**Status:** [ ] Pending
**Description:** Record implementation details after task completion.
**Usage:** After phases 3-6 complete

---

## Group 3: Interactive Mode

### 3.1 Implement prompt system
**Status:** [ ] Pending
**Description:** Create interactive prompts for phase transitions and inputs.
**Features:**
- Spec name input
- Phase selection
- Confirmation dialogs
- Error recovery options

### 3.2 Implement progress display
**Status:** [ ] Pending
**Description:** Show progress spinners and status updates during execution.
**Features:**
- Phase progress bars
- Step completion indicators
- Time elapsed

### 3.3 Implement confirmation dialogs
**Status:** [ ] Pending
**Description:** Add confirmation prompts before phase transitions.
**Features:**
- Y/n prompts
- Multi-choice menus
- Skip/retry options

### 3.4 Test interactive workflow
**Status:** [ ] Pending
**Description:** End-to-end test of interactive mode through all 6 phases.
**Verification:** Manual testing with various inputs

---

## Group 4: Headless Mode

### 4.1 Implement non-interactive execution
**Status:** [ ] Pending
**Description:** Execute phases without prompts, using flags for all inputs.
**Features:**
- All config via flags
- No stdin required
- Automatic phase progression

### 4.2 Implement log-friendly output
**Status:** [ ] Pending
**Description:** Structured output with timestamps for log parsing.
**Formats:**
- Human readable (default)
- JSON (`--output json`)
- Quiet (`--quiet`)

### 4.3 Implement exit code handling
**Status:** [ ] Pending
**Description:** Return appropriate exit codes for different failure modes.
**Exit Codes:**
- 0: Success
- 1: General error
- 2: Invalid arguments
- 3: Prerequisites not met
- 4: Phase failed
- 5: Quality gate failed
- 6: MCP error

### 4.4 Test headless workflow
**Status:** [ ] Pending
**Description:** End-to-end test of headless mode with various flag combinations.
**Verification:** Automated test suite

---

## Group 5: Phase Implementations

### 5.1 Implement SPEC phase
**Status:** [ ] Pending
**Description:** Create spec files using spec-workflow MCP.
**Steps:**
1. Load workflow guide
2. Create requirements.md
3. Create design.md
4. Create tasks.md
5. Request approval

### 5.2 Implement TEST phase
**Status:** [ ] Pending
**Description:** Generate test files and verify they fail (RED phase).
**Steps:**
1. Read design.md for contracts
2. Generate test files
3. Run tests to verify failure
4. Report RED phase achieved

### 5.3 Implement CODE phase
**Status:** [ ] Pending
**Description:** Guide implementation to pass tests (GREEN phase).
**Steps:**
1. Read failing tests
2. Implement models
3. Implement services
4. Implement API
5. Verify tests pass

### 5.4 Implement BUILD phase
**Status:** [ ] Pending
**Description:** Run quality checks (lint, type, coverage).
**Steps:**
1. Run `ruff check`
2. Run `mypy`
3. Run `pytest --cov`
4. Report results

### 5.5 Implement QUALITY GATE phase
**Status:** [ ] Pending
**Description:** Run security scans and code review.
**Steps:**
1. Run `bandit`
2. Run `safety check`
3. Trigger code review (interactive) or auto-pass (headless)
4. Report findings

### 5.6 Implement DOCS phase
**Status:** [ ] Pending
**Description:** Generate documentation and update changelog.
**Steps:**
1. Generate API docs
2. Update CHANGELOG.md
3. Update README.md
4. Log implementation

---

## Group 6: Testing & Documentation

### 6.1 Write unit tests for CLI
**Status:** [ ] Pending
**Description:** Unit tests for CLI components (parser, executor, config).
**Files:** `tests/unit/test_cli_*.py`

### 6.2 Write integration tests
**Status:** [ ] Pending
**Description:** Integration tests for full workflows (interactive, headless).
**Files:** `tests/integration/test_cli_workflow.py`

### 6.3 Document CLI usage
**Status:** [ ] Pending
**Description:** Create CLI documentation with examples.
**Files:** `docs/cli.md`

### 6.4 Create help content
**Status:** [ ] Pending
**Description:** Detailed --help content for all commands and flags.
**Features:**
- Command descriptions
- Flag explanations
- Usage examples

---

## Progress Summary

| Group | Tasks | Completed |
|-------|-------|-----------|
| 1. CLI Infrastructure | 4 | 0 |
| 2. MCP Integration | 5 | 0 |
| 3. Interactive Mode | 4 | 0 |
| 4. Headless Mode | 4 | 0 |
| 5. Phase Implementations | 6 | 0 |
| 6. Testing & Documentation | 4 | 0 |
| **Total** | **27** | **0** |

---

## Dependency Graph

```
Group 1 (Infrastructure)
    │
    ├──► Group 2 (MCP Integration)
    │        │
    │        └──► Group 5 (Phase Implementations)
    │                     │
    │                     ├──► Group 3 (Interactive Mode)
    │                     │
    │                     └──► Group 4 (Headless Mode)
    │
    └──────────────────────────► Group 6 (Testing & Docs)
```

**Execution Order:**
1. Group 1: CLI Infrastructure (foundation)
2. Group 2: MCP Integration (spec-workflow tools)
3. Group 5: Phase Implementations (core logic)
4. Group 3 & 4: Modes (parallel, depends on phases)
5. Group 6: Testing & Docs (final)
