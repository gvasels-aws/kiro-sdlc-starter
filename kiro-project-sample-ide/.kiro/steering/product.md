---
inclusion: always
---

# Product: Kiro SDLC Reference Implementation

## Overview

This is a **complete reference implementation** with working code demonstrating the full Software Development Lifecycle (SDLC) workflow in Kiro IDE/CLI. Use this to learn from a real example of TDD-based Python development.

**Note**: This is a complete implementation with a working user management API and comprehensive tests. For a minimal starter template, see the kiro-project-sample-cli sibling project.

## SDLC Workflow

This project follows a **6-phase SDLC workflow**:

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────────┐   ┌─────────┐
│ 1.SPEC  │──►│ 2.TEST  │──►│ 3.CODE  │──►│ 4.BUILD │──►│ 5.QUALITY   │──►│ 6.DOCS  │
│ (Chat)  │   │ (Chat)  │   │ (Chat)  │   │ (Hook)  │   │   GATE      │   │ (Chat)  │
│         │   │         │   │         │   │         │   │ (Hook+Chat) │   │         │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────────┘   └─────────┘
```

### Phase Descriptions

| Phase | Name | Mode | Description |
|-------|------|------|-------------|
| 1 | **SPEC** | Chat-driven | Define requirements, design, and tasks |
| 2 | **TEST** | Chat-driven | Write failing tests first (TDD Red phase) |
| 3 | **CODE** | Chat-driven | Implement minimal code to pass tests (Green phase) |
| 4 | **BUILD** | Hook-assisted | Lint, type check, run tests with coverage |
| 5 | **QUALITY GATE** | Hook + Chat | Security scan + code review |
| 6 | **DOCS** | Chat-driven | Generate API docs, update CHANGELOG |

### Phase Transitions

- **SPEC → TEST**: Spec approved, requirements and design complete
- **TEST → CODE**: Failing tests written, test structure established
- **CODE → BUILD**: All tests passing (Green phase achieved)
- **BUILD → QUALITY GATE**: Lint, type check, 80%+ coverage achieved
- **QUALITY GATE → DOCS**: 0 critical/high vulnerabilities, code review passed
- **DOCS → Complete**: Documentation generated, CHANGELOG updated

## Automation Strategy

### Hooks (Automated Quality Gates)

| Hook | Trigger | Purpose |
|------|---------|---------|
| Lint on Save | File Save (`**/*.py`) | Run `ruff check` automatically |
| Security Scan | File Save (`src/**/*.py`) | Run `bandit` for security issues |
| TDD Reminder | File Create (`src/**/*.py`) | Remind to write tests first |
| Code Review | Manual trigger | Run code review checklist |

### Chat-Driven Phases

Major phases (SPEC, TEST, CODE, DOCS) are driven through Kiro's agentic chat:
- Reference `#codebase` for full project context
- Reference `#terminal` for command outputs
- Reference `#problems` for current issues

## Quality Gates

| Gate | Requirement |
|------|-------------|
| Lint | 0 errors (ruff) |
| Type Check | 0 errors (mypy) |
| Test Coverage | 80%+ (pytest-cov) |
| Security | 0 critical/high vulnerabilities (bandit) |
| Code Review | Passed checklist |
| Documentation | CHANGELOG.md updated |

## Target Users

- Developers learning TDD practices (learn from working example)
- Teams adopting structured SDLC workflows
- Developers wanting to see a complete implementation before starting
- Teams evaluating Kiro for their projects

## Difference from kiro-project-sample-cli

| Aspect | kiro-project-sample-ide (this) | kiro-cli-template |
|--------|--------------------------------|-------------------|
| Purpose | Complete reference implementation | Minimal template/starter |
| Source code | Full user management API | Empty stubs |
| Tests | 45+ comprehensive tests | Empty stubs |
| Automation | Makefile + inline commands | Shell scripts |
| Use case | Learn from working example | Start new projects |
