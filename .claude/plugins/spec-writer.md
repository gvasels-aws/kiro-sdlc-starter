---
name: spec-writer
description: Requirements gathering and technical design
phase: 1-specification
skills: []
agents: []
mcp_servers: [spec-workflow]
---

# Spec Writer Plugin

Handles the first phase of SDLC: gathering requirements and creating technical design before any code is written.

## Phase Position

```
[1. SPEC] → 2. TEST → 3. CODE → 4. BUILD → 5. SECURITY → 6. DOCS
    ▲
    YOU ARE HERE
```

## Prerequisites

- Feature request, user story, or GitHub issue
- Stakeholder availability for clarification

## Specification Pipeline

```
┌─────────────────────────────────────────┐
│         REQUIREMENTS GATHERING          │
│   User stories, acceptance criteria     │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│          TECHNICAL DESIGN               │
│   Data models, API contracts            │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│           TASK BREAKDOWN                │
│   Implementation tasks with estimates   │
└─────────────────────────────────────────┘
```

## Workflow

### Step 1: Gather Requirements

Create `requirements.md` with:

```markdown
# Feature: [Feature Name]

## Overview
Brief description of the feature and its purpose.

## User Stories

### US-1: [Story Title]
**As a** [user type]
**I want** [capability]
**So that** [benefit]

#### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Non-Functional Requirements

### Performance
- Response time < 200ms for API calls
- Support 100 concurrent users

### Security
- Authentication required
- Input validation on all endpoints

### Scalability
- Horizontal scaling capability
```

### Step 2: Create Technical Design

Create `design.md` with:

```markdown
# Technical Design: [Feature Name]

## Data Models

### Entity: [EntityName]
```typescript
interface Entity {
  id: string;           // UUID v4
  name: string;         // 3-100 characters
  status: 'active' | 'inactive';
  createdAt: string;    // ISO 8601
  updatedAt: string;    // ISO 8601
}
```

## API Contracts

### POST /api/v1/entities
Creates a new entity.

**Request:**
```json
{
  "name": "string (required, 3-100 chars)"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "name": "string",
  "status": "active",
  "createdAt": "ISO8601",
  "updatedAt": "ISO8601"
}
```

**Errors:**
- 400: Validation error
- 409: Entity already exists

## Database Schema

| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | PK |
| name | VARCHAR(100) | NOT NULL, UNIQUE |
| status | ENUM | DEFAULT 'active' |

## Integration Points

- External API: [description]
- Event bus: [events published/consumed]
```

### Step 3: Break Down Tasks

Create `tasks.md` with:

```markdown
# Implementation Tasks

## Task 1: Create Data Models
- [ ] Define TypeScript interfaces
- [ ] Create validation schemas (Zod/Joi)
- [ ] Add database migration

**Estimated effort:** Small

## Task 2: Implement API Endpoints
- [ ] POST /api/v1/entities
- [ ] GET /api/v1/entities/:id
- [ ] PUT /api/v1/entities/:id
- [ ] DELETE /api/v1/entities/:id

**Estimated effort:** Medium

## Task 3: Add Business Logic
- [ ] Validation rules
- [ ] Error handling
- [ ] Event publishing

**Estimated effort:** Medium

## Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 2
```

## MCP Server Usage

Use `spec-workflow` MCP server for:

```
spec-workflow-guide     → Load workflow instructions
steering-guide          → Create project steering docs
spec-status             → Check spec completion status
approvals               → Request approval for documents
log-implementation      → Record implementation details
```

## Outputs

| Artifact | Location | Purpose |
|----------|----------|---------|
| Requirements | `specs/{feature}/requirements.md` | User stories, acceptance criteria |
| Design | `specs/{feature}/design.md` | Data models, API contracts |
| Tasks | `specs/{feature}/tasks.md` | Implementation breakdown |

## Quality Checks

Before proceeding to Test phase:

- [ ] All user stories have acceptance criteria
- [ ] Data models are fully defined with types
- [ ] API contracts specify request/response formats
- [ ] Error scenarios are documented
- [ ] Tasks are broken down and estimated
- [ ] Stakeholder has approved the spec

## Handoff to Next Phase

After spec approval:
1. Requirements documented and approved
2. Design complete with data models and API contracts
3. Tasks broken down and ready for implementation
4. **NEXT**: Pass to `test-writer` plugin for TDD test creation
