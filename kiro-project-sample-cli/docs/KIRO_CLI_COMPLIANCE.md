# Kiro CLI Compliance Documentation

**Last Updated**: 2025-12-16
**Kiro Documentation Reference**: https://kiro.dev/docs/cli/*

## Executive Summary

This project is structured to **clearly separate official Kiro CLI features** from **custom SDLC framework documentation**. This document explains what is processed by Kiro CLI and what is not.

## Official Kiro CLI Features

### ✅ What Kiro CLI Processes

| Directory/File | Purpose | Documentation |
|----------------|---------|---------------|
| `.kiro/steering/` | Persistent AI context loaded into every conversation | [Steering Docs](https://kiro.dev/docs/cli/steering) |
| `.kiro/specs/` | Feature specifications managed by spec-workflow MCP | [Specs via MCP](https://kiro.dev/docs/cli/mcp-servers) |
| `.kiro/settings/mcp.json` | MCP server configuration | [MCP Config](https://kiro.dev/docs/cli/mcp-servers) |

### Steering Documents (`.kiro/steering/`)

**Status**: ✅ Official Kiro CLI Feature

These files are loaded by Kiro CLI as persistent context:

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

**Status**: ✅ Official Kiro CLI Feature (via MCP)

Managed by the `spec-workflow` MCP server configured in `.kiro/settings/mcp.json`.

**What it provides**:
- Requirements → Design → Tasks workflow
- Approval system for documents
- Implementation logging
- Spec status tracking

**Configuration**:
```json
{
  "mcpServers": {
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

### MCP Servers (`.kiro/settings/mcp.json`)

**Status**: ✅ Official Kiro CLI Feature

Kiro CLI loads MCP servers defined in this configuration file.

**Available in this project**:
- `spec-workflow` - Specification management and SDLC orchestration

## Custom SDLC Framework (NOT Official Kiro)

### ❌ What Kiro CLI Does NOT Process

The following directories contain **reference documentation and implementation patterns** for structuring SDLC workflows. They are **not** processed by Kiro CLI as features.

| Directory | Purpose | Status |
|-----------|---------|--------|
| `docs/sdlc-framework/agents/` | AI persona patterns | Documentation only |
| `docs/sdlc-framework/plugins/` | SDLC phase implementations | Documentation only |
| `docs/sdlc-framework/skills/` | Advanced capabilities with scripts | Documentation + Scripts |
| `docs/sdlc-framework/workflows/` | Command sequences | Documentation only |
| `docs/sdlc-framework/hooks/` | Hook examples | Documentation only |

### Framework Component Details

#### Agents (`docs/sdlc-framework/agents/`)

**Status**: ❌ Not official Kiro CLI - Documentation only

These files describe specialized AI approaches for different tasks:
- `code-review.md` - Code quality analysis patterns
- `documentation-generator.md` - Documentation generation approach
- `implementation-agent.md` - Feature implementation patterns
- `security-auditor.md` - Security scanning approach
- `test-engineer.md` - Test creation patterns

**Usage**: Reference these documents when working on specific task types to follow consistent patterns.

#### Plugins (`docs/sdlc-framework/plugins/`)

**Status**: ❌ Not official Kiro CLI - Documentation only

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

**Status**: ❌ Not official Kiro CLI - Documentation + Executable Scripts

Advanced capabilities with supporting code:
- `code-reviewer/` - Code review with analysis scripts (Python)
- `documentation-generator/` - Documentation generation utilities (Python)

**Usage**:
- Documentation guides usage patterns
- Python scripts can be executed directly for automated tasks

#### Workflows (`docs/sdlc-framework/workflows/`)

**Status**: ❌ Not official Kiro CLI - Documentation only

Common command sequences and processes:
- `sdlc.md` - Full SDLC workflow orchestration
- `code-review.md` - Review checklist and process
- `test-file.md` - Test generation workflow
- `update-claudemd.md` - Documentation update process

**Usage**: Reference for common development workflows and best practices.

#### Hooks (`docs/sdlc-framework/hooks/`)

**Status**: ❌ Not official Kiro CLI - Documentation only

Hook examples and patterns for reference.

**Important**: Kiro CLI hooks are lifecycle events, not a file-based system. This directory contains examples for educational purposes only.

## Integration Between Official and Custom

```
┌─────────────────────────────────────────────────────────────────┐
│                    Official Kiro CLI                            │
│                                                                 │
│  .kiro/steering/        ← Loads phase-specific guidance        │
│  .kiro/settings/mcp     ← Enables spec-workflow MCP            │
│  .kiro/specs/           ← Drives Requirements → Design → Tasks │
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
│    └── hooks/           ← Hook examples                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Uses
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Build Automation                              │
│                                                                 │
│  scripts/               ← Shell scripts for quality gates      │
│    ├── build.sh         ← Lint + type check + tests           │
│    ├── quality-gate.sh  ← Security + dependency scan          │
│    └── ...              ← Individual check scripts             │
└─────────────────────────────────────────────────────────────────┘
```

## How Official Kiro Works with Custom Framework

1. **Steering documents** (official Kiro) provide persistent context about the SDLC process
2. **spec-workflow MCP** (official Kiro) manages specs: requirements → design → tasks
3. **Framework documentation** (custom) guides implementation of each task following SDLC patterns
4. **Shell scripts** (standard tooling) automate quality checks

## What Gets Loaded by Kiro CLI

### On Every Conversation

Kiro CLI automatically loads:
- All files in `.kiro/steering/` (including subdirectories)
- MCP servers configured in `.kiro/settings/mcp.json`

### What Does NOT Get Loaded

Kiro CLI does NOT automatically load:
- Files in `docs/sdlc-framework/` (custom framework documentation)
- Files in `scripts/` (shell scripts for CI/CD)
- Files in `src/`, `tests/`, etc. (your application code)

## For Users: How to Use This Project

### ✅ Official Kiro CLI Features

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

3. **Reference steering documents**:
   ```
   # In Kiro conversation
   > "#steering:sdlc-workflow Help me implement this feature"
   ```

### 📚 Custom Framework Documentation

1. **Read framework docs** for guidance:
   ```bash
   docs/sdlc-framework/README.md           # Framework overview
   docs/sdlc-framework/plugins/builder.md  # Build phase guidance
   ```

2. **Run scripts** for quality checks:
   ```bash
   ./scripts/build.sh                      # Standard shell script
   ./scripts/quality-gate.sh               # Standard shell script
   ```

3. **Execute skills** when needed:
   ```bash
   python docs/sdlc-framework/skills/code-reviewer/scripts/analyze-metrics.py
   ```

## Compliance Checklist

- ✅ `.kiro/steering/` contains only steering documents
- ✅ `.kiro/specs/` managed by spec-workflow MCP
- ✅ `.kiro/settings/mcp.json` uses official Kiro MCP format
- ✅ No `agents/`, `plugins/`, `skills/`, `commands/` directories in `.kiro/`
- ✅ Custom framework moved to `docs/sdlc-framework/`
- ✅ No `cli-config.json` (not used by Kiro CLI)
- ✅ README clearly distinguishes official vs custom features

## References

- **Kiro CLI Documentation**: https://kiro.dev/docs/cli/*
- **Steering Docs**: https://kiro.dev/docs/cli/steering
- **MCP Servers**: https://kiro.dev/docs/cli/mcp-servers
- **spec-workflow MCP**: https://github.com/pimzino/spec-workflow-mcp

## Changelog

| Date | Change | Reason |
|------|--------|--------|
| 2025-12-16 | Initial compliance documentation | Document official vs custom separation |
| 2025-12-16 | Moved agents/, plugins/, skills/, commands/, hooks/ to docs/sdlc-framework/ | Not official Kiro CLI features |
| 2025-12-16 | Removed cli-config.json | Not used by Kiro CLI |
| 2025-12-16 | Renamed tdd-workflow.md to sdlc-workflow.md | More accurate naming |
