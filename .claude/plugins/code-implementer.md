---
name: code-implementer
description: Implementation code to make tests pass
phase: 3-implementation
skills: []
agents: [implementation-agent]
mcp_servers: []
---

# Code Implementer Plugin

Writes production code to make failing tests pass, following the design specifications.

## Phase Position

```
1. SPEC → 2. TEST → [3. CODE] → 4. BUILD → 5. DOCS → PR (Security/Review)
                        ▲
                        YOU ARE HERE
```

## Prerequisites

From previous phases:
- `design.md` - Data models and API contracts (from spec-writer)
- Failing tests - Test suites expecting implementation (from test-writer)

## TDD Implementation Flow

```
TESTS ARE RED (All tests failing)
         │
         ▼
Write MINIMAL code to pass ONE test at a time
         │
         ▼
RUN TESTS - Does the targeted test pass?
    │                    │
   YES                  NO
    │                    │
    ▼                    ▼
REFACTOR            DEBUG/FIX
(Keep green)        (Stay red)
    │                    │
    └────────────────────┘
              │
              ▼
      Next failing test
```

## Implementation Principles

1. **Minimal Code** - Only write what's needed to pass the test
2. **No Premature Optimization** - Make it work, then make it right
3. **Follow the Contract** - Match API specs exactly
4. **Refactor After Green** - Clean up only when tests pass

## Subagent Delegation

Spawn `implementation-agent` for complex features:

```
Use Task tool with subagent_type='implementation-agent'
Provide:
- Failing test file location
- Design specs to implement
- Code style requirements
```

## Handoff to Next Phase

After implementation:
1. All tests pass (Green phase)
2. Code follows design specifications
3. No hardcoded values or shortcuts
4. **NEXT**: Pass to `builder` plugin for build verification
