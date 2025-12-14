---
name: sdlc
description: Full SDLC workflow orchestrator - spec, test, code, build, docs → PR → review, security, verify
---

# SDLC Orchestrator

You are orchestrating a complete Software Development Lifecycle workflow. Guide the user through each phase systematically, leveraging plugins, skills, and subagents.

## SDLC Phases (Optimized for Speed & Token Efficiency)

```
┌───────────────────────────────────────────────────────────────────────┐
│                     DEVELOPMENT PHASES (during dev)                    │
├─────────┬─────────┬─────────┬─────────┬───────────┬──────────────────┤
│ 1.SPEC  │ 2.TEST  │ 3.CODE  │ 4.BUILD │  5.DOCS   │    CREATE PR     │
│ ────────│─────────│─────────│─────────│───────────│──────────────────│
│ Plugin: │ Plugin: │ Plugin: │ Plugin: │ Plugin:   │                  │
│ spec-   │ test-   │ code-   │ builder │ docs-     │  gh pr create    │
│ writer  │ writer  │ implmtr │         │ generator │                  │
│         │         │         │         │           │                  │
│ MCP:    │ Agent:  │ Agent:  │ Tools:  │ Agent:    │                  │
│ spec-   │ test-   │ implmnt-│ bash    │ documntn- │                  │
│ workflow│ engineer│ agent   │ linters │ generator │                  │
└─────────┴─────────┴─────────┴─────────┴───────────┴──────────────────┘
                                                             │
                                                             ▼
┌───────────────────────────────────────────────────────────────────────┐
│                       PR-LEVEL PHASES (automated CI)                   │
├─────────────────────┬─────────────────────┬───────────────────────────┤
│    CODE REVIEW      │   SECURITY AUDIT    │      VERIFY (post-deploy) │
│  ───────────────────│─────────────────────│───────────────────────────│
│  claude-code-review │  gitleaks, checkov  │  Health check, smoke test │
│  workflow (auto)    │  semgrep, govulnck  │  Rollback on failure      │
│                     │                     │                           │
│  Runs on: PR opened │  Runs on: PR CI     │  Runs on: deployment      │
└─────────────────────┴─────────────────────┴───────────────────────────┘
```

## Why This Structure?

**Token Efficiency**: Security scans and code reviews run in parallel CI, not consuming interactive tokens.

**Speed**: Developers focus on SPEC → TEST → CODE → BUILD → DOCS without waiting for security scans.

**Quality Gates**: PR cannot merge without passing code review and security checks.

---

## Development Workflow Execution

### Phase 1: Specification (spec-writer plugin)

**Goal**: Define requirements and design before any code.

1. **Gather Requirements**
   - Analyze the feature request or GitHub issue
   - Identify user stories and acceptance criteria
   - Document non-functional requirements

2. **Create Technical Design**
   - Define data models (TypeScript interfaces, Go structs)
   - Specify API contracts (OpenAPI format)
   - Document integration points

3. **Break Down Tasks**
   - Create actionable implementation tasks
   - Identify dependencies between tasks

**Artifacts**: `requirements.md`, `design.md`, `tasks.md`

**MCP**: Use `spec-workflow` server for document creation and approval workflow.

---

### Phase 2: Testing (test-writer plugin)

**Goal**: Write failing tests BEFORE implementation (TDD).

1. **Create Test Structure**
   ```
   tests/
   ├── unit/{feature}/
   ├── integration/{feature}/
   └── e2e/{feature}/
   ```

2. **Write Tests from Contracts**
   - Unit tests for data model validation
   - Integration tests for API endpoints
   - Test all success and error scenarios

3. **Verify Tests Fail**
   - Run tests to confirm they fail (Red phase)
   - This validates tests are actually testing something

**Agent**: Spawn `test-engineer` subagent for complex test scenarios.

**Artifacts**: Test files, fixtures, schema validators

---

### Phase 3: Implementation (code-implementer plugin)

**Goal**: Write minimal code to make tests pass.

1. **Implement Data Models**
   - Create types/interfaces from design
   - Add validation schemas (Zod, etc.)

2. **Implement API Endpoints**
   - Create route handlers
   - Implement business logic
   - Add error handling

3. **Make Tests Pass**
   - Run tests after each change
   - Only write code needed to pass tests
   - Refactor when green

**Agent**: Spawn `implementation-agent` subagent for feature development.

**Artifacts**: Source files in `src/`

---

### Phase 4: Build Verification (builder plugin)

**Goal**: Ensure code quality through automated checks.

1. **Lint Check**
   ```bash
   npm run lint
   # or golangci-lint run ./...
   ```

2. **Type Check**
   ```bash
   npx tsc --noEmit
   # or go build ./...
   ```

3. **Test Suite**
   ```bash
   npm test -- --coverage
   ```

4. **Build Artifacts**
   ```bash
   npm run build
   ```

**Quality Gates**:
- 0 lint errors
- 0 type errors
- 80%+ test coverage
- Successful build

---

### Phase 5: Documentation (docs-generator plugin)

**Goal**: Generate comprehensive documentation before PR.

1. **API Documentation**
   - Generate/update OpenAPI spec
   - Create endpoint documentation

2. **Code Documentation**
   - Add TSDoc/GoDoc comments
   - Document public APIs

3. **CLAUDE.md Files**
   - Create directory documentation
   - Document new functions/exports

4. **CHANGELOG Update (REQUIRED)**
   - Add entry for the feature in `CHANGELOG.md`
   - Use Keep a Changelog format

**Agent**: Spawn `documentation-generator` subagent.

**Artifacts**: `docs/openapi.yaml`, `CLAUDE.md`, `CHANGELOG.md`

---

### Create Pull Request

After completing phases 1-5:

```bash
gh pr create --title "Feature: [description]" --body "$(cat <<'EOF'
## Summary
[Brief description of changes]

## Changes
- [Change 1]
- [Change 2]

## Testing
- [x] Unit tests pass
- [x] Integration tests pass
- [x] Build verification passed

## Documentation
- [x] CLAUDE.md updated
- [x] CHANGELOG.md updated

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## PR-Level Phases (Automated CI)

These phases run automatically when a PR is created - no manual intervention needed.

### Code Review (claude-code-review workflow)

**Trigger**: PR opened or synchronized

**What it does**:
- Reviews code quality (SOLID principles, naming, error handling)
- Checks documentation completeness
- Verifies CLAUDE.md exists in new directories
- Confirms CHANGELOG.md is updated

**Location**: `.github/workflows/claude-code-review.yml`

---

### Security Audit (CI checks)

**Trigger**: PR CI pipeline

**Checks run**:
1. **Secrets Detection**
   ```bash
   gitleaks detect --source .
   ```

2. **Dependency Vulnerabilities**
   ```bash
   npm audit --audit-level=high
   govulncheck ./...
   ```

3. **Infrastructure Security** (if OpenTofu files changed)
   ```bash
   checkov -d infrastructure/ --framework terraform
   ```

4. **SAST Scan**
   ```bash
   semgrep --config=auto .
   ```

**Quality Gates**:
- 0 critical/high vulnerabilities
- 0 hardcoded secrets
- 0 SAST critical findings

---

### Post-Deployment Verification (deploy-verifier plugin)

**Trigger**: After successful deployment to an environment

1. **Health Check**
   ```bash
   curl -f ${API_BASE_URL}/health
   ```

2. **Contract Validation**
   - Validate response schemas match OpenAPI spec
   - Test critical API paths

3. **Smoke Tests**
   ```bash
   npm run verify:deployment
   ```

4. **Rollback on Failure**
   - Automatic Lambda alias rollback
   - Notify team
   - Create incident issue

---

## Orchestration Commands

When user invokes `/sdlc`:

1. **Ask which phase to start from** (or start fresh)
2. **Execute development phases (1-5) sequentially**
3. **Create PR when development complete**
4. **PR-level phases run automatically in CI**

## Phase Transitions

```
Development Flow:
spec-writer ──[approval]──> test-writer ──[tests written]──> code-implementer
                                                                    │
                                                                    ▼
                      docs-generator <──[build passed]── builder
                           │
                           ▼
                       CREATE PR
                           │
                           ▼
              ┌────────────┴────────────┐
              │    PR-Level (Auto CI)   │
              ├─────────────────────────┤
              │ • Code Review           │
              │ • Security Audit        │
              │ • Documentation Check   │
              └────────────┬────────────┘
                           │
                      [PR Approved]
                           │
                           ▼
                        DEPLOY
                           │
                           ▼
                 deploy-verifier ──[passed]──> ✅ Complete
                        │
                   [failed]
                        │
                        ▼
                    Rollback ──> 🚨 Incident
```

## Ad-Hoc Invocation

Users can also invoke individual phases:
- "Run the spec phase" → Load spec-writer plugin
- "Write tests for this design" → Load test-writer plugin
- "Implement this feature" → Load code-implementer plugin
- "Build and verify" → Load builder plugin
- "Generate docs" → Load docs-generator plugin
- "Verify deployment" → Load deploy-verifier plugin (post-deploy only)

## Status Tracking

Use TodoWrite to track progress:

```
[ ] Phase 1: Specification
[ ] Phase 2: Testing (TDD)
[ ] Phase 3: Implementation
[ ] Phase 4: Build Verification
[ ] Phase 5: Documentation + CHANGELOG
[ ] Create PR
────── PR-Level (Automatic) ──────
[ ] Code Review (CI)
[ ] Security Audit (CI)
[ ] PR Approved & Merged
[ ] Deploy to environment
[ ] Post-Deployment Verification
```

## Begin Workflow

Ask the user:
1. What feature are we building?
2. Is there an existing spec or starting fresh?
3. Which phase should we begin with?

Then proceed through the development phases (1-5), create a PR, and let CI handle reviews and security.
