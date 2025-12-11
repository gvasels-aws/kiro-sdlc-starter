---
name: builder
description: Build verification, linting, type checking
phase: 4-build
skills: []
agents: []
mcp_servers: []
---

# Builder Plugin

Handles the fourth phase of SDLC: verifying code quality through automated checks before security scanning.

## Phase Position

```
1. SPEC → 2. TEST → 3. CODE → [4. BUILD] → 5. SECURITY → 6. DOCS
                                   ▲
                                   YOU ARE HERE
```

## Prerequisites

From previous phase (code-implementer):
- Implemented code with all tests passing
- Clean, refactored codebase

## Build Verification Pipeline

```
┌─────────────────────────────────────────┐
│             LINT CHECK                  │
│   ESLint, Prettier, golangci-lint       │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│            TYPE CHECK                   │
│   TypeScript, Go build, mypy            │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│           TEST SUITE                    │
│   Full test run with coverage           │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│          BUILD ARTIFACTS                │
│   Compile, bundle, package              │
└─────────────────────────────────────────┘
```

## Workflow

### Step 1: Lint Check

**TypeScript/JavaScript:**
```bash
# Run ESLint
npm run lint
# or
npx eslint . --ext .ts,.tsx,.js,.jsx

# Run Prettier check
npx prettier --check "src/**/*.{ts,tsx,js,jsx}"

# Auto-fix issues
npm run lint:fix
npx prettier --write "src/**/*.{ts,tsx,js,jsx}"
```

**Go:**
```bash
# Run golangci-lint
golangci-lint run ./...

# Run gofmt check
gofmt -l .

# Auto-fix
gofmt -w .
```

**Python:**
```bash
# Run ruff (fast linter)
ruff check .

# Run black check
black --check .

# Auto-fix
ruff check --fix .
black .
```

### Step 2: Type Check

**TypeScript:**
```bash
# Run TypeScript compiler in check mode
npx tsc --noEmit

# With strict mode
npx tsc --noEmit --strict
```

**Go:**
```bash
# Build without outputting binary
go build ./...

# Run vet for additional checks
go vet ./...
```

**Python:**
```bash
# Run mypy
mypy src/

# With strict mode
mypy src/ --strict
```

### Step 3: Test Suite with Coverage

**TypeScript (Vitest):**
```bash
# Run tests with coverage
npm test -- --coverage

# Coverage thresholds
npm test -- --coverage --coverage.thresholds.lines=80
```

**Go:**
```bash
# Run tests with coverage
go test -coverprofile=coverage.out ./...

# View coverage report
go tool cover -html=coverage.out -o coverage.html

# Check coverage percentage
go tool cover -func=coverage.out
```

**Python:**
```bash
# Run pytest with coverage
pytest --cov=src --cov-report=html

# With coverage threshold
pytest --cov=src --cov-fail-under=80
```

### Step 4: Build Artifacts

**TypeScript (Vite):**
```bash
# Production build
npm run build

# Analyze bundle size
npx vite-bundle-visualizer
```

**Go:**
```bash
# Build binary
go build -o bin/app ./cmd/app

# Build for specific platform
GOOS=linux GOARCH=arm64 go build -o bin/app-linux-arm64 ./cmd/app
```

**Docker:**
```bash
# Build container image
docker build -t app:latest .

# Multi-platform build
docker buildx build --platform linux/amd64,linux/arm64 -t app:latest .
```

## Quality Gates

| Check | Threshold | Command |
|-------|-----------|---------|
| Lint errors | 0 | `npm run lint` |
| Type errors | 0 | `npx tsc --noEmit` |
| Test failures | 0 | `npm test` |
| Line coverage | 80%+ | `npm test -- --coverage` |
| Branch coverage | 70%+ | `npm test -- --coverage` |
| Build success | ✓ | `npm run build` |

## Common Issues and Fixes

### Lint Errors

| Error | Fix |
|-------|-----|
| `no-unused-vars` | Remove unused imports/variables |
| `prefer-const` | Use `const` instead of `let` |
| `no-any` | Add proper TypeScript types |
| `max-line-length` | Break long lines |

### Type Errors

| Error | Fix |
|-------|-----|
| `Type X is not assignable to Y` | Fix type mismatch or add type guard |
| `Property does not exist` | Add property to interface or use optional chaining |
| `Argument of type X not assignable` | Cast or update function signature |

### Coverage Issues

| Issue | Fix |
|-------|-----|
| Low line coverage | Add tests for uncovered lines |
| Low branch coverage | Add tests for else/error paths |
| Untested file | Create test file for module |

## CI Integration

Example GitHub Actions workflow:

```yaml
name: Build

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npx tsc --noEmit

      - name: Test with coverage
        run: npm test -- --coverage

      - name: Build
        run: npm run build
```

## Outputs

| Artifact | Location | Purpose |
|----------|----------|---------|
| Lint report | `reports/lint.json` | Lint findings |
| Coverage report | `coverage/` | Test coverage HTML |
| Build output | `dist/` or `bin/` | Production artifacts |
| Bundle analysis | `reports/bundle-stats.html` | Bundle size breakdown |

## Quality Checks

Before proceeding to Security phase:

- [ ] 0 lint errors
- [ ] 0 type errors
- [ ] All tests passing
- [ ] Coverage >= 80%
- [ ] Build successful
- [ ] Bundle size acceptable

## Handoff to Next Phase

After build verification:
1. All lint checks pass
2. No type errors
3. Test coverage meets threshold
4. Build artifacts created
5. **NEXT**: Pass to `security-checker` plugin for security scanning
