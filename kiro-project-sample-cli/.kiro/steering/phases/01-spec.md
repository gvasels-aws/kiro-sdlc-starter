---
inclusion: manual
---

# Phase 1: Specification (SPEC)

**Mode**: Chat-driven
**Trigger**: User requests to start a new feature or `@spec` mention

## Purpose

Define requirements, design, and implementation tasks before writing any code. This phase ensures alignment between stakeholders and provides a clear roadmap for development.

## Artifacts Produced

| Artifact | Location | Purpose |
|----------|----------|---------|
| `requirements.md` | `.kiro/specs/{feature}/` | User stories, acceptance criteria |
| `design.md` | `.kiro/specs/{feature}/` | Technical architecture, data models, API contracts |
| `tasks.md` | `.kiro/specs/{feature}/` | Implementation breakdown |

## Workflow

### Step 1: Gather Requirements

1. **Understand the Feature Request**
   - What problem does this solve?
   - Who are the users?
   - What are the success criteria?

2. **Write User Stories** (EARS format)
   ```
   WHEN [condition/event]
   THE SYSTEM SHALL [expected behavior]
   ```

3. **Define Acceptance Criteria**
   - Testable conditions for completion
   - Clear pass/fail criteria

### Step 2: Create Technical Design

1. **Data Models**
   ```python
   @dataclass
   class User:
       id: str
       name: str
       email: str
   ```

2. **API Contracts** (OpenAPI format)
   ```yaml
   paths:
     /users:
       get:
         summary: List users
         responses:
           '200':
             description: Success
   ```

3. **Sequence Diagrams** (Mermaid)
   ```mermaid
   sequenceDiagram
       Client->>API: POST /users
       API->>Service: create_user()
       Service->>API: User
       API->>Client: 201 Created
   ```

### Step 3: Break Down Tasks

1. **Group by Dependency**
   - Group 1: Models (no dependencies)
   - Group 2: Services (depends on models)
   - Group 3: API (depends on services)

2. **Estimate Complexity**
   - S: < 2 hours
   - M: 2-4 hours
   - L: 4-8 hours

## Requirements Template

```markdown
# {Feature Name} - Requirements

## Overview
Brief description of the feature.

## User Stories

### REQ-001: {Story Title}
**EARS Syntax:** WHEN {condition}, THE SYSTEM SHALL {behavior}.

**User Story:** As a {role}, I want {goal} so that {benefit}.

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

## Non-Functional Requirements

### Performance
- Response time < 200ms

### Security
- Authentication required
- Input validation on all endpoints
```

## Design Template

```markdown
# {Feature Name} - Design

## Architecture

### System Overview
[Diagram or description]

### Components
- **API Layer**: HTTP handlers
- **Service Layer**: Business logic
- **Model Layer**: Data structures

## Data Models

### {Entity}
```python
@dataclass
class Entity:
    id: str
    name: str
```

## API Contract

```yaml
openapi: 3.0.3
paths:
  /endpoint:
    get:
      summary: Description
```

## Sequence Diagrams

[Mermaid diagram]
```

## Tasks Template

```markdown
# {Feature Name} - Tasks

## Group 1: Models
- [ ] 1.1 Create {Entity} dataclass
- [ ] 1.2 Create {Request} dataclass

## Group 2: Services
- [ ] 2.1 Implement {Entity}Service
- [ ] 2.2 Add validation logic

## Group 3: API
- [ ] 3.1 Implement GET endpoint
- [ ] 3.2 Implement POST endpoint

## Group 4: Tests
- [ ] 4.1 Write unit tests for service
- [ ] 4.2 Write integration tests for API
```

## Exit Criteria

Before moving to Phase 2 (TEST):
- [ ] Requirements document complete
- [ ] Design document complete
- [ ] Tasks broken down
- [ ] Stakeholder approval (if applicable)

## Chat Invocation

```
# Reference this phase
#steering:phases/01-spec

# Start spec workflow
"Create a spec for [feature description]"
```
