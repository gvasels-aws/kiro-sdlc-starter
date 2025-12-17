# Kiro IDE Configuration

This directory contains configuration files for the Kiro SDLC reference implementation.

## cli-config.json Structure

This project uses **inline commands** and **Makefile integration** for automation. This is the IDE-friendly approach that emphasizes:

- Interactive development workflows
- Hook-driven automation
- Makefile convenience
- IDE panel integration

### Configuration Approach

```json
{
  "phases": {
    "4": {
      "name": "BUILD",
      "commands": {
        "lint": "ruff check src/ tests/",
        "typeCheck": "mypy src/",
        "test": "pytest --cov=src --cov-fail-under=80"
      }
    }
  }
}
```

**Key Features:**
- Commands are defined inline as strings
- Executed directly by the Kiro CLI/IDE
- Complemented by Makefile for convenience (`make build`, `make test`)
- Perfect for IDE-driven development with hooks

## Comparison with kiro-project-sample-cli

The sibling template project (kiro-project-sample-cli) uses a different approach:

```json
{
  "sdlc": {
    "scripts": {
      "build": "./scripts/build.sh"
    }
  },
  "phases": {
    "4": {
      "script": "./scripts/build.sh"
    }
  }
}
```

**CLI Template Features:**
- Scripts are external executable files
- Self-contained shell scripts in `./scripts/` directory
- Better for headless/CI-CD execution
- No Makefile dependency

## Which Approach to Use?

| Use Inline Commands (this project) | Use Shell Scripts (cli-template) |
|-------------------------------------|----------------------------------|
| Building with IDE integration | Building CLI-first tools |
| Prefer Makefile + hooks | Need standalone script execution |
| Interactive development focus | CI/CD heavy workflows |
| Simple command execution | Complex build pipelines |

Both approaches are valid and achieve the same goal - choose based on your development workflow preference.

## Directory Contents

- `cli-config.json` - SDLC phase and inline command configuration
- `steering/` - Persistent AI context documents
- `specs/` - Feature specifications (managed by spec-workflow MCP)
- `settings/mcp.json` - MCP server configuration
- `hooks/` - Hook configuration documentation
