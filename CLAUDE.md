# CLAUDE.md - Project Documentation

## Project Overview

<!-- Update this section with your project details -->
**Project Name**: [Your Project Name]
**Description**: [Brief description of what this project does]
**Status**: [Planning | Development | Production]

## Repository Structure

```
├── src/                    # Source code
├── tests/                  # Test files
├── docs/                   # Documentation
├── infrastructure/         # IaC (OpenTofu/Terraform)
└── .claude/               # Claude Code automation
    ├── plugins/           # SDLC workflow plugins
    ├── agents/            # Specialized subagents
    ├── skills/            # Reusable capabilities
    └── commands/          # Slash commands
```

## Technology Stack

<!-- Update these tables with your project's technology choices -->

**Backend:**
| Component | Technology |
|-----------|------------|
| Language | [Go / TypeScript / Python] |
| Framework | [Echo / Express / FastAPI] |
| Runtime | [Lambda / EKS / Docker] |

**Frontend:**
| Component | Technology |
|-----------|------------|
| Framework | [React / Vue / Svelte] |
| Build Tool | [Vite / Webpack] |
| Testing | [Vitest / Jest] |

**Infrastructure:**
| Component | Technology |
|-----------|------------|
| Cloud | [AWS / GCP / Azure] |
| IaC | [OpenTofu / Terraform] |
| CI/CD | [GitHub Actions / Buildkite] |

**Data:**
| Component | Technology |
|-----------|------------|
| Database | [PostgreSQL / DynamoDB / MongoDB] |
| Cache | [Redis / Memcached] |

## Development Workflow

### SDLC Workflow (6-Phase)

This project follows a structured Software Development Lifecycle using Claude Code automation:

```
/sdlc → SPEC → TEST → CODE → BUILD → SECURITY → DOCS → Deploy
```

| Phase | Plugin | Description | Artifacts |
|-------|--------|-------------|-----------|
| 1. **Spec** | `spec-writer` | Requirements, design, data models, API contracts | `requirements.md`, `design.md`, `tasks.md` |
| 2. **Test** | `test-writer` | TDD - Write failing tests before implementation | Test files, fixtures |
| 3. **Code** | `code-implementer` | Implement minimal code to make tests pass | Source files |
| 4. **Build** | `builder` | Lint, type check, test coverage, build artifacts | Build output |
| 5. **Security** | `security-checker` | Dependency scan, secrets detection, SAST | Security report |
| 6. **Docs** | `docs-generator` | API docs, code docs, CLAUDE.md, CHANGELOG | Documentation |

### Starting a New Feature

1. **Run `/sdlc`** to start the full workflow, or
2. **Run individual phases** as needed:
   - "Run the spec phase for feature X"
   - "Write tests for this design"
   - "Implement this feature"

### Creating GitHub Issues from Task Groups

**When to use which workflow:**

| Context | Workflow | Description |
|---------|----------|-------------|
| **Chat session** | `/sdlc` command | Implement directly in the conversation - spec, test, code, build, security, docs phases executed inline |
| **GitHub automation** | GitHub Issues | Create issues for each task, tag `@claude` for async implementation |
| **Team collaboration** | GitHub Issues | Track progress, assign work, enable PR reviews |

**Use `/sdlc` in chat when:**
- Working interactively with Claude Code locally
- Implementing a single feature end-to-end
- Rapid prototyping or exploration

**Use GitHub Issues when:**
- Requested to "implement group N in GitHub" or "create issues for group N"
- Working with team members who need visibility
- Tasks need to be tracked, assigned, or scheduled
- Running via GitHub Actions / @claude automation

---

When asked to "implement group N" or "create issues for group N" from a spec's `tasks.md`:

**Workflow:**
1. Read `.spec-workflow/specs/{spec-name}/tasks.md` to find the group
2. Read `.spec-workflow/specs/{spec-name}/design.md` for technical context
3. Create labels if they don't exist (use `gh label create`)
4. Create one GitHub issue per task using `gh issue create`
5. Update `tasks.md` to mark tasks as having issues created (optional)

**Issue Template:**
```markdown
## Overview
[Brief description from task]

**Epic**: [Epic name]
**Group**: [Group number] - [Group name]
**Task**: [Task number]
**Dependencies**: [List dependencies]

## Files to Create
- [List files from task]

## Requirements
[Details from design.md - schemas, API contracts, etc.]

## Acceptance Criteria
- [ ] [Checkboxes for verification]

## Related Specs
- Design: `.spec-workflow/specs/{spec}/design.md`
- Tasks: `.spec-workflow/specs/{spec}/tasks.md`

---
@claude implement this task following TDD - write tests first, then implement
```

**Label Conventions:**
| Label | Description | Color |
|-------|-------------|-------|
| `infrastructure` | Infrastructure and IaC | `#0e8a16` |
| `backend` | Backend services | `#c5def5` |
| `frontend` | Frontend components | `#d4c5f9` |
| `api` | API related | `#c5def5` |
| `epic-{name}` | Epic identifier | `#5319e7` |
| `group-N` | Task group number | `#fbca04` |

**Example Command:**
```bash
# Create labels first
gh label create "infrastructure" --description "Infrastructure and IaC" --color "0e8a16"
gh label create "group-1" --description "Task group 1" --color "fbca04"

# Create an issue
gh issue create \
  --title "[Epic-Task] Brief description" \
  --label "infrastructure,epic-name,group-1" \
  --body "$(cat <<'EOF'
## Overview
...issue body...
EOF
)"
```

**Note:** Use the `gh` CLI tool for private repositories where MCP GitHub tools may lack access.

### Component Hierarchy

| Component | Location | Invocation | Purpose |
|-----------|----------|------------|---------|
| **Plugins** | `.claude/plugins/` | Via `/sdlc` or direct | SDLC workflow phases |
| **Skills** | `.claude/skills/` | Model-invoked (automatic) | Reusable capabilities |
| **Agents** | `.claude/agents/` | Explicit or auto-delegated | Specialized subagents |
| **Commands** | `.claude/commands/` | User-invoked (`/command`) | Slash commands |
| **MCP Servers** | `.mcp.json` | Tool-based | External tools/services |

### Available Skills

| Skill | Purpose | Tools |
|-------|---------|-------|
| `code-reviewer` | Code review with security, performance, and quality analysis | read, grep, diff, lint_runner |
| `documentation-generator` | Generate API documentation and code documentation | read, write, bash, grep, glob |

### Available Agents

| Agent | Purpose | Tools |
|-------|---------|-------|
| `code-review` | Code quality and maintainability analysis | read, grep, diff |
| `documentation-generator` | Generate comprehensive documentation | read, write, bash, grep |
| `implementation-agent` | Full implementation capabilities | read, write, bash, grep, edit, glob |
| `test-engineer` | Test strategy and automated testing | read, write, bash, grep |
| `security-auditor` | Security vulnerability analysis | read, grep, bash |

## Test-Driven Development (TDD)

All development follows TDD principles:

```
Requirements → Data Models → API Contracts → Tests → Implementation → Refactor
```

**The Three Laws of TDD:**
1. Write a failing test before writing any production code
2. Write only enough test to demonstrate a failure
3. Write only enough production code to make the test pass

### Test Coverage Requirements

| Type | Minimum Coverage | Focus Areas |
|------|------------------|-------------|
| Unit Tests | 80% | Business logic, data transformations |
| Integration Tests | Key paths | API contracts, database operations |
| E2E Tests | Critical flows | User journeys, cross-service interactions |

## Documentation Standards

### CHANGELOG.md

Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [Unreleased]

### Added
- New features

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes
```

### Subdirectory CLAUDE.md Files

**Every major subdirectory MUST contain a `CLAUDE.md` file** with:

1. **Overview** - Brief description of the directory's purpose
2. **File Descriptions** - List of files with their purpose
3. **Functions/Exports** - Key functions with signatures and descriptions
4. **Dependencies** - Internal and external dependencies
5. **Usage Examples** - Common usage patterns

**Exception:** The `.claude/` directory and its subdirectories should NOT contain CLAUDE.md files. Documentation for Claude Code capabilities is maintained in dedicated files at the project root:
- `AGENTS.md` - Specialized subagents documentation
- `COMMANDS.md` - Slash commands documentation
- `PLUGINS.md` - SDLC workflow plugins documentation
- `SKILLS.md` - Reusable capabilities documentation

#### When to Update CLAUDE.md

- After adding new files or functions
- After modifying function signatures or behavior
- After removing or deprecating functionality
- During code reviews (verify CLAUDE.md accuracy)

## Quick Reference

### Common Commands

| Command | Purpose |
|---------|---------|
| `/sdlc` | Start full SDLC workflow |
| `/update-claudemd` | Update CLAUDE.md from git changes |
| `/code-review` | Run comprehensive code review |
| `/test-file <path>` | Generate tests for a file |

### Quality Gates

| Phase | Gate Criteria |
|-------|---------------|
| Spec | Design approved |
| Test | Tests written and failing (Red) |
| Code | All tests passing (Green) |
| Build | Lint ✓, Types ✓, Coverage 80%+ |
| Security | 0 critical/high vulnerabilities |
| Docs | OpenAPI valid, CLAUDE.md updated |
