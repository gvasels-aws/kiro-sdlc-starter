# Kiro CLI Template

A minimal starter template for CLI-first development with Test-Driven Development (TDD) and structured SDLC workflows using Claude Code CLI and the spec-workflow MCP server.

## Overview

This is a **template/skeleton project** - a starting point for new CLI-driven projects. For a complete working example, see [kiro-project-sample-ide](../kiro-project-sample-ide).

This template provides:
- **6-phase SDLC workflow** structure via spec-workflow MCP
- **Test-Driven Development (TDD)** setup for Python
- **Automated quality gates** via shell scripts
- **CLI-first development** approach (headless and interactive modes)
- **Empty source/test structure** ready for your implementation

### Project Structure Philosophy

This project separates **official Kiro CLI features** from **custom SDLC framework documentation**:

```
.kiro/                    ← Official Kiro CLI (steering, specs, MCP settings)
docs/sdlc-framework/      ← Custom framework (agents, plugins, workflows, skills)
scripts/                  ← Build automation (shell scripts)
```

**Important**: Only `.kiro/steering/`, `.kiro/specs/`, and `.kiro/settings/` are processed by Kiro CLI. The `docs/sdlc-framework/` directory contains reference documentation for implementing structured SDLC workflows, but these are **not** official Kiro CLI features.

See `docs/sdlc-framework/README.md` for details on the custom framework.

## Quick Start

### Prerequisites

```bash
# Python 3.11+
python --version

# direnv (optional, recommended for auto environment setup)
# macOS: brew install direnv
# Linux: apt-get install direnv
# Add to your shell: eval "$(direnv hook bash)"  # or zsh, fish, etc.
```

### Environment Setup

**Option A: Using direnv (Recommended)**

```bash
# Copy the example environment file
cp .envrc.example .envrc

# Allow direnv to load the environment
direnv allow

# Install dependencies
pip install -e ".[dev]"
```

**Option B: Manual Setup**

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Set PYTHONPATH
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"

# Install dependencies
pip install -e ".[dev]"
```

### Development Tools

- **ruff**: Fast Python linter
- **mypy**: Static type checker
- **pytest**: Testing framework with coverage
- **bandit**: Security scanner
- **safety**: Dependency vulnerability checker

### Installation

```bash
# Install all dev dependencies
pip install -e ".[dev]"

# Or manually
pip install ruff mypy pytest pytest-cov bandit safety
```

## SDLC Workflow

### 6-Phase Development Pipeline

```
1.SPEC → 2.TEST → 3.CODE → 4.BUILD → 5.QUALITY GATE → 6.DOCS
(MCP)    (CLI)    (CLI)    (Script)   (Script)         (CLI)
```

| Phase | Description | Tool |
|-------|-------------|------|
| 1. **SPEC** | Requirements, design, tasks | spec-workflow MCP |
| 2. **TEST** | Write failing tests (Red) | pytest |
| 3. **CODE** | Implement to pass tests (Green) | Python + Claude |
| 4. **BUILD** | Lint + type check + tests | `./scripts/build.sh` |
| 5. **QUALITY GATE** | Security + dependency scan | `./scripts/quality-gate.sh` |
| 6. **DOCS** | Generate documentation | Claude + manual |

### Interactive Workflow

Start a Claude Code conversation:

```bash
claude --project /path/to/kiro-project-sample-cli
```

Example conversation flow:

```
> "Create a new spec for user authentication"
# Claude uses spec-workflow MCP to create requirements, design, tasks

> "Let's implement task 1.1 - create User model"
# Claude follows TDD: writes failing test first

> "Run the tests"
# Claude executes: pytest tests/unit/test_user.py

> "Implement the User model to make tests pass"
# Claude implements minimal code

> "Run the build pipeline"
# Claude executes: ./scripts/build.sh
```

### Headless Workflow

For CI/CD or scripted automation:

```bash
# Full build check
./scripts/build.sh

# Quality gates
./scripts/quality-gate.sh

# Individual checks
./scripts/lint.sh
./scripts/type-check.sh
./scripts/test.sh
./scripts/security-scan.sh
```

## Environment Configuration

### Environment Variables

| Variable | Purpose | Required | Default |
|----------|---------|----------|---------|
| `PYTHONPATH` | Include src/ in path | Yes | `${PWD}/src` |
| `KIRO_PROJECT_PATH` | Project root for CLI | Optional | `${PWD}` |
| `COVERAGE_THRESHOLD` | Minimum test coverage % | Optional | `80` |
| `LINT_MAX_ERRORS` | Max allowed lint errors | Optional | `0` |
| `PYTHONDONTWRITEBYTECODE` | Prevent .pyc files | Optional | `1` |
| `PYTHONUNBUFFERED` | Unbuffered output | Optional | `1` |

**Important**: `.envrc` is gitignored to protect your configuration. Always use `.envrc.example` as your starting template.

### Manual Environment Setup

If not using direnv:

```bash
# Set PYTHONPATH
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"

# Optional: Development settings
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

# Optional: Quality gate overrides
export COVERAGE_THRESHOLD=80
export LINT_MAX_ERRORS=0
```

## Spec-Workflow MCP Integration

### Creating Specs

The spec-workflow MCP server manages specifications:

```bash
# Inside Claude conversation
> "Create a spec for feature X"

# Spec files are created in .kiro/specs/{spec-name}/
# - requirements.md
# - design.md
# - tasks.md
```

### Spec Approval Workflow

```bash
# Request approval for documents
> "Request approval for the requirements document"

# Check approval status
> "Check spec status for feature-x"
```

### Implementation Logging

```bash
# Log implementation progress
> "Log implementation for task 1.1"
# Creates structured artifacts (APIs, functions, components)
```

## Test-Driven Development

### The TDD Cycle

```
1. RED    → Write a failing test
2. GREEN  → Make the test pass (minimal code)
3. REFACTOR → Improve the code (tests still pass)
```

### Example TDD Flow

**Step 1: Write failing test**

```python
# tests/unit/test_user_service.py
def test_create_user(service: UserService):
    request = CreateUserRequest(name="John", email="john@example.com")
    user = service.create_user(request)
    assert user.name == "John"
    assert user.id.startswith("usr_")
```

```bash
pytest tests/unit/test_user_service.py
# FAILED - ModuleNotFoundError or AssertionError
```

**Step 2: Implement minimal code**

```python
# src/services/user_service.py
class UserService:
    def create_user(self, request: CreateUserRequest) -> User:
        return User(id=f"usr_{uuid.uuid4().hex[:8]}", name=request.name)
```

```bash
pytest tests/unit/test_user_service.py
# PASSED
```

**Step 3: Refactor (optional)**

Improve code while keeping tests green.

## Quality Gates

### Build Pipeline

```bash
./scripts/build.sh
```

Runs:
1. **Lint** (ruff) - Code style and quality
2. **Type Check** (mypy) - Type safety
3. **Tests** (pytest) - 80%+ coverage required

Exit codes:
- `0` = Success
- `1` = Quality check failed
- `2` = Tool not installed

### Quality Gate

```bash
./scripts/quality-gate.sh
```

Runs:
1. **Security Scan** (bandit) - Detect vulnerabilities
2. **Dependency Check** (safety) - Known CVEs

Requirements:
- 0 critical/high security issues
- No known vulnerable dependencies

## Project Structure

```
kiro-project-sample-cli/
├── .kiro/                         # ✅ OFFICIAL KIRO CLI
│   ├── steering/                  # AI context documents
│   │   ├── product.md             # Product vision
│   │   ├── tech.md                # Technology stack
│   │   ├── structure.md           # Directory conventions
│   │   ├── sdlc-workflow.md       # SDLC process
│   │   └── phases/                # Phase-specific guidance
│   ├── specs/                     # Feature specifications (spec-workflow MCP)
│   └── settings/
│       └── mcp.json               # MCP server configuration
│
├── docs/                          # 📚 CUSTOM FRAMEWORK DOCS
│   └── sdlc-framework/            # SDLC implementation patterns
│       ├── README.md              # Framework overview
│       ├── agents/                # AI persona patterns
│       ├── plugins/               # SDLC phase implementations
│       ├── skills/                # Advanced capabilities with scripts
│       ├── workflows/             # Command sequences
│       └── hooks/                 # Hook examples (reference only)
│
├── scripts/                       # Build automation (shell scripts)
│   ├── lint.sh                    # Ruff linting
│   ├── type-check.sh              # MyPy type checking
│   ├── test.sh                    # Pytest with coverage
│   ├── security-scan.sh           # Bandit security scan
│   ├── build.sh                   # Full build pipeline
│   └── quality-gate.sh            # Security + dependency check
│
├── src/                           # Source code (EMPTY - ready for your code)
│   ├── api/                       # API layer (__init__.py only)
│   ├── models/                    # Data models (__init__.py only)
│   └── services/                  # Business logic (__init__.py only)
│
├── tests/                         # Test files (EMPTY - ready for your tests)
│   ├── unit/                      # Unit tests (__init__.py only)
│   ├── integration/               # Integration tests (__init__.py only)
│   └── fixtures/                  # Test fixtures (__init__.py only)
│
├── pyproject.toml                 # Python project configuration
└── README.md                      # This file
```

**Note**: This is a template with empty directories. For a complete working example with actual implementation, see [kiro-project-sample-ide](../kiro-project-sample-ide).

## Configuration

### MCP Server Setup

The spec-workflow MCP server is configured in `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "spec-workflow": {
      "command": "npx",
      "args": ["-y", "@kimtaeyoon83/spec-workflow-mcp-server"],
      "env": {
        "PROJECT_PATH": "${workspaceFolder}"
      }
    }
  }
}
```

### Quality Thresholds

Configure quality thresholds via environment variables:

```bash
# In .envrc or shell
export COVERAGE_THRESHOLD=80
export LINT_MAX_ERRORS=0
```

Scripts automatically enforce these thresholds during `build.sh` and `quality-gate.sh` execution.

## CI/CD Integration

### GitHub Actions Example

```yaml
name: SDLC Pipeline

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Run build pipeline
        run: ./scripts/build.sh

      - name: Run quality gate
        run: ./scripts/quality-gate.sh
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

./scripts/lint.sh && ./scripts/test.sh
```

## Common Workflows

### Starting a New Feature

```bash
# 1. Interactive spec creation
claude --project .
> "Create a spec for the payments feature"
> "Request approval for requirements"

# 2. Wait for approval, then implement
> "Let's start with task 1.1 - PaymentRequest model"

# 3. Follow TDD
> "Write tests for PaymentRequest validation"
> "Implement PaymentRequest to make tests pass"

# 4. Verify quality
> "Run ./scripts/build.sh"
```

### Running Quality Checks

```bash
# Before committing
./scripts/lint.sh && ./scripts/test.sh

# Before merging
./scripts/build.sh && ./scripts/quality-gate.sh
```

### Debugging Failed Tests

```bash
# Run specific test with verbose output
pytest tests/unit/test_user_service.py -v -s

# Run with coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Run only failed tests
pytest --lf
```

## Best Practices

### TDD Discipline

1. **Always write tests first** - No production code without a failing test
2. **Minimal implementation** - Only write code to make tests pass
3. **Refactor fearlessly** - Tests protect against regressions

**Note**: This template has empty source/test directories. Start by creating your first test following the TDD cycle.

### Quality Standards

- **80%+ test coverage** - Enforced by `./scripts/test.sh`
- **0 lint errors** - Clean code style
- **Type hints** - All public functions typed
- **0 security issues** - No critical/high vulnerabilities

### Spec-Driven Development

- **Start with specs** - Define requirements and design first
- **Request approvals** - Get stakeholder sign-off
- **Log implementations** - Track progress and artifacts
- **Update as needed** - Specs evolve with understanding

## Troubleshooting

### Script Not Found

```bash
# Ensure scripts are executable
chmod +x scripts/*.sh
```

### Tool Not Installed

```bash
# Install missing tools
pip install ruff mypy pytest pytest-cov bandit safety
```

### Tests Failing

```bash
# Run tests with verbose output
pytest -v

# Check coverage
pytest --cov=src --cov-report=term-missing
```

### MCP Server Not Loading

```bash
# Verify MCP configuration
cat .kiro/settings/mcp.json

# Ensure spec-workflow is installed
npx -y @kimtaeyoon83/spec-workflow-mcp-server --version
```

## Resources

### Official Kiro CLI Documentation
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

## License

MIT
