---
name: code-implementer
description: Implementation code to make tests pass
phase: 3-implementation
skills: []
agents: [implementation-agent]
mcp_servers: []
---

# Code Implementer Plugin

Handles the third phase of SDLC: writing minimal code to make tests pass (Green phase of TDD).

## Phase Position

```
1. SPEC → 2. TEST → [3. CODE] → 4. BUILD → 5. SECURITY → 6. DOCS
                        ▲
                        YOU ARE HERE
```

## Prerequisites

From previous phases:
- `design.md` with data models and API contracts (from spec-writer)
- Failing tests (from test-writer)

## TDD Implementation Flow

```
┌─────────────────────────────────────────┐
│            GREEN PHASE                  │
│   Write minimal code to pass tests      │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│           REFACTOR PHASE                │
│   Clean up while keeping tests green    │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│              REPEAT                     │
│   Next failing test → Green → Refactor  │
└─────────────────────────────────────────┘
```

## Workflow

### Step 1: Implement Data Models

From `design.md` specifications:

```typescript
// src/models/entity.ts
import { z } from 'zod';

export const EntitySchema = z.object({
  id: z.string().uuid().optional(),
  name: z.string().min(3).max(100),
  status: z.enum(['active', 'inactive']).default('active'),
  createdAt: z.string().datetime().optional(),
  updatedAt: z.string().datetime().optional()
});

export type Entity = z.infer<typeof EntitySchema>;

export type CreateEntityInput = Pick<Entity, 'name'>;

export function validateEntity(data: unknown): Entity {
  return EntitySchema.parse(data);
}
```

**Run tests**: `npm test -- tests/unit/entities/models.test.ts`

### Step 2: Implement Repository Layer

```typescript
// src/repositories/entity.repository.ts
import { Entity, CreateEntityInput } from '@/models/entity';
import { db } from '@/lib/database';
import { v4 as uuid } from 'uuid';

export class EntityRepository {
  async create(input: CreateEntityInput): Promise<Entity> {
    const now = new Date().toISOString();
    const entity: Entity = {
      id: uuid(),
      name: input.name,
      status: 'active',
      createdAt: now,
      updatedAt: now
    };

    await db.put({
      TableName: 'entities',
      Item: entity,
      ConditionExpression: 'attribute_not_exists(#name)',
      ExpressionAttributeNames: { '#name': 'name' }
    });

    return entity;
  }

  async findById(id: string): Promise<Entity | null> {
    const result = await db.get({
      TableName: 'entities',
      Key: { id }
    });

    return result.Item as Entity | null;
  }

  async findByName(name: string): Promise<Entity | null> {
    const result = await db.query({
      TableName: 'entities',
      IndexName: 'name-index',
      KeyConditionExpression: '#name = :name',
      ExpressionAttributeNames: { '#name': 'name' },
      ExpressionAttributeValues: { ':name': name }
    });

    return result.Items?.[0] as Entity | null;
  }
}
```

### Step 3: Implement Service Layer

```typescript
// src/services/entity.service.ts
import { Entity, CreateEntityInput, validateEntity } from '@/models/entity';
import { EntityRepository } from '@/repositories/entity.repository';
import { ConflictError, NotFoundError, ValidationError } from '@/lib/errors';

export class EntityService {
  constructor(private repository: EntityRepository) {}

  async create(input: CreateEntityInput): Promise<Entity> {
    // Validate input
    try {
      validateEntity({ ...input, status: 'active' });
    } catch (error) {
      throw new ValidationError('Invalid entity data', error);
    }

    // Check for duplicates
    const existing = await this.repository.findByName(input.name);
    if (existing) {
      throw new ConflictError(`Entity with name '${input.name}' already exists`);
    }

    return this.repository.create(input);
  }

  async findById(id: string): Promise<Entity> {
    const entity = await this.repository.findById(id);
    if (!entity) {
      throw new NotFoundError(`Entity with id '${id}' not found`);
    }
    return entity;
  }
}
```

### Step 4: Implement API Endpoints

```typescript
// src/routes/entities.ts
import { Router, Request, Response, NextFunction } from 'express';
import { EntityService } from '@/services/entity.service';
import { EntityRepository } from '@/repositories/entity.repository';
import { ValidationError, ConflictError, NotFoundError } from '@/lib/errors';

const router = Router();
const service = new EntityService(new EntityRepository());

router.post('/', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const entity = await service.create(req.body);
    res.status(201).json(entity);
  } catch (error) {
    if (error instanceof ValidationError) {
      return res.status(400).json({ error: error.message });
    }
    if (error instanceof ConflictError) {
      return res.status(409).json({ error: error.message });
    }
    next(error);
  }
});

router.get('/:id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const entity = await service.findById(req.params.id);
    res.json(entity);
  } catch (error) {
    if (error instanceof NotFoundError) {
      return res.status(404).json({ error: error.message });
    }
    next(error);
  }
});

export default router;
```

### Step 5: Run Tests Continuously

After each implementation step:

```bash
# Run specific test file
npm test -- tests/unit/entities/models.test.ts

# Run all tests for feature
npm test -- tests/**/entities/

# Run all tests
npm test
```

### Step 6: Refactor (When Green)

Once tests pass, refactor while keeping them green:

- Extract common logic to utilities
- Improve naming for clarity
- Remove duplication
- Optimize performance (if needed)

## Subagent Delegation

Spawn `implementation-agent` for complex features:

```
Use Task tool with subagent_type='implementation-agent'
Provide:
- Design specifications
- Failing tests to pass
- Existing codebase patterns to follow
```

## Implementation Principles

1. **Write minimal code** - Only what's needed to pass tests
2. **Follow existing patterns** - Match codebase conventions
3. **Handle errors properly** - Use typed errors, appropriate status codes
4. **Keep functions small** - Single responsibility
5. **Name things clearly** - Self-documenting code

## Code Organization

```
src/
├── models/          # Data types and validation
│   └── entity.ts
├── repositories/    # Data access layer
│   └── entity.repository.ts
├── services/        # Business logic
│   └── entity.service.ts
├── routes/          # API endpoints
│   └── entities.ts
├── lib/             # Shared utilities
│   ├── database.ts
│   └── errors.ts
└── app.ts           # Application setup
```

## Outputs

| Artifact | Location | Purpose |
|----------|----------|---------|
| Models | `src/models/` | Data types and validation |
| Repositories | `src/repositories/` | Database operations |
| Services | `src/services/` | Business logic |
| Routes | `src/routes/` | API endpoints |

## Quality Checks

Before proceeding to Build phase:

- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] No hardcoded values (use config/env)
- [ ] Error handling implemented
- [ ] Code follows project conventions

## Handoff to Next Phase

After implementation complete:
1. All tests passing (Green)
2. Code refactored and clean
3. No TODO comments left unresolved
4. **NEXT**: Pass to `builder` plugin for build verification
