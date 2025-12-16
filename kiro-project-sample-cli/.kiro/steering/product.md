---
inclusion: always
---

# Product: Kiro CLI SDLC Sample Project

## Overview

This project demonstrates a complete Software Development Lifecycle (SDLC) workflow implemented using Claude Code CLI with the spec-workflow MCP server. It serves as both a reference implementation and a template for TDD-based Python development in headless/interactive CLI environments.

## SDLC Workflow

This project follows a **6-phase SDLC workflow** orchestrated via shell scripts and spec-workflow MCP:

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────────┐   ┌─────────┐
│ 1.SPEC  │──►│ 2.TEST  │──►│ 3.CODE  │──►│ 4.BUILD │──►│ 5.QUALITY   │──►│ 6.DOCS  │
│ (MCP)   │   │ (CLI)   │   │ (CLI)   │   │(Script) │   │   GATE      │   │ (CLI)   │
│         │   │         │   │         │   │         │   │   (Script)  │   │         │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────────┘   └─────────┘
```

### Phase Descriptions

| Phase | Name | Mode | Description |
|-------|------|------|-------------|
| 1 | **SPEC** | MCP-driven | Define requirements, design, tasks via spec-workflow |
| 2 | **TEST** | CLI-driven | Write failing tests first (TDD Red phase) |
| 3 | **CODE** | CLI-driven | Implement minimal code to pass tests (Green phase) |
| 4 | **BUILD** | Script-assisted | Lint, type check, run tests with coverage |
| 5 | **QUALITY GATE** | Script-assisted | Security scan + code review |
| 6 | **DOCS** | CLI-driven | Generate API docs, update CHANGELOG |

### Phase Transitions

- **SPEC → TEST**: Spec approved, requirements and design complete
- **TEST → CODE**: Failing tests written, test structure established
- **CODE → BUILD**: All tests passing (Green phase achieved)
- **BUILD → QUALITY GATE**: Lint, type check, 80%+ coverage achieved
- **QUALITY GATE → DOCS**: 0 critical/high vulnerabilities, code review passed
- **DOCS → Complete**: Documentation generated, CHANGELOG updated

## Automation Strategy

### Shell Scripts (Headless Quality Gates)

| Script | Purpose | Phase |
|--------|---------|-------|
| `scripts/lint.sh` | Run ruff check on all Python files | BUILD |
| `scripts/type-check.sh` | Run mypy type checking | BUILD |
| `scripts/test.sh` | Run pytest with coverage reporting | BUILD |
| `scripts/security-scan.sh` | Run bandit security analysis | QUALITY GATE |
| `scripts/build.sh` | Full build pipeline (lint + types + tests) | BUILD |
| `scripts/quality-gate.sh` | Security + dependencies check | QUALITY GATE |

### Spec-Workflow MCP Integration

The spec-workflow MCP server orchestrates the entire SDLC:

```bash
# Start a new spec
claude mcp spec-workflow spec-workflow-guide

# Create requirements
claude mcp spec-workflow create-requirements

# Create design from requirements
claude mcp spec-workflow create-design

# Create task breakdown
claude mcp spec-workflow create-tasks

# Check spec status
claude mcp spec-workflow spec-status --specName=<name>

# Request approval for documents
claude mcp spec-workflow approvals --action=request

# Log implementation progress
claude mcp spec-workflow log-implementation
```

### CLI Execution Modes

**Interactive Mode:**
```bash
# Start conversation with spec context
claude --project /path/to/kiro-project-sample-cli

# Reference spec files during conversation
> "Let's implement task 2.1 from the spec"
```

**Headless Mode:**
```bash
# Run automated build checks
./scripts/build.sh

# Run quality gates
./scripts/quality-gate.sh

# Generate documentation
claude --prompt "Generate API documentation for src/api/"
```

## Quality Gates

| Gate | Requirement | Script |
|------|-------------|--------|
| Lint | 0 errors (ruff) | `scripts/lint.sh` |
| Type Check | 0 errors (mypy) | `scripts/type-check.sh` |
| Test Coverage | 80%+ (pytest-cov) | `scripts/test.sh` |
| Security | 0 critical/high vulnerabilities (bandit) | `scripts/security-scan.sh` |
| Dependencies | No known vulnerabilities (safety) | `scripts/quality-gate.sh` |
| Documentation | CHANGELOG.md updated | Manual/CLI |

## Target Users

- Developers using Claude Code CLI for TDD
- Teams adopting spec-workflow for structured SDLC
- CI/CD pipelines requiring headless quality checks
- Developers migrating from IDE workflows to CLI automation
