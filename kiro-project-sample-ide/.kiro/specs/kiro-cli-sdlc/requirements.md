# Kiro CLI SDLC Replication - Requirements

## Overview

Replicate the Claude Code 5-phase SDLC workflow in Kiro CLI with support for both interactive and headless modes. Integrates with the `spec-workflow` MCP server for structured specification management with approval workflows.

## User Stories

### REQ-CLI-001: Interactive Mode (Default)

**EARS Syntax:** WHEN the user runs `kiro sdlc` without flags, THE SYSTEM SHALL prompt for feature name, phase selection, and guide interactively through each phase.

**User Story:** As a developer, I want interactive prompts when running the SDLC workflow so that I'm guided through each step with confirmations.

**Acceptance Criteria:**
- [ ] User prompted for feature/spec name
- [ ] User prompted for starting phase (1-6)
- [ ] Progress displayed in terminal with clear formatting
- [ ] Confirmation required before each phase transition
- [ ] Can exit and resume later

---

### REQ-CLI-002: Headless Mode

**EARS Syntax:** WHEN the user runs `kiro sdlc --headless --spec <name>`, THE SYSTEM SHALL execute all phases sequentially without prompts, using exit codes to indicate success/failure.

**User Story:** As a CI/CD system or automation script, I want headless execution so that SDLC workflows can run in batch/automated pipelines.

**Acceptance Criteria:**
- [ ] All configuration passed via command-line flags
- [ ] Output suitable for log parsing (structured, timestamped)
- [ ] Exit codes indicate phase-specific success/failure
- [ ] No interactive prompts or confirmations
- [ ] Supports timeout configuration

---

### REQ-CLI-003: Phase Selection

**EARS Syntax:** WHEN the user provides `--phase <number>` flag, THE SYSTEM SHALL validate prerequisites and start from that specific phase.

**User Story:** As a developer, I want to resume from a specific phase so that I can continue interrupted work without re-running completed phases.

**Acceptance Criteria:**
- [ ] `--phase 1` through `--phase 6` supported
- [ ] Phase prerequisites validated before execution
- [ ] Error with clear message if prerequisites not met
- [ ] Works in both interactive and headless modes

---

### REQ-CLI-004: Spec-Workflow MCP Integration

**EARS Syntax:** WHEN the user runs the SDLC workflow, THE SYSTEM SHALL use the spec-workflow MCP server to manage specifications, track progress, and handle approvals.

**User Story:** As a developer, I want structured spec management so that requirements, designs, and tasks are versioned and have approval workflows.

**Acceptance Criteria:**
- [ ] Spec creation uses `spec-workflow-guide` tool
- [ ] Spec status tracked via `spec-status` tool
- [ ] Approvals managed via `approvals` tool
- [ ] Implementation logged via `log-implementation` tool
- [ ] Steering documents created via `steering-guide` tool

---

### REQ-CLI-005: Dry Run Mode

**EARS Syntax:** WHEN the user provides `--dry-run` flag, THE SYSTEM SHALL display what would happen at each phase without executing any changes.

**User Story:** As a developer, I want to preview the workflow so that I understand what will happen before committing to execution.

**Acceptance Criteria:**
- [ ] All actions logged without execution
- [ ] File paths that would be created/modified shown
- [ ] Commands that would run displayed
- [ ] No files written, no tests run, no commits made

---

### REQ-CLI-006: Verbose Output

**EARS Syntax:** WHEN the user provides `--verbose` or `-v` flag, THE SYSTEM SHALL display detailed progress information including timestamps and command outputs.

**User Story:** As a developer debugging issues, I want detailed output so that I can understand exactly what's happening.

**Acceptance Criteria:**
- [ ] Each step logged with timestamp
- [ ] File operations detailed
- [ ] Command outputs included (not just exit codes)
- [ ] Stack traces shown on errors

---

### REQ-CLI-007: Configuration File Support

**EARS Syntax:** WHEN a `.kiro/cli-config.json` file exists, THE SYSTEM SHALL use it for default values and project-specific settings.

**User Story:** As a team lead, I want to configure default settings for the project so that all developers use consistent SDLC parameters.

**Acceptance Criteria:**
- [ ] Default phase, spec name prefix, timeouts configurable
- [ ] Quality thresholds configurable (coverage %, lint rules)
- [ ] Command-line flags override config file settings
- [ ] Config validated on load with clear error messages

---

## Non-Functional Requirements

### NFR-CLI-001: Exit Codes

**Requirement:** CLI uses consistent exit codes for automation integration.

| Code | Meaning |
|------|---------|
| 0 | Success - all phases completed |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Prerequisites not met |
| 4 | Phase failed (lint, test, etc.) |
| 5 | Quality gate failed (security, coverage) |
| 6 | MCP server communication error |

---

### NFR-CLI-002: Output Formats

**Requirement:** Support multiple output formats for different use cases.

| Format | Flag | Use Case |
|--------|------|----------|
| Human | (default) | Interactive terminal |
| JSON | `--output json` | Automation, parsing |
| Quiet | `--quiet` | Only errors, minimal output |

---

### NFR-CLI-003: Spec-Workflow MCP Tools

**Requirement:** CLI leverages spec-workflow MCP server tools for structured workflow.

| Tool | Purpose | CLI Usage |
|------|---------|-----------|
| `spec-workflow-guide` | Load workflow instructions | Phase 1 (SPEC) |
| `steering-guide` | Create steering documents | Initial setup |
| `spec-status` | Check spec progress | Resume, status checks |
| `approvals` | Request/check approvals | Phase transitions |
| `log-implementation` | Record implementation details | After each task |

---

## Dependencies

- Kiro CLI with MCP support
- `spec-workflow` MCP server (`@pimzino/spec-workflow-mcp`)
- Python 3.11+ with dev dependencies
- Same tooling as IDE: pytest, ruff, mypy, bandit
