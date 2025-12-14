---
name: docs-generator
description: API and code documentation generation
phase: 5-documentation
skills: [documentation-generator]
agents: [documentation-generator]
mcp_servers: []
---

# Docs Generator Plugin

Generates comprehensive documentation as the final development phase before PR creation.

## Phase Position

```
1. SPEC → 2. TEST → 3. CODE → 4. BUILD → [5. DOCS] → CREATE PR → (Security/Review in CI)
                                              ▲
                                              YOU ARE HERE
```

## Documentation Pipeline

```
API DOCUMENTATION (OpenAPI spec, endpoint docs)
         │
         ▼
CODE DOCUMENTATION (TSDoc, GoDoc, inline comments)
         │
         ▼
CLAUDE.md GENERATION (Directory-level documentation)
         │
         ▼
TASKS.MD UPDATE (Mark completed tasks in spec)
         │
         ▼
CHANGELOG UPDATE (REQUIRED - document changes)
```

## CHANGELOG.md Requirements (MANDATORY)

**Every feature or fix MUST have a CHANGELOG.md entry before the PR is complete.**

### Format (Keep a Changelog)
```markdown
## [Unreleased]

### Added
- New features

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes
```

## Subagent Delegation

Spawn `documentation-generator` agent:

```
Use Task tool with subagent_type='documentation-generator'
Provide:
- Source files to document
- API endpoints implemented
- Design specs for reference
```

## Handoff to PR Creation

After documentation complete:
1. OpenAPI spec generated and valid
2. Code documented with TSDoc/GoDoc
3. **CLAUDE.md files created/updated** for all affected directories
4. CHANGELOG updated
5. **NEXT**: Create PR - Security and Code Review run automatically in CI

## Development Phases Complete

```
✅ 1. SPEC      - Requirements and design documented
✅ 2. TEST      - Tests written (TDD)
✅ 3. CODE      - Implementation complete
✅ 4. BUILD     - Quality gates passed
✅ 5. DOCS      - Documentation generated

🚀 Ready for PR! Security audit and code review run automatically in CI.
```
