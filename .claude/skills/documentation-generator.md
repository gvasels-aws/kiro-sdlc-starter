---
description: Generate API documentation, OpenAPI specs, and code documentation
tools: read, write, bash, grep, glob
---

# Documentation Generator Skill

Provides documentation generation capabilities for APIs, code, and project structure.

## Capabilities

- **API Documentation**: Generate OpenAPI/Swagger specs
- **Code Documentation**: TSDoc, GoDoc, docstrings
- **CLAUDE.md Files**: Directory-level documentation
- **Architecture Docs**: System design documentation
- **CHANGELOG**: Release notes and change tracking

## Documentation Types

### OpenAPI Specification
```yaml
openapi: 3.1.0
info:
  title: API Title
  version: 1.0.0
paths:
  /endpoint:
    get:
      summary: Description
```

### Code Documentation
```typescript
/**
 * Function description.
 * @param name - Parameter description
 * @returns Return value description
 */
```

### CLAUDE.md Format
```markdown
# Directory Name

## Overview
Purpose of this directory.

## Files
| File | Description |
|------|-------------|

## Key Functions
### functionName()
Description.
```

## Standards

- OpenAPI 3.1.0 for API specs
- TSDoc for TypeScript
- GoDoc conventions for Go
- Keep a Changelog format

## Usage

This skill is automatically available. It's commonly used:
- During the docs phase of SDLC
- By the documentation-generator agent
- When updating project documentation
