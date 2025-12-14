---
name: builder
description: Build verification, linting, and type checking
phase: 4-build
skills: []
agents: []
mcp_servers: []
---

# Builder Plugin

Verifies code quality through builds, linting, type checking, and test execution.

## Phase Position

```
1. SPEC → 2. TEST → 3. CODE → [4. BUILD] → 5. DOCS → PR (Security/Review)
                                   ▲
                                   YOU ARE HERE
```

## Build Pipeline

```
LINT CHECK (ESLint, golangci-lint, flake8)
         │
         ▼
TYPE CHECK (TypeScript tsc, Go build)
         │
         ▼
TEST SUITE (Unit + Integration + Coverage)
         │
         ▼
BUILD ARTIFACTS (Compile, bundle, package)
         │
         ▼
BUILD VERIFICATION (Start server, smoke test)
```

## Quality Gates

| Check | Tool | Threshold |
|-------|------|-----------|
| Lint | ESLint/golangci-lint | 0 errors, 0 warnings |
| Types | TypeScript/Go | 0 errors |
| Unit Tests | Vitest/Testify | 100% pass |
| Coverage | c8/go cover | 80% minimum |
| Build | Vite/Go | Success |

## Failure Handling

If any check fails:

1. **Lint fails** → Return to `code-implementer`, fix style issues
2. **Type check fails** → Return to `code-implementer`, fix types
3. **Tests fail** → Return to `code-implementer`, fix implementation
4. **Coverage low** → Return to `test-writer`, add more tests
5. **Build fails** → Investigate dependency/config issues

## Handoff to Next Phase

After successful build:
1. All lints pass
2. All types check
3. All tests pass with coverage
4. Build artifacts generated
5. **NEXT**: Pass to `docs-generator` plugin for documentation
