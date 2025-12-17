# Custom SDLC Framework Documentation

## ⚠️ Important Clarification

**This is NOT a built-in Kiro IDE feature.**

This directory contains documentation for a **custom 6-phase SDLC framework** built on top of Kiro IDE.

## What This Framework Is

- ✅ **Organizational patterns and documentation**
- ✅ **Workflow guidance via Kiro steering documents**
- ✅ **Quality automation via Makefile and shell scripts**
- ❌ **NOT processed by Kiro IDE as features**

## Directory Structure

```
docs/sdlc-framework/
├── agents/          # AI persona patterns (documentation only)
├── plugins/         # SDLC phase implementations (documentation only)
├── skills/          # Advanced capabilities with scripts
├── workflows/       # Command sequences (documentation only)
└── hooks/           # Hook examples (for reference - UI-managed in IDE)
```

## How It Works with Kiro IDE

### 1. Steering Documents Guide AI
Located in `.kiro/steering/phases/`, these files provide phase-specific guidance:
- **01-spec.md** - Requirements and design
- **02-test.md** - Test-Driven Development
- **03-code.md** - Implementation
- **04-build.md** - Build verification
- **05-quality-gate.md** - Security and quality
- **06-docs.md** - Documentation

Kiro IDE loads these via its official steering system.

### 2. Makefile Automates Quality
Located at `Makefile`, this provides build automation:
- `make build` - Lint + type check + tests
- `make quality-gate` - Security scan + coverage
- `make install` - Setup dependencies
- `make test` - Run tests
- Individual targets for each check

These are standard tooling, not Kiro-specific.

### 3. Hooks Configured via UI
**Important**: Unlike file-based approaches, Kiro IDE manages hooks through the **Agent Hooks panel** in the UI:
- Pre-tool hooks
- Post-tool hooks
- Lifecycle hooks

The `hooks/` directory in this framework is **reference documentation only** - actual hook configuration happens in the IDE interface.

### 4. Documentation Provides Patterns
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
- `deploy-verifier.md` - Phase 7: Post-Deploy Verification

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

## Integration with Official Kiro IDE

```
Official Kiro IDE              Custom Framework
────────────────────          ─────────────────
.kiro/steering/      ───────► Loads: Phase-specific guidance
.kiro/settings/mcp   ───────► Enables: 3 MCP servers
                                - spec-workflow (SDLC orchestration)
                                - docs-mcp-server (Documentation search)
                                - context7 (Library context)
.kiro/specs/         ───────► Drives: Requirements → Design → Tasks

Agent Hooks Panel    ───────► Configures: Lifecycle hooks (UI-based)
Makefile             ───────► Automates: Quality gates

                              Supports: docs/sdlc-framework/
                                        ├── agents/
                                        ├── plugins/
                                        ├── skills/
                                        └── workflows/

src/                 ───────► Example: Working Python API
```

## Working Python API Example

This project includes a reference implementation:
- FastAPI-based REST API
- Comprehensive test suite (pytest)
- Quality automation (ruff, mypy, bandit)
- TDD workflow demonstration

Use this as a template for new projects following the SDLC framework.

## For Users

1. **Use official Kiro IDE features** (steering, MCP, specs, UI-based hooks)
2. **Reference framework docs** when implementing each phase
3. **Run Makefile targets** for quality checks
4. **Configure hooks via Agent Hooks panel** in the IDE
5. **Leverage steering guidance** via `.kiro/steering/phases/`
6. **Study the Python API example** for TDD patterns

This framework enhances Kiro IDE with structured SDLC guidance while remaining fully compatible with official Kiro features.
