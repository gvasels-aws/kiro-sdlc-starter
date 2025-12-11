---
name: docs-generator
description: API and code documentation generation
phase: 6-documentation
skills: [documentation-generator]
agents: [documentation-generator]
mcp_servers: []
---

# Docs Generator Plugin

Generates comprehensive documentation as the final phase before deployment.

## Phase Position

```
1. SPEC → 2. TEST → 3. CODE → 4. BUILD → 5. SECURITY → [6. DOCS]
                                                           ▲
                                                           YOU ARE HERE
```

## Prerequisites

From previous phases:
- Implemented code (from code-implementer)
- Security-approved (from security-checker)
- Design specifications (from spec-writer)

## Documentation Pipeline

```
┌─────────────────────────────────────────┐
│          API DOCUMENTATION               │
│   OpenAPI spec, endpoint docs           │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         CODE DOCUMENTATION               │
│   TSDoc, GoDoc, inline comments         │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│        CLAUDE.md GENERATION              │
│   Directory-level documentation         │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         CHANGELOG UPDATE                 │
│   Document changes for release          │
└─────────────────────────────────────────┘
```

## Workflow

### Step 1: Generate API Documentation

From implemented endpoints, create OpenAPI spec:

```yaml
# docs/openapi.yaml
openapi: 3.1.0
info:
  title: API Documentation
  version: 1.0.0
  description: API for managing resources

servers:
  - url: http://localhost:3000
    description: Development
  - url: https://api.example.com
    description: Production

paths:
  /api/v1/resources:
    post:
      operationId: createResource
      summary: Create a new resource
      tags: [Resources]
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateResourceRequest'
            example:
              name: "my-resource"
              type: "standard"
      responses:
        '201':
          description: Resource created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
        '400':
          $ref: '#/components/responses/ValidationError'
        '409':
          $ref: '#/components/responses/ConflictError'

components:
  schemas:
    Resource:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        status:
          type: string
          enum: [active, inactive]
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time
      required: [id, name, status, createdAt, updatedAt]

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### Step 2: Generate Code Documentation

**TypeScript (TSDoc):**

```typescript
/**
 * Creates a new resource in the system.
 *
 * @param input - The resource creation parameters
 * @returns The created resource with generated ID
 * @throws {ValidationError} When input fails validation
 * @throws {ConflictError} When resource name already exists
 *
 * @example
 * ```typescript
 * const resource = await createResource({
 *   name: 'my-resource',
 *   type: 'standard'
 * });
 * console.log(resource.id); // 'res_abc123'
 * ```
 */
export async function createResource(
  input: CreateResourceInput
): Promise<Resource> {
  // Implementation
}
```

**Go (GoDoc):**

```go
// CreateResource creates a new resource in the system.
//
// It validates the input, checks for duplicates, and persists
// the resource to the database.
//
// Parameters:
//   - ctx: Context for cancellation and deadlines
//   - input: Resource creation parameters
//
// Returns the created resource or an error if:
//   - Validation fails (ValidationError)
//   - Resource name exists (ConflictError)
//
// Example:
//
//	resource, err := svc.CreateResource(ctx, CreateResourceInput{
//	    Name: "my-resource",
//	    Type: "standard",
//	})
func (s *Service) CreateResource(
    ctx context.Context,
    input CreateResourceInput,
) (*Resource, error) {
    // Implementation
}
```

### Step 3: Generate CLAUDE.md Files

For each directory with new/modified code:

```markdown
# src/services/resources/CLAUDE.md

## Overview
Resource management service handling CRUD operations.

## Files

| File | Description |
|------|-------------|
| `service.ts` | Main service class with business logic |
| `repository.ts` | Database operations for resources |
| `types.ts` | TypeScript interfaces and schemas |
| `validation.ts` | Input validation logic |

## Key Functions

### `ResourceService.create(input: CreateResourceInput): Promise<Resource>`
Creates a new resource after validation.
- **Input**: `CreateResourceInput` - name, type, optional metadata
- **Output**: `Resource` - created resource with ID
- **Throws**: `ValidationError`, `ConflictError`

### `ResourceService.findById(id: string): Promise<Resource | null>`
Retrieves a resource by ID.
- **Input**: `id` - UUID of the resource
- **Output**: `Resource` or `null` if not found

## Dependencies

- `@/lib/database` - Database client
- `@/lib/validation` - Zod schemas
- `@/lib/errors` - Custom error types
```

### Step 4: Update CHANGELOG

Add entry for the feature:

```markdown
## [Unreleased]

### Added
- **Resource Management API** - CRUD operations for resources
  - `POST /api/v1/resources` - Create resource
  - `GET /api/v1/resources/:id` - Get resource by ID
  - `PUT /api/v1/resources/:id` - Update resource
  - `DELETE /api/v1/resources/:id` - Delete resource
- Resource validation with Zod schemas
- Repository layer with database abstraction
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

## Documentation Standards

| Type | Format | Location |
|------|--------|----------|
| API Spec | OpenAPI 3.1 | `docs/openapi.yaml` |
| Code Docs | TSDoc/GoDoc | Inline in source |
| Directory Docs | Markdown | `CLAUDE.md` per directory |
| Change Log | Keep a Changelog | `CHANGELOG.md` |

## Quality Checks

```bash
# Validate OpenAPI spec
npx @redocly/cli lint docs/openapi.yaml

# Check TypeScript docs
npx typedoc --validation

# Generate Go docs
go doc -all ./...
```

## CLAUDE.md Update Requirements

**CRITICAL**: CLAUDE.md updates are a mandatory part of the documentation phase.

| Scope | Action | When |
|-------|--------|------|
| **Directory-level** | Create `CLAUDE.md` in new directories | New modules/features added |
| **Directory-level** | Update existing `CLAUDE.md` | Functions/files added or modified |
| **Project-level** | Update root `CLAUDE.md` | New agents, skills, workflows, or architecture changes |

Use `/update-claudemd` command for git-based analysis of project-level changes.

## Outputs

| Artifact | Location | Purpose |
|----------|----------|---------|
| OpenAPI spec | `docs/openapi.yaml` | API documentation |
| API reference | `docs/api/` | Generated HTML docs |
| CLAUDE.md files | Per directory | AI/dev context |
| CHANGELOG entry | `CHANGELOG.md` | Release notes |

## Handoff to Deployment

After documentation complete:
1. OpenAPI spec generated and valid
2. Code documented with TSDoc/GoDoc
3. **CLAUDE.md files created/updated** for all affected directories
4. Root CLAUDE.md updated if project structure changed
5. CHANGELOG updated
6. **READY FOR DEPLOYMENT** - Feature complete!

## SDLC Complete

```
✅ 1. SPEC      - Requirements and design documented
✅ 2. TEST      - Tests written (TDD)
✅ 3. CODE      - Implementation complete
✅ 4. BUILD     - Quality gates passed
✅ 5. SECURITY  - Security audit passed
✅ 6. DOCS      - Documentation generated

🚀 Ready for PR and deployment!
```
