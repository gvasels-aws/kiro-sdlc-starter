# Getting Started

## Prerequisites

- **Python 3.11+**
- **direnv** (optional but recommended)
- **Node.js 18+** (for MCP servers)

## Quick Start

### 1. Clone and Setup

```bash
# Navigate to the template directory
cd kiro-project-sample-cli

# Copy environment configuration
cp .envrc.example .envrc

# If using direnv
direnv allow

# If not using direnv
python -m venv venv
source venv/bin/activate
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
```

### 2. Install Dependencies

```bash
# Install development dependencies
pip install -e ".[dev]"
```

### 3. Verify Installation

```bash
# Run the build pipeline (should pass with empty template)
./scripts/build.sh

# Run quality gates
./scripts/quality-gate.sh
```

## Development Workflow

### Using Claude Code CLI

```bash
# Start interactive session
claude --project /path/to/kiro-project-sample-cli

# Example conversation
> "Create a new spec for user authentication"
> "Let's implement task 1.1 following TDD"
> "Run the build pipeline"
```

### Test-Driven Development

1. **Write a failing test** (Red)
   ```bash
   # Create test file
   touch tests/unit/test_example.py

   # Write failing test
   pytest tests/unit/test_example.py
   ```

2. **Make the test pass** (Green)
   ```bash
   # Implement minimal code
   # Run test again
   pytest tests/unit/test_example.py
   ```

3. **Refactor** while keeping tests green

### Quality Checks

```bash
# Individual checks
./scripts/lint.sh           # Code style
./scripts/type-check.sh     # Type safety
./scripts/test.sh           # Tests with coverage
./scripts/security-scan.sh  # Security vulnerabilities

# Full pipeline
./scripts/build.sh          # Lint + type + test
./scripts/quality-gate.sh   # Security + dependencies
```

## Creating Your First Feature

### 1. Create a Specification

Use the spec-workflow MCP server to create requirements, design, and tasks:

```bash
claude --project .
> "Create a spec for my new feature"
```

### 2. Write Tests First (TDD)

```bash
# tests/unit/test_my_feature.py
def test_my_feature():
    # Write test that will fail
    assert my_function() == expected_result
```

### 3. Implement the Code

```bash
# src/my_module.py
def my_function():
    # Minimal code to make test pass
    return expected_result
```

### 4. Run Quality Gates

```bash
./scripts/build.sh
```

## Next Steps

- Read [../README.md](../README.md) for detailed information
- Explore `.kiro/steering/` for AI context documents
- Check `.kiro/specs/hello-world/` for an example specification
- Review [../kiro-project-sample-ide](../../kiro-project-sample-ide/) for a complete working example

## Troubleshooting

### Scripts Not Executable

```bash
chmod +x scripts/*.sh
```

### Missing Tools

```bash
pip install ruff mypy pytest pytest-cov bandit safety
```

### PYTHONPATH Issues

```bash
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
```

### MCP Server Not Loading

```bash
# Verify configuration
cat .kiro/settings/mcp.json

# Test MCP server
npx -y @pimzino/spec-workflow-mcp@latest --version
```
