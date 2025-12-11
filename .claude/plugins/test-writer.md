---
name: test-writer
description: TDD test creation before implementation
phase: 2-testing
skills: []
agents: [test-engineer]
mcp_servers: []
---

# Test Writer Plugin

Handles the second phase of SDLC: writing failing tests BEFORE implementation (Test-Driven Development).

## Phase Position

```
1. SPEC → [2. TEST] → 3. CODE → 4. BUILD → 5. SECURITY → 6. DOCS
              ▲
              YOU ARE HERE
```

## Prerequisites

From previous phase (spec-writer):
- `requirements.md` with acceptance criteria
- `design.md` with data models and API contracts

## TDD Workflow

```
┌─────────────────────────────────────────┐
│              RED PHASE                  │
│   Write failing tests from contracts    │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│            GREEN PHASE                  │
│   (Handled by code-implementer)         │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│           REFACTOR PHASE                │
│   (Handled by code-implementer)         │
└─────────────────────────────────────────┘
```

## Testing Pyramid

```
        ╱╲
       ╱  ╲         E2E Tests (10%)
      ╱────╲        Critical user journeys
     ╱      ╲
    ╱────────╲      Integration Tests (20%)
   ╱          ╲     API contracts, DB operations
  ╱────────────╲
 ╱              ╲   Unit Tests (70%)
╱────────────────╲  Business logic, utilities
```

## Workflow

### Step 1: Create Test Structure

```
tests/
├── unit/
│   └── {feature}/
│       ├── models.test.ts
│       ├── validation.test.ts
│       └── service.test.ts
├── integration/
│   └── {feature}/
│       ├── api.test.ts
│       └── repository.test.ts
└── e2e/
    └── {feature}/
        └── journey.test.ts
```

### Step 2: Write Unit Tests

From data models in `design.md`:

```typescript
// tests/unit/entities/models.test.ts
import { describe, it, expect } from 'vitest';
import { EntitySchema, validateEntity } from '@/models/entity';

describe('Entity Model', () => {
  describe('validation', () => {
    it('accepts valid entity data', () => {
      const data = {
        name: 'valid-name',
        status: 'active'
      };

      const result = EntitySchema.safeParse(data);
      expect(result.success).toBe(true);
    });

    it('rejects name shorter than 3 characters', () => {
      const data = { name: 'ab' };

      const result = EntitySchema.safeParse(data);
      expect(result.success).toBe(false);
      expect(result.error?.issues[0].path).toContain('name');
    });

    it('rejects name longer than 100 characters', () => {
      const data = { name: 'a'.repeat(101) };

      const result = EntitySchema.safeParse(data);
      expect(result.success).toBe(false);
    });

    it('defaults status to active', () => {
      const data = { name: 'valid-name' };

      const result = validateEntity(data);
      expect(result.status).toBe('active');
    });
  });
});
```

### Step 3: Write Integration Tests

From API contracts in `design.md`:

```typescript
// tests/integration/entities/api.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import { app } from '@/app';
import { setupTestDb, teardownTestDb } from '@/tests/helpers';

describe('POST /api/v1/entities', () => {
  beforeAll(async () => {
    await setupTestDb();
  });

  afterAll(async () => {
    await teardownTestDb();
  });

  it('creates entity with valid input (201)', async () => {
    const response = await request(app)
      .post('/api/v1/entities')
      .send({ name: 'test-entity' })
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(String),
      name: 'test-entity',
      status: 'active',
      createdAt: expect.any(String),
      updatedAt: expect.any(String)
    });
  });

  it('returns 400 for invalid name', async () => {
    const response = await request(app)
      .post('/api/v1/entities')
      .send({ name: 'ab' })
      .expect(400);

    expect(response.body.error).toBeDefined();
  });

  it('returns 409 for duplicate name', async () => {
    // Create first entity
    await request(app)
      .post('/api/v1/entities')
      .send({ name: 'duplicate-name' });

    // Try to create duplicate
    const response = await request(app)
      .post('/api/v1/entities')
      .send({ name: 'duplicate-name' })
      .expect(409);

    expect(response.body.error).toContain('already exists');
  });
});

describe('GET /api/v1/entities/:id', () => {
  it('returns entity by ID (200)', async () => {
    // Create entity first
    const created = await request(app)
      .post('/api/v1/entities')
      .send({ name: 'fetch-test' });

    const response = await request(app)
      .get(`/api/v1/entities/${created.body.id}`)
      .expect(200);

    expect(response.body.name).toBe('fetch-test');
  });

  it('returns 404 for non-existent entity', async () => {
    await request(app)
      .get('/api/v1/entities/non-existent-id')
      .expect(404);
  });
});
```

### Step 4: Write E2E Tests (Critical Paths)

```typescript
// tests/e2e/entities/journey.test.ts
import { test, expect } from '@playwright/test';

test.describe('Entity Management Journey', () => {
  test('user can create and view entity', async ({ page }) => {
    // Navigate to create page
    await page.goto('/entities/new');

    // Fill form
    await page.fill('[data-testid="name-input"]', 'my-entity');
    await page.click('[data-testid="submit-button"]');

    // Verify redirect to detail page
    await expect(page).toHaveURL(/\/entities\/[\w-]+/);
    await expect(page.locator('[data-testid="entity-name"]'))
      .toHaveText('my-entity');
  });
});
```

### Step 5: Verify Tests Fail

Run all tests to confirm they fail (Red phase):

```bash
npm test
# All tests should FAIL because implementation doesn't exist yet
```

## Subagent Delegation

Spawn `test-engineer` agent for complex scenarios:

```
Use Task tool with subagent_type='test-engineer'
Provide:
- Design specifications (data models, API contracts)
- Test coverage requirements
- Edge cases to cover
```

## Framework Recommendations

| Language | Unit Testing | Integration | E2E |
|----------|--------------|-------------|-----|
| TypeScript | Vitest | Supertest | Playwright |
| Go | testing + testify | httptest | - |
| Python | pytest | pytest + httpx | Playwright |

## Coverage Requirements

| Test Type | Target Coverage | Focus |
|-----------|-----------------|-------|
| Unit | 80%+ | Business logic, validation |
| Integration | Key paths | API contracts, DB operations |
| E2E | Critical flows | User journeys |

## Outputs

| Artifact | Location | Purpose |
|----------|----------|---------|
| Unit tests | `tests/unit/{feature}/` | Function-level testing |
| Integration tests | `tests/integration/{feature}/` | API contract testing |
| E2E tests | `tests/e2e/{feature}/` | User journey testing |
| Test fixtures | `tests/fixtures/` | Shared test data |

## Quality Checks

Before proceeding to Code phase:

- [ ] Unit tests cover all data model validations
- [ ] Integration tests cover all API endpoints
- [ ] Error scenarios are tested (400, 404, 409, 500)
- [ ] Tests are organized by feature
- [ ] All tests fail (Red phase confirmed)

## Handoff to Next Phase

After tests written:
1. Test structure created
2. Unit tests cover business logic
3. Integration tests cover API contracts
4. All tests fail (implementation doesn't exist)
5. **NEXT**: Pass to `code-implementer` plugin to make tests pass
