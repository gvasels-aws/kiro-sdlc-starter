# Custom SDLC Framework Documentation

## ⚠️ Important Clarification

**This is NOT a built-in Kiro CLI feature.**

This directory contains documentation for a **custom 6-phase SDLC framework** built on top of Kiro CLI.

## What This Framework Is

- ✅ **Organizational patterns and documentation**
- ✅ **Workflow guidance via Kiro steering documents**
- ✅ **Quality automation via shell scripts**
- ❌ **NOT processed by Kiro CLI as features**

## Directory Structure

```
docs/sdlc-framework/
├── agents/          # AI persona patterns (documentation only)
├── plugins/         # SDLC phase implementations (documentation only)
├── skills/          # Advanced capabilities with scripts
├── workflows/       # Command sequences (documentation only)
└── hooks/           # Hook examples (for reference)
```

## How It Works with Kiro CLI

### 1. Steering Documents Guide AI
Located in `.kiro/steering/phases/`, these files provide phase-specific guidance:
- **01-spec.md** - Requirements and design
- **02-test.md** - Test-Driven Development
- **03-code.md** - Implementation
- **04-build.md** - Build verification
- **05-quality-gate.md** - Security and quality
- **06-docs.md** - Documentation

Kiro CLI loads these via its official steering system.

### 2. Shell Scripts Automate Quality
Located in `scripts/`, these provide build automation:
- `build.sh` - Lint + type check + tests
- `quality-gate.sh` - Security scan + coverage
- Individual scripts for each check

These are standard tooling, not Kiro-specific.

### 3. Documentation Provides Patterns
This directory provides reference material for:
- **Agents**: Specialized AI personas for different tasks
- **Plugins**: SDLC phase implementation patterns
- **Skills**: Advanced capabilities with supporting scripts
- **Workflows**: Common development sequences

## Framework Components

### Agents (Documentation)
Describe specialized AI approaches for specific tasks:
- `code-review.md` - Code quality analysis patterns
- `documentation-generator.md` - Documentation generation approach
- `implementation-agent.md` - Feature implementation patterns
- `security-auditor.md` - Security scanning approach
- `test-engineer.md` - Test creation patterns

**Usage**: Reference these when working on specific task types.

### Plugins (Documentation)
Describe each SDLC phase implementation:
- `spec-writer.md` - Phase 1: Requirements & Design
- `test-writer.md` - Phase 2: TDD Test Creation
- `code-implementer.md` - Phase 3: Implementation
- `builder.md` - Phase 4: Build Verification
- `security-checker.md` - Phase 5: Security Audit
- `docs-generator.md` - Phase 6: Documentation

**Usage**: Reference when working through SDLC phases.

### Skills (Documentation + Scripts)
Advanced capabilities with supporting code:
- `code-reviewer/` - Code review with analysis scripts
- `documentation-generator/` - Documentation generation utilities

**Usage**: Python scripts can be executed; documentation guides usage.

### Workflows (Documentation)
Common command sequences:
- `sdlc.md` - Full SDLC workflow orchestration
- `code-review.md` - Review checklist and process
- `test-file.md` - Test generation workflow
- `update-claudemd.md` - Documentation update process

**Usage**: Reference for common development workflows.

## Integration with Official Kiro CLI

```
Official Kiro CLI              Custom Framework
────────────────────          ─────────────────
.kiro/steering/      ───────► Loads: Phase-specific guidance
.kiro/settings/mcp   ───────► Enables: spec-workflow MCP tool
.kiro/specs/         ───────► Drives: Requirements → Design → Tasks

scripts/             ───────► Automates: Quality gates

                              Supports: docs/sdlc-framework/
                                        ├── agents/
                                        ├── plugins/
                                        ├── skills/
                                        └── workflows/
```

## For Users

1. **Use official Kiro features** (steering, MCP, specs)
2. **Reference framework docs** when implementing each phase
3. **Run shell scripts** for quality checks
4. **Leverage steering guidance** via `.kiro/steering/phases/`

This framework enhances Kiro CLI with structured SDLC guidance while remaining fully compatible with official Kiro features.
