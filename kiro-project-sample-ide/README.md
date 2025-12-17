# Kiro SDLC Reference Implementation

A complete Python project demonstrating the Kiro SDLC workflow with Test-Driven Development (TDD) and working code examples.

## Overview

This project is a **full reference implementation** with working code - use it to learn from a complete example. For a minimal starter template, see [kiro-project-sample-cli](../kiro-project-sample-cli).

This reference implementation includes:

- **6-Phase SDLC Workflow**: SPEC → TEST → CODE → BUILD → QUALITY GATE → DOCS
- **Steering Documents**: Persistent AI context for consistent behavior
- **Hook Configuration**: Automated quality gates (lint, security) via IDE UI
- **MCP Integration**: 3 MCP servers (spec-workflow, docs-mcp-server, context7)
- **TDD Sample**: User management API with 100% test coverage

### Project Structure Philosophy

This project separates **official Kiro IDE features** from **custom SDLC framework documentation**:

```
.kiro/                    ← Official Kiro IDE (steering, specs, MCP settings)
docs/sdlc-framework/      ← Custom framework (agents, plugins, workflows, skills)
Makefile                  ← Build automation
```

**Important**: Only `.kiro/steering/`, `.kiro/specs/`, and `.kiro/settings/` are processed by Kiro IDE. Hooks are configured via the **Agent Hooks panel** in the IDE UI, not files. The `docs/sdlc-framework/` directory contains reference documentation for implementing structured SDLC workflows, but these are **not** official Kiro IDE features.

See `docs/sdlc-framework/README.md` for details on the custom framework.

## Repository Setup

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** (for MCP servers)
- **Kiro IDE** or **Kiro CLI**
- **direnv** (optional, recommended)

### Quick Start

```bash
# Navigate to the sample-ide directory
cd kiro-project-sample-ide

# Option A: Using direnv (Recommended)
# 1. Copy the example environment file
cp .envrc.example .envrc

# 2. Edit .envrc and add your API keys
# Replace "your-context7-api-key-here" with your actual key
nano .envrc  # or vim, code, etc.

# 3. Allow direnv to load the environment
direnv allow

# Option B: Manual setup
python -m venv venv
source venv/bin/activate
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
export CONTEXT7_API_KEY="your-context7-api-key"

# Install dependencies
pip install -e ".[dev]"

# Verify installation
make build
```

### Using Make Commands

```bash
make help           # Show all available commands
make dev-install    # Install development dependencies
make build          # Run lint + type check + tests
make quality-gate   # Run security scan + coverage report
make all            # Run complete SDLC pipeline
make clean          # Remove build artifacts
```

## Environment Configuration

### Using direnv (.envrc)

The project includes `.envrc.example` as a template for environment setup:

```bash
# 1. Copy the example file
cp .envrc.example .envrc

# 2. Edit .envrc and configure your API keys
nano .envrc

# 3. Allow direnv to manage environment
direnv allow

# This automatically:
# - Creates Python virtual environment
# - Sets PYTHONPATH
# - Loads environment variables
# - Loads API keys for MCP servers
```

**Important**: `.envrc` is gitignored to protect your secrets. Always use `.envrc.example` as your starting template.

### Environment Variables

| Variable | Purpose | Required | Default |
|----------|---------|----------|---------|
| `PYTHONPATH` | Include src/ in path | Yes | `${PWD}/src` |
| `CONTEXT7_API_KEY` | Context7 MCP for library docs | Yes* | - |
| `KIRO_PROJECT_PATH` | Project root for CLI | Optional | `${PWD}` |
| `COVERAGE_THRESHOLD` | Minimum test coverage % | Optional | `80` |
| `LINT_MAX_ERRORS` | Max allowed lint errors | Optional | `0` |

\* Required if using the Context7 MCP server for library documentation

### MCP Server Configuration

Edit `.kiro/settings/mcp.json` to configure MCP servers:

```json
{
  "mcpServers": {
    "docs-mcp-server": { ... },
    "context7": { ... },
    "spec-workflow": { ... }
  }
}
```

See `docs/GETTING_STARTED.md` for detailed configuration.

## Project Structure

```
kiro-project-sample-ide/
├── .kiro/                           # ✅ OFFICIAL KIRO IDE
│   ├── steering/                    # AI context documents
│   │   ├── product.md               # Product vision
│   │   ├── tech.md                  # Technology stack
│   │   ├── structure.md             # Directory conventions
│   │   ├── sdlc-workflow.md         # SDLC process
│   │   └── phases/                  # Phase-specific instructions
│   ├── specs/                       # Feature specifications (spec-workflow MCP)
│   │   ├── kiro-ide-sdlc/           # Spec 1: IDE workflow
│   │   └── kiro-cli-sdlc/           # Spec 2: CLI workflow
│   └── settings/
│       └── mcp.json                 # MCP server configuration (3 servers)
│
├── docs/                            # 📚 DOCUMENTATION
│   ├── sdlc-framework/              # Custom SDLC framework
│   │   ├── README.md                # Framework overview
│   │   ├── agents/                  # AI persona patterns
│   │   ├── plugins/                 # SDLC phase implementations
│   │   ├── skills/                  # Advanced capabilities with scripts
│   │   ├── workflows/               # Command sequences
│   │   └── hooks/                   # Hook examples (UI-managed in IDE)
│   ├── api.md                       # API documentation
│   ├── GETTING_STARTED.md           # Setup guide
│   └── KIRO_CLI_SETUP.md            # CLI setup guide
│
├── src/                             # Source code (working Python API)
│   ├── api/                         # API endpoints
│   ├── models/                      # Data models
│   └── services/                    # Business logic
│
├── tests/                           # Test files (100% coverage)
│   ├── unit/                        # Unit tests
│   ├── integration/                 # Integration tests
│   └── fixtures/                    # Test fixtures
│
├── .envrc.example                   # Example environment file
├── .gitignore                       # Git ignore patterns
├── Makefile                         # Build automation
├── pyproject.toml                   # Python project config
├── CHANGELOG.md                     # Change log
└── README.md                        # This file
```

## SDLC Workflow

This project follows a 6-phase SDLC workflow:

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────────┐   ┌─────────┐
│ 1.SPEC  │──►│ 2.TEST  │──►│ 3.CODE  │──►│ 4.BUILD │──►│ 5.QUALITY   │──►│ 6.DOCS  │
│ (Chat)  │   │ (Chat)  │   │ (Chat)  │   │ (Hook)  │   │   GATE      │   │ (Chat)  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────────┘   └─────────┘
```

### Phase Details

| Phase | Description | Artifacts | Mode |
|-------|-------------|-----------|------|
| 1. SPEC | Define requirements and design | requirements.md, design.md, tasks.md | Chat |
| 2. TEST | Write failing tests (TDD Red) | test_*.py, fixtures | Chat |
| 3. CODE | Implement to pass tests (Green) | src/*.py | Chat |
| 4. BUILD | Lint, type check, coverage | Quality reports | Hook |
| 5. QUALITY GATE | Security scan, code review | Security report | Hook+Chat |
| 6. DOCS | Generate documentation | API docs, CHANGELOG | Chat |

### Quality Gates

| Check | Tool | Threshold | Command |
|-------|------|-----------|---------|
| Lint | ruff | 0 errors | `ruff check src/ tests/` |
| Type Check | mypy | 0 errors | `mypy src/` |
| Test Coverage | pytest-cov | 80%+ | `pytest --cov-fail-under=80` |
| Security | bandit | 0 critical/high | `bandit -r src/` |

## Kiro IDE Setup

### 1. Open Project

Open the `kiro-sdlc-sample/` folder in Kiro IDE.

### 2. Configure Hooks

Set up these hooks in Kiro IDE → **Agent Hooks Panel** (UI-managed):

| Hook | Trigger | Pattern | Purpose |
|------|---------|---------|---------|
| Lint on Save | File Save | `**/*.py` | Run ruff check |
| Security Scan | File Save | `src/**/*.py` | Run bandit |
| TDD Reminder | File Create | `src/**/*.py` | Remind tests first |
| Code Review | Manual | - | Review checklist |

**Important**: Hooks are configured through the IDE UI, not files. See `docs/sdlc-framework/hooks/README.md` for hook examples and patterns (reference only).

### 3. Use Steering Documents

Reference in chat:

```
#steering:phases/01-spec Create a spec for user authentication
#steering:sdlc-workflow Help me write tests following TDD
```

## Kiro CLI Setup

### 1. Install Kiro CLI

```bash
curl -fsSL https://cli.kiro.dev/install | bash
```

### 2. Interactive Mode

```bash
kiro-cli
> Run SDLC workflow for user-authentication feature
```

### 3. Headless Mode

```bash
kiro-cli --headless "Run BUILD phase for user-auth spec"
```

### 4. Using spec-workflow MCP

```bash
kiro-cli
> Use spec-workflow to check status of kiro-ide-sdlc spec
> Request approval for the requirements document
```

See `docs/KIRO_CLI_SETUP.md` for complete CLI guide.

## API Reference

### User Management

```python
from src.api.sample_api import get_users, get_user_by_id, create_user

# List users
users = get_users(limit=10, offset=0)

# Get single user
user = get_user_by_id("usr_abc123")

# Create user
new_user = create_user(name="John Doe", email="john@example.com")
```

See `docs/api.md` for complete API documentation.

## MCP Servers

| Server | Package | Purpose |
|--------|---------|---------|
| docs-mcp-server | `@arabold/docs-mcp-server` | Documentation indexing |
| context7 | `@upstash/context7-mcp` | Library documentation |
| spec-workflow | `@pimzino/spec-workflow-mcp` | Specification management |

## Specifications

Two specs demonstrate the SDLC workflow:

### 1. Kiro IDE SDLC (`.kiro/specs/kiro-ide-sdlc/`)

- 30 tasks across 6 groups
- Uses steering documents and hooks
- Chat-driven with hook automation

### 2. Kiro CLI SDLC (`.kiro/specs/kiro-cli-sdlc/`)

- 27 tasks across 6 groups
- Interactive and headless modes
- Integrates with spec-workflow MCP

## Development Workflow

### Running Tests

```bash
# All tests with coverage
pytest

# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# With verbose output
pytest -v
```

### Quality Checks

```bash
# Individual checks
ruff check src/ tests/
mypy src/
bandit -r src/

# All checks via Make
make build
```

### Full SDLC Pipeline

```bash
make all
```

## Contributing

1. Follow TDD - write tests first
2. Ensure all quality gates pass: `make build`
3. Run security scan: `make security`
4. Update CHANGELOG.md
5. Update relevant documentation

## Documentation

### Official Kiro IDE Documentation
- [SDLC Workflow Guide](.kiro/steering/sdlc-workflow.md)
- [Product Vision](.kiro/steering/product.md)
- [Technology Stack](.kiro/steering/tech.md)
- [Project Structure](.kiro/steering/structure.md)
- [Phase-Specific Guidance](.kiro/steering/phases/)

### Custom Framework Documentation
- [SDLC Framework Overview](docs/sdlc-framework/README.md)
- [Agent Patterns](docs/sdlc-framework/agents/)
- [Plugin Implementations](docs/sdlc-framework/plugins/)
- [Workflow Sequences](docs/sdlc-framework/workflows/)
- [Skills with Scripts](docs/sdlc-framework/skills/)
- [Hook Examples (UI-managed)](docs/sdlc-framework/hooks/)

### Setup Guides
- [Getting Started Guide](docs/GETTING_STARTED.md)
- [Kiro CLI Setup](docs/KIRO_CLI_SETUP.md)
- [API Documentation](docs/api.md)

## License

MIT
