# Kiro IDE SDLC Replication - Design

## Architecture Overview

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                              KIRO IDE                                          │
├───────────────────────────────────────────────────────────────────────────────┤
│                          STEERING DOCUMENTS                                    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐  │
│  │ product.md   │ │ tech.md      │ │ structure.md │ │ phases/*.md          │  │
│  │ (always)     │ │ (always)     │ │ (always)     │ │ (manual reference)   │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────────────┘  │
├───────────────────────────────────────────────────────────────────────────────┤
│                               HOOKS                                            │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐ │
│  │ Lint on Save    │ │ Security Scan   │ │ TDD Reminder    │ │ Code Review  │ │
│  │ (File Save)     │ │ (File Save)     │ │ (File Create)   │ │ (Manual)     │ │
│  │ **/*.py         │ │ src/**/*.py     │ │ src/**/*.py     │ │              │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ └──────────────┘ │
├───────────────────────────────────────────────────────────────────────────────┤
│                          SPECS (Per Feature)                                   │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │ .kiro/specs/{feature}/                                                   │  │
│  │ ├── requirements.md    (EARS syntax, user stories)                       │  │
│  │ ├── design.md          (data models, API contracts, architecture)        │  │
│  │ └── tasks.md           (implementation checklist, grouped by dependency) │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
├───────────────────────────────────────────────────────────────────────────────┤
│                            MCP SERVERS                                         │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐                  │
│  │ docs-mcp-server │ │ context7        │ │ spec-workflow   │                  │
│  │ (documentation) │ │ (library docs)  │ │ (spec mgmt)     │                  │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘                  │
├───────────────────────────────────────────────────────────────────────────────┤
│                           AGENTIC CHAT                                         │
│  Context Providers: #codebase  #terminal  #problems  #mcp                      │
│  Phase Execution: Chat-driven for SPEC, TEST, CODE, DOCS                       │
│                   Hook-assisted for BUILD, QUALITY GATE                        │
└───────────────────────────────────────────────────────────────────────────────┘
```

## Phase Flow Diagram

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────────┐     ┌─────────┐
│ 1.SPEC  │────►│ 2.TEST  │────►│ 3.CODE  │────►│ 4.BUILD │────►│ 5.QUALITY   │────►│ 6.DOCS  │
│         │     │         │     │         │     │         │     │   GATE      │     │         │
│ Chat    │     │ Chat    │     │ Chat    │     │ Hook    │     │ Hook+Chat   │     │ Chat    │
└────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘     └──────┬──────┘     └────┬────┘
     │               │               │               │                  │                 │
     ▼               ▼               ▼               ▼                  ▼                 ▼
requirements.md  test_*.py      src/*.py        Lint pass       Security pass      docs/api.md
design.md        fixtures       models          Type pass       Review pass        CHANGELOG.md
tasks.md                        services        Coverage 80%+   0 critical vuln    README.md
```

## Component Mapping

### Claude Code → Kiro IDE Mapping

| Claude Code Component | Kiro IDE Equivalent | Location |
|----------------------|---------------------|----------|
| `.claude/plugins/spec-writer.md` | Steering document | `.kiro/steering/phases/01-spec.md` |
| `.claude/plugins/test-writer.md` | Steering document | `.kiro/steering/phases/02-test.md` |
| `.claude/agents/test-engineer` | Embedded in steering | `.kiro/steering/phases/02-test.md` |
| `.claude/plugins/code-implementer.md` | Steering document | `.kiro/steering/phases/03-code.md` |
| `.claude/agents/implementation-agent` | Embedded in steering | `.kiro/steering/phases/03-code.md` |
| `.claude/plugins/builder.md` | Steering + Hook | `.kiro/steering/phases/04-build.md` |
| `.claude/plugins/security-checker.md` | Steering + Hook | `.kiro/steering/phases/05-quality-gate.md` |
| `.claude/agents/security-auditor` | Embedded in steering | `.kiro/steering/phases/05-quality-gate.md` |
| `.claude/skills/code-reviewer` | Embedded in steering | `.kiro/steering/phases/05-quality-gate.md` |
| `.claude/plugins/docs-generator.md` | Steering document | `.kiro/steering/phases/06-docs.md` |
| `.claude/commands/sdlc.md` | Spec workflow | `.kiro/specs/*/tasks.md` |
| `.claude/docs/tdd-workflow.md` | Steering document | `.kiro/steering/tdd-workflow.md` |
| `.mcp.json` | MCP config | `.kiro/settings/mcp.json` |

## Steering Document Design

### Inclusion Strategy

| Document | Inclusion | Rationale |
|----------|-----------|-----------|
| `product.md` | Always | Core workflow context |
| `tech.md` | Always | Technology constraints |
| `structure.md` | Always | Directory conventions |
| `tdd-workflow.md` | Always | TDD fundamentals |
| `phases/01-spec.md` | Manual | Reference during SPEC phase |
| `phases/02-test.md` | Manual | Reference during TEST phase |
| `phases/03-code.md` | Manual | Reference during CODE phase |
| `phases/04-build.md` | fileMatch: `*.py` | Triggered on Python files |
| `phases/05-quality-gate.md` | Manual | Reference during QG phase |
| `phases/06-docs.md` | Manual | Reference during DOCS phase |

### Document Content Structure

```yaml
# Phase steering document structure
---
inclusion: manual  # or always, or fileMatch: "pattern"
---

# Phase N: Phase Name

## Purpose
[What this phase accomplishes]

## Prerequisites
[What must be complete before this phase]

## Workflow
[Step-by-step instructions]

## Artifacts
[What this phase produces]

## Exit Criteria
[Conditions for moving to next phase]

## Chat Invocation
[How to reference this phase in chat]
```

## Hook Design

### Hook Configuration Table

| Hook | Trigger | Pattern | Action | Tool |
|------|---------|---------|--------|------|
| Lint on Save | File Save | `**/*.py` | Run lint check | `ruff check {file}` |
| Security Scan | File Save | `src/**/*.py` | Run security analysis | `bandit -r {file}` |
| TDD Reminder | File Create | `src/**/*.py` | Show reminder | Chat message |
| Code Review | Manual | - | Run review checklist | Chat-driven |

### Hook Instructions Format

```
[Natural language description]

When {trigger condition}:
1. {Action 1}
2. {Action 2}
3. {Report format}

Expected output:
- {Output 1}
- {Output 2}
```

## MCP Server Configuration

```json
{
  "mcpServers": {
    "docs-mcp-server": {
      "command": "npx",
      "args": ["@arabold/docs-mcp-server@latest"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": { "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}" }
    },
    "spec-workflow": {
      "command": "npx",
      "args": ["-y", "@pimzino/spec-workflow-mcp@latest"],
      "env": {}
    }
  }
}
```

## Quality Gates

### Phase Transitions

| From Phase | To Phase | Gate Criteria |
|------------|----------|---------------|
| 1. SPEC | 2. TEST | requirements.md + design.md + tasks.md complete |
| 2. TEST | 3. CODE | Failing tests written, structure established |
| 3. CODE | 4. BUILD | All tests passing (Green phase) |
| 4. BUILD | 5. QUALITY GATE | Lint 0, Type 0, Coverage 80%+ |
| 5. QUALITY GATE | 6. DOCS | Security 0 critical/high, Review passed |
| 6. DOCS | Complete | API docs + CHANGELOG + README updated |

### Automated Checks

| Check | Command | Threshold |
|-------|---------|-----------|
| Lint | `ruff check src/ tests/` | 0 errors |
| Type | `mypy src/` | 0 errors |
| Tests | `pytest` | 100% pass |
| Coverage | `pytest --cov-fail-under=80` | 80%+ |
| Security | `bandit -r src/` | 0 critical/high |
| Dependencies | `safety check` | 0 vulnerable |

## Data Models

### Spec Structure

```
.kiro/specs/{feature-name}/
├── requirements.md      # EARS syntax requirements
├── design.md           # Technical design
└── tasks.md            # Implementation checklist
```

### Sample Project Structure

```
kiro-project-sample-ide/
├── .kiro/
│   ├── steering/
│   │   ├── product.md
│   │   ├── tech.md
│   │   ├── structure.md
│   │   ├── tdd-workflow.md
│   │   └── phases/
│   ├── specs/
│   ├── settings/
│   │   └── mcp.json
│   └── hooks/
├── src/
│   ├── api/
│   ├── models/
│   └── services/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/
├── pyproject.toml
└── README.md
```
