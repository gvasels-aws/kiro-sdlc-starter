---
name: sdlc
description: Full SDLC workflow orchestrator - spec, test, code, build, security, docs, verify
---

# SDLC Orchestrator

You are orchestrating a complete Software Development Lifecycle workflow. Guide the user through each phase systematically, leveraging plugins, skills, and subagents.

## SDLC Phases

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                              SDLC WORKFLOW                                        │
├─────────┬─────────┬─────────┬─────────┬─────────┬───────────┬────────────────────┤
│ 1.SPEC  │ 2.TEST  │ 3.CODE  │ 4.BUILD │5.SECURE │  6.DOCS   │     7.VERIFY       │
│ ────────│─────────│─────────│─────────│─────────│───────────│────────────────────│
│ Plugin: │ Plugin: │ Plugin: │ Plugin: │ Plugin: │ Plugin:   │ Plugin:            │
│ spec-   │ test-   │ code-   │ builder │security-│ docs-     │ deploy-            │
│ writer  │ writer  │ implmtr │         │ checker │ generator │ verifier           │
│         │         │         │         │         │           │                    │
│ MCP:    │ Agent:  │ Agent:  │ Tools:  │ Agent:  │ Agent:    │ Tools:             │
│ spec-   │ test-   │ implmnt-│ bash    │security-│ documntn- │ curl, scripts      │
│ workflow│ engineer│ agent   │ linters │ auditor │ generator │ + rollback         │
└─────────┴─────────┴─────────┴─────────┴─────────┴───────────┴────────────────────┘
                                                        │              │
                                                     Deploy ──────► Verify
                                                                   (or rollback)
```

## Workflow Execution

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

### Phase 5: Security Audit (security-checker plugin)

**Goal**: Catch security vulnerabilities before deployment.

1. **Dependency Scan**
   ```bash
   npm audit --audit-level=high
   govulncheck ./...
   ```

2. **Secrets Detection**
   ```bash
   gitleaks detect --source .
   ```

3. **SAST Scan**
   ```bash
   semgrep --config=auto .
   ```

4. **Infrastructure Scan** (if applicable)
   ```bash
   checkov -d infrastructure/
   ```

**Agent**: Spawn `security-auditor` subagent for deep analysis.

**Quality Gates**:
- 0 critical/high vulnerabilities
- 0 hardcoded secrets
- 0 SAST critical findings

---

### Phase 6: Documentation (docs-generator plugin)

**Goal**: Generate comprehensive documentation.

1. **API Documentation**
   - Generate/update OpenAPI spec
   - Create endpoint documentation

2. **Code Documentation**
   - Add TSDoc/GoDoc comments
   - Document public APIs

3. **CLAUDE.md Files**
   - Create directory documentation
   - Document new functions/exports

4. **CHANGELOG Update**
   - Add entry for the feature

**Agent**: Spawn `documentation-generator` subagent.

**Artifacts**: `docs/openapi.yaml`, `CLAUDE.md`, `CHANGELOG.md`

---

### Phase 7: Post-Deployment Verification (deploy-verifier plugin)

**Goal**: Verify API Gateway + Lambda deployments work correctly; rollback on failure.

**Trigger**: After successful deployment to an environment (dev/staging/prod).

1. **Health Check**
   ```bash
   curl -f ${API_BASE_URL}/health
   ```

2. **Contract Validation**
   - Reuse TDD test expectations from Phase 2
   - Validate response schemas match OpenAPI spec
   - Test critical API paths

3. **Smoke Tests**
   ```bash
   npm run verify:deployment
   # or go run cmd/verify/main.go
   ```

4. **Rollback on Failure**
   - Automatic Lambda alias rollback to previous version
   - Notify team via configured email
   - Create incident issue in GitHub

**Configuration**: `verify.config.json` in service root

**Quality Gates**:
- Health endpoint responds 200 within 60s
- All smoke tests pass
- Response schemas match OpenAPI spec

**On Failure**:
- Rollback to previous version
- Pipeline marked as failed
- Incident notification sent

---

## Orchestration Commands

When user invokes `/sdlc`:

1. **Ask which phase to start from** (or start fresh)
2. **Execute phases sequentially**
3. **Report status after each phase**
4. **Handle failures with guidance to fix and retry**

## Phase Transitions

```
spec-writer ──[approval]──> test-writer ──[tests written]──> code-implementer
                                                                    │
                                                                    ▼
docs-generator <──[security passed]── security-checker <──[build passed]── builder
      │
      ▼
   Deploy ──────> deploy-verifier ──[passed]──> ✅ Complete
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
- "Security scan" → Load security-checker plugin
- "Generate docs" → Load docs-generator plugin
- "Verify deployment" → Load deploy-verifier plugin

## Status Tracking

Use TodoWrite to track progress:

```
[ ] Phase 1: Specification
[ ] Phase 2: Testing (TDD)
[ ] Phase 3: Implementation
[ ] Phase 4: Build Verification
[ ] Phase 5: Security Audit
[ ] Phase 6: Documentation
[ ] Deploy to environment
[ ] Phase 7: Post-Deployment Verification
```

## Begin Workflow

Ask the user:
1. What feature are we building?
2. Is there an existing spec or starting fresh?
3. Which phase should we begin with?

Then proceed through the SDLC phases, providing guidance and spawning appropriate subagents as needed.
