---
name: test-writer
description: TDD test creation before implementation
phase: 2-testing
skills: []
agents: [test-engineer]
mcp_servers: []
---

# Test Writer Plugin

Creates comprehensive test suites BEFORE implementation code, following Test-Driven Development principles.

## Phase Position

```
1. SPEC → [2. TEST] → 3. CODE → 4. BUILD → 5. DOCS → PR (Security/Review)
              ▲
              YOU ARE HERE
```

## Prerequisites

From `spec-writer` plugin:
- `requirements.md` - User stories and acceptance criteria
- `design.md` - Data models and API contracts
- `tasks.md` - Implementation breakdown

## TDD Workflow

### The Three Laws

1. **Write a failing test** before writing any production code
2. **Write only enough test** to demonstrate a failure
3. **Write only enough code** to make the test pass

### Test Categories

| Type | Purpose | Coverage Target |
|------|---------|-----------------|
| Unit | Individual functions | 80%+ |
| Integration | API endpoints, DB operations | Key paths |
| Contract | API response validation | All endpoints |
| E2E | User workflows | Critical flows |

## Subagent Delegation

Spawn `test-engineer` agent for complex test scenarios:

```
Use Task tool with subagent_type='test-engineer'
Provide:
- Data models from design.md
- API contracts to test against
- Specific test category needed
```

## Handoff to Next Phase

After tests are written:
1. All tests fail (Red phase - this is expected!)
2. Test coverage targets defined
3. Test fixtures created
4. **NEXT**: Pass to `code-implementer` plugin to make tests pass
