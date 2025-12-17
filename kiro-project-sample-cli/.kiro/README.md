# Kiro CLI Configuration

This directory contains configuration files for the Kiro CLI template.

## cli-config.json Structure

This template uses **external shell scripts** for automation. This is the CLI-first approach that emphasizes:

- Headless execution capability
- CI/CD integration
- Script-based quality gates
- Command-line friendly workflows

### Configuration Approach

```json
{
  "sdlc": {
    "scripts": {
      "lint": "./scripts/lint.sh",
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

**Key Features:**
- Scripts are referenced as paths to executable shell files
- Each script is self-contained and can be run independently
- Perfect for CLI-driven development and CI/CD pipelines
- Scripts live in `./scripts/` directory

## Comparison with kiro-project-sample-ide

The sibling project (kiro-project-sample-ide) uses a different approach:

```json
{
  "phases": {
    "4": {
      "commands": {
        "lint": "ruff check src/ tests/",
        "typeCheck": "mypy src/"
      }
    }
  }
}
```

**IDE Approach Features:**
- Commands are inline strings
- Executed directly by the IDE/CLI
- More suitable for hook-driven workflows
- Commands configured via Makefile as well

## Which Approach to Use?

| Use Shell Scripts (this template) | Use Inline Commands (sample-ide) |
|-----------------------------------|-----------------------------------|
| Building CLI-first tools | Building with IDE integration |
| Need standalone script execution | Prefer Makefile + hooks |
| CI/CD heavy workflows | Interactive development focus |
| Complex build pipelines | Simple command execution |

Both approaches are valid and achieve the same goal - choose based on your development workflow preference.

## Directory Contents

- `cli-config.json` - SDLC phase and script configuration
- `steering/` - Persistent AI context documents
- `specs/` - Feature specifications (managed by spec-workflow MCP)
- `settings/mcp.json` - MCP server configuration
- `hooks/` - Hook configuration (if applicable)
