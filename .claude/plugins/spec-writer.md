---
name: spec-writer
description: Requirements gathering and technical design specification
phase: 1-specification
skills: []
agents: []
mcp_servers: [spec-workflow]
---

# Spec Writer Plugin

Orchestrates the specification phase of the SDLC, producing requirements and design documents before any code is written.

## Phase Position

```
[1. SPEC] → 2. TEST → 3. CODE → 4. BUILD → 5. DOCS → PR (Security/Review)
   ▲
   YOU ARE HERE
```

## Workflow

### Step 1: Requirements Gathering

Use `spec-workflow` MCP to create requirements document:

```
1. Analyze user request / GitHub issue
2. Identify stakeholders and acceptance criteria
3. Define user stories (As a... I want... So that...)
4. Document non-functional requirements (performance, security, scalability)
5. Create requirements.md via spec-workflow
```

### Step 2: Technical Design

Produce design artifacts:

```
1. Data models (TypeScript interfaces, Go structs)
2. API contracts (OpenAPI spec with request/response schemas)
3. Architecture decisions (component diagram, data flow)
4. Integration points (external services, databases)
5. Create design.md via spec-workflow
```

### Step 3: Task Breakdown

Generate implementation tasks:

```
1. Break design into discrete, testable tasks
2. Identify dependencies between tasks
3. Estimate complexity (not time)
4. Assign to SDLC phases (which tasks need tests first, etc.)
5. Create tasks.md via spec-workflow
```

## Outputs

| Artifact | Location | Purpose |
|----------|----------|---------|
| `requirements.md` | `.spec-workflow/specs/{feature}/` | User stories, acceptance criteria |
| `design.md` | `.spec-workflow/specs/{feature}/` | Data models, API contracts |
| `tasks.md` | `.spec-workflow/specs/{feature}/` | Implementation breakdown |

## Handoff to Next Phase

After spec approval:
1. Requirements reviewed and approved
2. Design documents complete with data models
3. Tasks broken down and ready for test-first development
4. **NEXT**: Pass to `test-writer` plugin for TDD test creation
