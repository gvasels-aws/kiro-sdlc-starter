# Kiro IDE Compliance Documentation

**Last Updated**: 2025-12-16
**Kiro Documentation Reference**: https://kiro.dev/docs/*

## Executive Summary

This project is structured to **clearly separate official Kiro IDE features** from **custom SDLC framework documentation**. This document explains what is processed by Kiro IDE and what is not.

## Official Kiro IDE Features

### ✅ What Kiro IDE Processes

| Directory/File | Purpose | Documentation |
|----------------|---------|---------------|
| `.kiro/steering/` | Persistent AI context loaded into every conversation | [Steering Docs](https://kiro.dev/docs/steering) |
| `.kiro/specs/` | Feature specifications managed by spec-workflow MCP | [Specs via MCP](https://kiro.dev/docs/mcp-servers) |
| `.kiro/settings/mcp.json` | MCP server configuration | [MCP Config](https://kiro.dev/docs/mcp-servers) |
| **Agent Hooks Panel** (UI) | Lifecycle hooks configured via IDE interface | [Hooks](https://kiro.dev/docs/hooks) |

### Steering Documents (`.kiro/steering/`)

**Status**: ✅ Official Kiro IDE Feature

These files are loaded by Kiro IDE as persistent context:

- `product.md` - Product vision and goals
- `tech.md` - Technology stack and decisions
- `structure.md` - Directory structure and conventions
- `sdlc-workflow.md` - SDLC process overview
- `phases/` - Phase-specific guidance (can use YAML front matter for conditional inclusion)

**Key Features**:
- Loaded automatically into every conversation
- Provides consistent AI behavior
- Can be referenced with `#steering:filename` syntax
- Supports YAML front matter for conditional inclusion

### Specs Workflow (`.kiro/specs/`)

**Status**: ✅ Official Kiro IDE Feature (via MCP)

Managed by the `spec-workflow` MCP server configured in `.kiro/settings/mcp.json`.

**What it provides**:
- Requirements → Design → Tasks workflow
- Approval system for documents
- Implementation logging
- Spec status tracking

**Specs in this project**:
- `kiro-ide-sdlc/` - IDE-specific workflow specification
- `kiro-cli-sdlc/` - CLI-specific workflow specification

### MCP Servers (`.kiro/settings/mcp.json`)

**Status**: ✅ Official Kiro IDE Feature

Kiro IDE loads MCP servers defined in this configuration file.

**Available in this project**:
- `docs-mcp-server` - Documentation indexing and search
- `context7` - Library documentation with AI-powered context
- `spec-workflow` - Specification management and SDLC orchestration

**Configuration**:
```json
{
  "mcpServers": {
    "docs-mcp-server": {
      "command": "npx",
      "args": ["-y", "@arabold/docs-mcp-server@latest"]
    },
    "context7": {
      "env": {
        "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}"
      }
    },
    "spec-workflow": {
      "command": "npx",
      "args": ["-y", "@pimzino/spec-workflow-mcp@latest"],
      "env": {
        "PROJECT_PATH": "${workspaceFolder}"
      }
    }
  }
}
```

### Agent Hooks (IDE UI Panel)

**Status**: ✅ Official Kiro IDE Feature

**CRITICAL DIFFERENCE FROM CLI**: Hooks are configured via the **Agent Hooks panel** in the IDE UI, NOT files.

**How it works**:
1. Open Kiro IDE
2. Navigate to Agent Hooks panel
3. Configure hooks with triggers, patterns, and actions
4. Hooks execute automatically based on configured triggers

**Common hook types**:
- Pre-tool hooks (before tool execution)
- Post-tool hooks (after tool execution)
- File save hooks
- File create hooks
- Manual trigger hooks

**Example hooks for this project**:
| Hook | Trigger | Pattern | Purpose |
|------|---------|---------|---------|
| Lint on Save | File Save | `**/*.py` | Run ruff check |
| Security Scan | File Save | `src/**/*.py` | Run bandit |
| TDD Reminder | File Create | `src/**/*.py` | Remind to write tests first |

## Custom SDLC Framework (NOT Official Kiro)

### ❌ What Kiro IDE Does NOT Process

The following directories contain **reference documentation and implementation patterns** for structuring SDLC workflows. They are **not** processed by Kiro IDE as features.

| Directory | Purpose | Status |
|-----------|---------|--------|
| `docs/sdlc-framework/agents/` | AI persona patterns | Documentation only |
| `docs/sdlc-framework/plugins/` | SDLC phase implementations | Documentation only |
| `docs/sdlc-framework/skills/` | Advanced capabilities with scripts | Documentation + Scripts |
| `docs/sdlc-framework/workflows/` | Command sequences | Documentation only |
| `docs/sdlc-framework/hooks/` | Hook examples (UI-managed in IDE) | Documentation only |

### Framework Component Details

#### Agents (`docs/sdlc-framework/agents/`)

**Status**: ❌ Not official Kiro IDE - Documentation only

These files describe specialized AI approaches for different tasks:
- `code-review.md` - Code quality analysis patterns
- `documentation-generator.md` - Documentation generation approach
- `implementation-agent.md` - Feature implementation patterns
- `security-auditor.md` - Security scanning approach
- `test-engineer.md` - Test creation patterns

**Usage**: Reference these documents when working on specific task types to follow consistent patterns.

#### Plugins (`docs/sdlc-framework/plugins/`)

**Status**: ❌ Not official Kiro IDE - Documentation only

These files describe each SDLC phase implementation:
- `spec-writer.md` - Phase 1: Requirements & Design
- `test-writer.md` - Phase 2: TDD Test Creation
- `code-implementer.md` - Phase 3: Implementation
- `builder.md` - Phase 4: Build Verification
- `security-checker.md` - Phase 5: Security Audit
- `docs-generator.md` - Phase 6: Documentation
- `deploy-verifier.md` - Phase 7: Post-Deploy Verification

**Usage**: Reference when working through SDLC phases to ensure consistent implementation.

#### Skills (`docs/sdlc-framework/skills/`)

**Status**: ❌ Not official Kiro IDE - Documentation + Executable Scripts

Advanced capabilities with supporting code:
- `code-reviewer/` - Code review with analysis scripts (Python)
- `documentation-generator/` - Documentation generation utilities (Python)

**Usage**:
- Documentation guides usage patterns
- Python scripts can be executed directly for automated tasks

#### Workflows (`docs/sdlc-framework/workflows/`)

**Status**: ❌ Not official Kiro IDE - Documentation only

Common command sequences and processes:
- `sdlc.md` - Full SDLC workflow orchestration
- `code-review.md` - Review checklist and process
- `test-file.md` - Test generation workflow
- `update-claudemd.md` - Documentation update process

**Usage**: Reference for common development workflows and best practices.

#### Hooks (`docs/sdlc-framework/hooks/`)

**Status**: ❌ Not official Kiro IDE - Documentation only

Hook examples and patterns for reference.

**CRITICAL**: This directory contains **examples only**. Actual hooks are configured via the **Agent Hooks panel** in the IDE UI, not files.

## Integration Between Official and Custom

```
┌─────────────────────────────────────────────────────────────────┐
│                    Official Kiro IDE                            │
│                                                                 │
│  .kiro/steering/        ← Loads phase-specific guidance        │
│  .kiro/settings/mcp     ← Enables 3 MCP servers                │
│  .kiro/specs/           ← Drives Requirements → Design → Tasks │
│  Agent Hooks Panel (UI) ← Configures lifecycle hooks           │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Informs
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Custom SDLC Framework                         │
│                                                                 │
│  docs/sdlc-framework/   ← Reference documentation              │
│    ├── agents/          ← AI persona patterns                  │
│    ├── plugins/         ← SDLC phase implementations           │
│    ├── skills/          ← Advanced capabilities with scripts   │
│    ├── workflows/       ← Command sequences                    │
│    └── hooks/           ← Hook examples (UI-managed in IDE)    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Uses
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Build Automation                              │
│                                                                 │
│  Makefile               ← Build targets for quality gates      │
│    ├── build            ← Lint + type check + tests           │
│    ├── quality-gate     ← Security + dependency scan          │
│    └── ...              ← Individual check targets             │
└─────────────────────────────────────────────────────────────────┘
```

## How Official Kiro Works with Custom Framework

1. **Steering documents** (official Kiro) provide persistent context about the SDLC process
2. **spec-workflow MCP** (official Kiro) manages specs: requirements → design → tasks
3. **Agent Hooks** (official Kiro, UI-configured) automate quality checks on file operations
4. **Framework documentation** (custom) guides implementation of each task following SDLC patterns
5. **Makefile** (standard tooling) provides build automation targets

## What Gets Loaded by Kiro IDE

### On Every Conversation

Kiro IDE automatically loads:
- All files in `.kiro/steering/` (including subdirectories)
- MCP servers configured in `.kiro/settings/mcp.json`
- Hooks configured in Agent Hooks panel (UI)

### What Does NOT Get Loaded

Kiro IDE does NOT automatically load:
- Files in `docs/sdlc-framework/` (custom framework documentation)
- Files referenced by Makefile (build automation)
- Files in `src/`, `tests/`, etc. (your application code)

## For Users: How to Use This Project

### ✅ Official Kiro IDE Features

1. **Edit steering documents** to customize AI behavior:
   ```bash
   # These files are loaded into every conversation
   .kiro/steering/product.md
   .kiro/steering/tech.md
   .kiro/steering/sdlc-workflow.md
   ```

2. **Create specs** using spec-workflow MCP:
   ```
   # In Kiro conversation
   > "Create a spec for user authentication"
   # Uses spec-workflow MCP to create requirements, design, tasks
   ```

3. **Configure hooks** via Agent Hooks panel:
   - Open Kiro IDE
   - Navigate to Agent Hooks panel
   - Add hooks for lint, security, TDD reminders

4. **Reference steering documents**:
   ```
   # In Kiro conversation
   > "#steering:sdlc-workflow Help me implement this feature"
   ```

### 📚 Custom Framework Documentation

1. **Read framework docs** for guidance:
   ```bash
   docs/sdlc-framework/README.md           # Framework overview
   docs/sdlc-framework/plugins/builder.md  # Build phase guidance
   docs/sdlc-framework/hooks/README.md     # Hook examples (reference)
   ```

2. **Run Makefile targets** for quality checks:
   ```bash
   make build                              # Standard build target
   make quality-gate                       # Standard quality target
   ```

3. **Execute skills** when needed:
   ```bash
   python docs/sdlc-framework/skills/code-reviewer/scripts/analyze-metrics.py
   ```

## Key Differences: Kiro IDE vs Kiro CLI

| Feature | Kiro IDE | Kiro CLI |
|---------|----------|----------|
| **Hooks** | UI-managed via Agent Hooks panel | Lifecycle events (not file-based) |
| **MCP Servers** | 3 servers (docs, context7, spec) | 1 server (spec) |
| **Build Automation** | Makefile | Shell scripts |
| **Interface** | Visual IDE with panels | Terminal/CLI |
| **Steering** | Same format | Same format |
| **Specs** | Same format (spec-workflow MCP) | Same format (spec-workflow MCP) |

## Compliance Checklist

- ✅ `.kiro/steering/` contains only steering documents
- ✅ `.kiro/specs/` managed by spec-workflow MCP
- ✅ `.kiro/settings/mcp.json` uses official Kiro MCP format (3 servers)
- ✅ Hooks configured via Agent Hooks panel (UI), not files
- ✅ No `agents/`, `plugins/`, `skills/`, `commands/` directories in `.kiro/`
- ✅ Custom framework moved to `docs/sdlc-framework/`
- ✅ `docs/sdlc-framework/hooks/` clearly marked as examples only
- ✅ README clearly distinguishes official vs custom features

## References

- **Kiro IDE Documentation**: https://kiro.dev/docs/*
- **Steering Docs**: https://kiro.dev/docs/steering
- **MCP Servers**: https://kiro.dev/docs/mcp-servers
- **Agent Hooks**: https://kiro.dev/docs/hooks
- **spec-workflow MCP**: https://github.com/pimzino/spec-workflow-mcp
- **docs-mcp-server**: https://github.com/arabold/docs-mcp-server
- **context7 MCP**: https://github.com/upstash/context7-mcp

## Changelog

| Date | Change | Reason |
|------|--------|--------|
| 2025-12-16 | Initial compliance documentation | Document official vs custom separation |
| 2025-12-16 | Moved agents/, plugins/, skills/, commands/, hooks/ to docs/sdlc-framework/ | Not official Kiro IDE features |
| 2025-12-16 | Clarified hooks are UI-managed, not file-based | Critical IDE difference from CLI |
| 2025-12-16 | Renamed tdd-workflow.md to sdlc-workflow.md | More accurate naming |
