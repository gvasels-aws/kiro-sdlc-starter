# Hooks Configuration

## Overview

Hooks are automated triggers that run commands in response to events. While this is a CLI-first template optimized for headless execution, hooks can still be useful for certain workflows.

## Hook Types

### Available Hooks (if using Kiro IDE or compatible tools)

| Hook Type | Trigger Event | Use Case |
|-----------|---------------|----------|
| File Save | After saving a file | Auto-lint, auto-format |
| File Create | When new file created | TDD reminders, template insertion |
| Manual | User-triggered | Code review, security scan |
| Pre-commit | Git commit | Quality gates before commit |

## CLI-First Approach

**This template uses scripts instead of hooks** for quality automation:

```bash
# Instead of hooks on file save
./scripts/lint.sh           # Run manually or in CI

# Instead of pre-commit hooks
./scripts/build.sh          # Run before committing

# Full quality gate
./scripts/quality-gate.sh   # Run before pushing
```

## When to Use Hooks

Hooks are most useful when:
- Using Kiro IDE for interactive development
- Want automatic feedback on file changes
- Integrating with IDE-based workflows
- Running alongside CLI-based automation

## Example Hook Configuration (IDE)

If using Kiro IDE, you can configure hooks in the IDE settings:

### Lint on Save
```json
{
  "trigger": "file.save",
  "pattern": "**/*.py",
  "command": "ruff check ${file}"
}
```

### Security Scan on Save (src files only)
```json
{
  "trigger": "file.save",
  "pattern": "src/**/*.py",
  "command": "bandit ${file}"
}
```

### TDD Reminder on File Create
```json
{
  "trigger": "file.create",
  "pattern": "src/**/*.py",
  "message": "Remember: Write tests first! Create test_{filename} in tests/unit/"
}
```

## Pre-commit Hooks (Git)

For Git-based automation, use standard Git hooks:

```bash
# .git/hooks/pre-commit
#!/bin/bash
./scripts/lint.sh && ./scripts/test.sh
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Hook vs. Script Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| **Hooks** | Automatic, immediate feedback | Requires IDE support, can be intrusive |
| **Scripts** | Portable, CI-friendly, explicit | Manual execution, easy to forget |
| **Both** | Best of both worlds | More complex setup |

## Recommended Setup

For CLI-first development:
1. **Primary**: Use scripts for quality gates
2. **Optional**: Add Git pre-commit hooks
3. **Advanced**: Add IDE hooks if using Kiro IDE

## Reference Implementation

For a complete hook configuration example, see:
- [kiro-project-sample-ide/.kiro/hooks/](../../kiro-project-sample-ide/.kiro/hooks/)

## Further Reading

- Main README: [../README.md](../../README.md)
- SDLC Workflow: [../steering/product.md](../steering/product.md)
- Build Scripts: [../../scripts/](../../scripts/)
