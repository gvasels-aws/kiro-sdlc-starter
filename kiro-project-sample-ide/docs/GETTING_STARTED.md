# Getting Started with Kiro SDLC Sample Project

This guide will help you set up and use the Kiro SDLC sample project for both Kiro IDE and Kiro CLI.

## Prerequisites

- **Python 3.11+**
- **Node.js 18+** (for MCP servers)
- **Kiro IDE** or **Kiro CLI**
- **direnv** (optional, for automatic environment setup)

## Quick Setup

### 1. Clone/Copy the Project

```bash
git clone <repository-url> kiro-sdlc-sample
cd kiro-sdlc-sample
```

### 2. Environment Setup

#### Option A: Using direnv (Recommended)

```bash
# Install direnv if not already installed
# macOS: brew install direnv
# Linux: sudo apt install direnv

# Allow direnv to manage environment
direnv allow

# This automatically:
# - Creates a Python virtual environment
# - Sets PYTHONPATH
# - Loads environment variables
```

#### Option B: Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Set PYTHONPATH
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"

# Install dependencies
pip install -e ".[dev]"
```

### 3. Install Dependencies

```bash
pip install -e ".[dev]"

# Or using requirements file
pip install -r requirements-dev.txt
```

### 4. Verify Installation

```bash
# Run quality checks
ruff check src/ tests/
mypy src/

# Run tests
pytest

# Expected: 39 tests passed, 100% coverage
```

---

## Kiro IDE Setup

### 1. Open Project in Kiro IDE

Open the `kiro-sdlc-sample/` folder in Kiro IDE.

### 2. Configure MCP Servers

The MCP configuration is in `.kiro/settings/mcp.json`. If you need to add API keys:

1. Open `.kiro/settings/mcp.json`
2. Replace `${CONTEXT7_API_KEY}` with your actual API key, or
3. Set the environment variable before launching Kiro IDE

### 3. Set Up Hooks

Configure the following hooks in Kiro IDE:

#### Hook 1: Lint on Save
1. Open Kiro Panel → Agent Hooks → Click `+`
2. **Trigger:** File Save
3. **Pattern:** `**/*.py`
4. **Description:**
   ```
   When a Python file is saved, run ruff check on the file.
   Display any lint errors with suggestions for fixing.
   ```

#### Hook 2: Security Scan on Save
1. **Trigger:** File Save
2. **Pattern:** `src/**/*.py`
3. **Description:**
   ```
   When a source file is saved, run bandit security scan.
   Report findings by severity (LOW, MEDIUM, HIGH, CRITICAL).
   ```

#### Hook 3: TDD Reminder on File Create
1. **Trigger:** File Create
2. **Pattern:** `src/**/*.py`
3. **Description:**
   ```
   When a new source file is created, remind the user:
   "Following TDD: Write tests first in tests/unit/"
   ```

#### Hook 4: Code Review (Manual)
1. **Trigger:** Manual
2. **Description:**
   ```
   Run a comprehensive code review checking:
   - Code quality (naming, SRP, DRY)
   - Security (validation, secrets, auth)
   - Performance (algorithms, cleanup)
   - Testing (coverage, edge cases)
   ```

### 4. Using Steering Documents

Reference steering documents in chat using `#steering:`:

```
# Start the SPEC phase
#steering:phases/01-spec
Create a spec for user authentication

# Reference TDD workflow
#steering:tdd-workflow
Help me write tests for this service
```

---

## Kiro CLI Setup

### 1. Install Kiro CLI

```bash
curl -fsSL https://cli.kiro.dev/install | bash
```

### 2. Navigate to Project

```bash
cd kiro-sdlc-sample
```

### 3. Configure MCP Servers

The CLI uses the same `.kiro/settings/mcp.json` configuration. Set environment variables:

```bash
# Add to .envrc or .bashrc
export CONTEXT7_API_KEY="your-api-key"
```

### 4. Using SDLC Workflow

#### Interactive Mode (Default)

```bash
kiro-cli

# In chat:
> Run the SDLC workflow for a new feature

# Or reference steering directly:
> #steering:phases/01-spec Create a spec for user profile feature
```

#### Headless Mode (Automation)

```bash
# Run full workflow
kiro-cli --headless "Run SDLC for feature: user-profiles"

# Run specific phase
kiro-cli --headless "Run TEST phase for user-profiles spec"
```

### 5. Using spec-workflow MCP

The spec-workflow MCP server provides structured workflow management:

```bash
# In Kiro CLI chat:
> Use spec-workflow to check the status of kiro-ide-sdlc spec
> Request approval for the requirements document
> Log implementation for task 2.1
```

---

## Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `CONTEXT7_API_KEY` | Context7 MCP for library docs | Optional |
| `PYTHONPATH` | Include src/ in path | Yes |
| `KIRO_PROJECT_PATH` | Project root for CLI | Optional |

### Setting Variables

#### Using .envrc (direnv)

```bash
# Edit .envrc
export CONTEXT7_API_KEY="your-key-here"

# Reload
direnv allow
```

#### Using .env file

Create `.env` in project root:

```bash
CONTEXT7_API_KEY=your-key-here
```

#### Using shell profile

```bash
# Add to ~/.bashrc or ~/.zshrc
export CONTEXT7_API_KEY="your-key-here"
```

---

## MCP Server Configuration

### Default Configuration

`.kiro/settings/mcp.json`:

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
      "env": {
        "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}"
      }
    },
    "spec-workflow": {
      "command": "npx",
      "args": ["-y", "@pimzino/spec-workflow-mcp@latest"],
      "env": {}
    }
  }
}
```

### Adding Additional MCP Servers

To add AWS servers (optional):

```json
{
  "mcpServers": {
    "awslabs.aws-documentation-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.aws-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

---

## Project Structure Reference

```
kiro-sdlc-sample/
├── .kiro/
│   ├── steering/          # AI context documents
│   │   ├── product.md     # SDLC workflow definition
│   │   ├── tech.md        # Technology stack
│   │   ├── structure.md   # Directory conventions
│   │   ├── tdd-workflow.md# TDD practices
│   │   └── phases/        # Phase-specific guides
│   ├── specs/             # Feature specifications
│   │   ├── kiro-ide-sdlc/ # Spec 1
│   │   └── kiro-cli-sdlc/ # Spec 2
│   ├── settings/
│   │   └── mcp.json       # MCP configuration
│   └── hooks/
│       └── README.md      # Hook documentation
├── src/                   # Source code
├── tests/                 # Test files
├── docs/                  # Documentation
├── .envrc                 # direnv configuration
├── .gitignore             # Git ignore patterns
├── pyproject.toml         # Python project config
└── README.md              # Project overview
```

---

## Troubleshooting

### MCP Server Not Found

```bash
# Ensure Node.js is installed
node --version

# Install npx globally
npm install -g npx

# Test MCP server
npx @arabold/docs-mcp-server@latest --help
```

### Python Import Errors

```bash
# Ensure PYTHONPATH is set
echo $PYTHONPATH

# Should include: /path/to/project/src

# If using direnv, reload:
direnv allow
```

### Tests Failing

```bash
# Check virtual environment is activated
which python

# Reinstall dependencies
pip install -e ".[dev]"

# Run with verbose output
pytest -v --tb=long
```

### Hooks Not Triggering

1. Check hook is enabled in Kiro Panel
2. Verify file pattern matches saved file
3. Check Kiro Output panel for errors
4. Restart Kiro IDE if needed

---

## Next Steps

1. **Explore Steering Documents**: Read `.kiro/steering/product.md` for workflow overview
2. **Try the SDLC**: Start with `#steering:phases/01-spec` in chat
3. **Review Specs**: Check `.kiro/specs/` for implementation examples
4. **Customize**: Modify steering documents for your project needs
