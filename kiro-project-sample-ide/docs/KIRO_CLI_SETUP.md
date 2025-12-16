# Kiro CLI Setup Guide

This guide covers setting up and using the Kiro SDLC workflow with Kiro CLI, including integration with the spec-workflow MCP server.

## Installation

### 1. Install Kiro CLI

```bash
# macOS / Linux
curl -fsSL https://cli.kiro.dev/install | bash

# Verify installation
kiro-cli --version
```

### 2. Project Setup

```bash
cd kiro-sdlc-sample

# Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Or use direnv
direnv allow
```

### 3. Environment Configuration

Create or edit `.envrc` (if using direnv):

```bash
# .envrc
layout python3
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"

# MCP API Keys (optional)
export CONTEXT7_API_KEY="your-context7-api-key"
```

Or set environment variables directly:

```bash
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
```

---

## MCP Configuration

### Default MCP Servers

The project includes three MCP servers configured in `.kiro/settings/mcp.json`:

| Server | Purpose |
|--------|---------|
| `docs-mcp-server` | Index and search project documentation |
| `context7` | Library documentation lookup |
| `spec-workflow` | Structured SDLC workflow management |

### spec-workflow MCP Server

The `spec-workflow` MCP server (`@pimzino/spec-workflow-mcp`) provides:

#### Available Tools

| Tool | Purpose | Usage |
|------|---------|-------|
| `spec-workflow-guide` | Load SDLC workflow instructions | Start of SPEC phase |
| `steering-guide` | Create steering documents | Project setup |
| `spec-status` | Check spec progress | Status checks, resume |
| `approvals` | Request/check approvals | Phase transitions |
| `log-implementation` | Record implementation details | After task completion |

#### Example Usage in CLI

```bash
# Start Kiro CLI
kiro-cli

# In chat:
> Load the spec-workflow guide to start SDLC
> Check status of the kiro-ide-sdlc spec
> Request approval for the requirements document
> Log implementation for task 2.1 - User model created
```

---

## SDLC Workflow Modes

### Interactive Mode (Default)

Interactive mode guides you through each phase with prompts and confirmations.

```bash
# Start CLI
kiro-cli

# Example session:
> Start SDLC workflow for user-authentication feature

# CLI will:
# 1. Ask for spec name confirmation
# 2. Guide through each phase
# 3. Request confirmation before transitions
# 4. Show progress and status
```

### Headless Mode

Headless mode runs without prompts, suitable for automation.

```bash
# Run entire workflow
kiro-cli --headless "Run SDLC workflow for spec: user-auth"

# Run specific phase
kiro-cli --headless "Run BUILD phase for user-auth spec"

# Check status
kiro-cli --headless "Check status of user-auth spec"
```

### Combining with Steering Documents

Reference steering documents in your prompts:

```bash
# Interactive
kiro-cli
> #steering:phases/01-spec Create a spec for user profiles

# Headless
kiro-cli --headless "#steering:phases/02-test Write tests for user-profiles spec"
```

---

## CLI Configuration File

Create `.kiro/cli-config.json` for default settings:

```json
{
  "sdlc": {
    "defaultPhase": 1,
    "specPrefix": "",
    "timeout": {
      "phase": 300000,
      "command": 60000
    },
    "quality": {
      "coverageThreshold": 80,
      "lintErrors": 0,
      "securityLevel": "high"
    },
    "output": {
      "format": "human",
      "verbose": false,
      "timestamps": true
    },
    "mcp": {
      "specWorkflow": {
        "autoApprove": false,
        "approvalTimeout": 86400000
      }
    }
  }
}
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `defaultPhase` | 1 | Starting phase for new specs |
| `specPrefix` | "" | Prefix for spec names |
| `timeout.phase` | 300000 | Phase timeout (ms) |
| `timeout.command` | 60000 | Command timeout (ms) |
| `quality.coverageThreshold` | 80 | Minimum coverage % |
| `quality.lintErrors` | 0 | Maximum lint errors |
| `output.format` | "human" | Output format (human/json/quiet) |
| `output.verbose` | false | Verbose logging |

---

## Phase Execution

### Phase 1: SPEC

```bash
# Interactive
kiro-cli
> Create a new spec for user-authentication

# The CLI will:
# 1. Load spec-workflow-guide from MCP
# 2. Create .kiro/specs/user-authentication/
# 3. Generate requirements.md, design.md, tasks.md
# 4. Request approval via approvals MCP tool
```

### Phase 2: TEST

```bash
> Run TEST phase for user-authentication

# The CLI will:
# 1. Read design.md for contracts
# 2. Generate test files in tests/
# 3. Run tests to verify they fail (RED phase)
# 4. Report status
```

### Phase 3: CODE

```bash
> Run CODE phase for user-authentication

# The CLI will:
# 1. Read failing tests
# 2. Guide implementation
# 3. Run tests after changes
# 4. Verify all pass (GREEN phase)
```

### Phase 4: BUILD

```bash
> Run BUILD phase for user-authentication

# The CLI will execute:
# 1. ruff check src/ tests/
# 2. mypy src/
# 3. pytest --cov=src --cov-fail-under=80
# Report results
```

### Phase 5: QUALITY GATE

```bash
> Run QUALITY GATE phase for user-authentication

# The CLI will:
# 1. Run bandit -r src/
# 2. Run safety check
# 3. Trigger code review (interactive) or auto-pass (headless)
```

### Phase 6: DOCS

```bash
> Run DOCS phase for user-authentication

# The CLI will:
# 1. Generate API documentation
# 2. Update CHANGELOG.md
# 3. Update README.md
# 4. Log implementation via MCP
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Prerequisites not met |
| 4 | Phase failed (lint, test, etc.) |
| 5 | Quality gate failed |
| 6 | MCP server error |

### Using in Scripts

```bash
#!/bin/bash

# Run SDLC and check result
kiro-cli --headless "Run SDLC for feature-x"
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "SDLC completed successfully"
elif [ $exit_code -eq 5 ]; then
    echo "Quality gate failed - check security/coverage"
else
    echo "SDLC failed with code: $exit_code"
fi
```

---

## Automation Examples

### CI/CD Integration

```yaml
# .github/workflows/sdlc.yml
name: SDLC Workflow

on:
  push:
    branches: [main]
  pull_request:

jobs:
  sdlc:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"

      - name: Run Quality Checks
        run: |
          ruff check src/ tests/
          mypy src/
          pytest --cov=src --cov-fail-under=80
          bandit -r src/
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run quality checks before commit
ruff check src/ tests/ || exit 1
mypy src/ || exit 1
pytest --tb=short -q || exit 1

echo "All checks passed!"
```

---

## Troubleshooting

### MCP Server Connection Issues

```bash
# Test MCP server directly
npx @pimzino/spec-workflow-mcp@latest --help

# Check Node.js version
node --version  # Should be 18+

# Reinstall MCP server
npm cache clean --force
npx -y @pimzino/spec-workflow-mcp@latest
```

### Steering Documents Not Found

```bash
# Verify steering directory exists
ls -la .kiro/steering/

# Check file permissions
chmod -R 644 .kiro/steering/*.md
```

### Phase Prerequisites Failing

```bash
# Check spec status
kiro-cli --headless "Check status of my-spec"

# List spec files
ls -la .kiro/specs/my-spec/

# Verify previous phase artifacts exist
```

### Coverage Below Threshold

```bash
# Run coverage with detailed report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Identify uncovered lines
pytest --cov=src --cov-report=term-missing
```

---

## Best Practices

1. **Always use spec-workflow MCP** for structured workflow tracking
2. **Log implementations** after completing tasks for future reference
3. **Request approvals** at phase transitions for audit trail
4. **Use headless mode** for CI/CD, interactive for development
5. **Reference steering documents** for consistent AI guidance
6. **Check status frequently** when resuming work
