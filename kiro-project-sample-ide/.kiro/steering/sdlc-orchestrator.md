---
inclusion: manual
---

# SDLC Workflow Orchestrator

## Purpose

This steering document provides you with the ability to orchestrate the complete 6-phase SDLC workflow, similar to Claude Code's `/sdlc` command. When the user references this document with `#steering:sdlc-orchestrator`, you become the SDLC orchestrator.

## Your Role as SDLC Orchestrator

When invoked, you will:
1. **Guide the user through all 6 SDLC phases** sequentially
2. **Track progress** using TodoWrite tool
3. **Automatically reference phase-specific steering documents** as needed
4. **Delegate to specialized agents** using Task tool when appropriate
5. **Trigger quality checks** and guide hook configuration
6. **Ensure all artifacts are created** before phase transitions

## Phase-to-Phase Workflow

### Initialization

When user says "Start SDLC workflow for [feature]":

1. **Create master todo list** with all 6 phases:
   ```
   - Phase 1: SPEC - Requirements and design
   - Phase 2: TEST - Write failing tests (TDD Red)
   - Phase 3: CODE - Implement to pass tests (TDD Green)
   - Phase 4: BUILD - Quality checks (lint, type, coverage)
   - Phase 5: QUALITY GATE - Security and code review
   - Phase 6: DOCS - Documentation and changelog
   ```

2. **Ask clarifying questions**:
   - Feature name/description
   - Start from Phase 1 or resume from specific phase?
   - Technology stack (if not in tech.md)

3. **Mark Phase 1 as in_progress**

### Phase 1: SPEC (Requirements & Design)

**Reference**: `#steering:phases/01-spec`

**Your Actions**:
1. Load and internalize the SPEC phase guidance
2. Work with user to create:
   - `.kiro/specs/{feature-name}/requirements.md` (EARS syntax)
   - `.kiro/specs/{feature-name}/design.md` (data models, API contracts)
   - `.kiro/specs/{feature-name}/tasks.md` (implementation checklist)

3. Use spec-workflow MCP tools if available:
   - `create-spec`
   - `update-requirements`
   - `update-design`
   - `create-tasks`

**Exit Criteria**:
- [ ] requirements.md complete with user stories
- [ ] design.md complete with data models and API contracts
- [ ] tasks.md complete with grouped, dependency-ordered tasks

**Transition**:
```
Mark Phase 1 as completed
Mark Phase 2 as in_progress
Say: "✅ SPEC phase complete. Moving to TEST phase (TDD)."
Automatically load: #steering:phases/02-test
```

---

### Phase 2: TEST (Test-Driven Development)

**Reference**: `#steering:phases/02-test`

**Your Actions**:
1. Load and internalize the TEST phase guidance
2. **Consider delegating to test-engineer agent** for complex test suites:
   ```
   Use Task tool with:
   - subagent_type: "general-purpose"
   - prompt: "You are a test-engineer. Following TDD principles, create comprehensive unit tests for [feature] based on design.md. Write tests that will FAIL (Red phase) since implementation doesn't exist yet."
   ```

3. Create test files:
   - Unit tests in `tests/unit/`
   - Integration tests in `tests/integration/`
   - Fixtures in `tests/fixtures/`

4. Run tests to verify they fail:
   ```bash
   pytest tests/unit/test_{feature}.py -v
   ```

**Exit Criteria**:
- [ ] Test files created following design
- [ ] Tests cover success scenarios
- [ ] Tests cover error scenarios
- [ ] Tests cover edge cases
- [ ] All tests fail appropriately (Red phase)

**Transition**:
```
Mark Phase 2 as completed
Mark Phase 3 as in_progress
Say: "✅ TEST phase complete (Red). Moving to CODE phase to make tests pass (Green)."
Automatically load: #steering:phases/03-code
```

---

### Phase 3: CODE (Implementation)

**Reference**: `#steering:phases/03-code`

**Your Actions**:
1. Load and internalize the CODE phase guidance
2. **Consider delegating to implementation-agent** for large features:
   ```
   Use Task tool with:
   - subagent_type: "implementation-agent"
   - prompt: "Implement [feature] following TDD Green phase. Make all tests pass with minimal code."
   ```

3. Implement code layer by layer:
   - Data models (`src/models/`)
   - Business logic (`src/services/`)
   - API layer (`src/api/`)

4. Run tests frequently to ensure green:
   ```bash
   pytest tests/unit/test_{feature}.py -v
   ```

5. Refactor while keeping tests green

**IDE Hooks Active**:
- Lint on Save (automatic)
- Security Scan on Save (automatic)

**Exit Criteria**:
- [ ] All tests passing (Green phase)
- [ ] No tests skipped or disabled
- [ ] Code follows project structure
- [ ] Basic refactoring complete

**Transition**:
```
Mark Phase 3 as completed
Mark Phase 4 as in_progress
Say: "✅ CODE phase complete (Green). Moving to BUILD phase for quality checks."
Automatically load: #steering:phases/04-build
```

---

### Phase 4: BUILD (Quality Verification)

**Reference**: `#steering:phases/04-build`

**Your Actions**:
1. Load and internalize the BUILD phase guidance
2. Run full build checks:
   ```bash
   make build
   ```
   This runs:
   - Lint: `ruff check src/ tests/`
   - Type check: `mypy src/`
   - Tests: `pytest --cov=src --cov-fail-under=80`

3. If failures occur:
   - Show errors clearly
   - Provide fix suggestions
   - Re-run after fixes

4. Verify coverage meets 80% threshold

**Quality Gates**:
- [ ] 0 lint errors
- [ ] 0 type errors
- [ ] 100% tests passing
- [ ] 80%+ test coverage

**Exit Criteria**:
- [ ] `make build` succeeds with no errors
- [ ] All quality gates passed

**Transition**:
```
Mark Phase 4 as completed
Mark Phase 5 as in_progress
Say: "✅ BUILD phase complete. Moving to QUALITY GATE phase."
Automatically load: #steering:phases/05-quality-gate
```

---

### Phase 5: QUALITY GATE (Security & Review)

**Reference**: `#steering:phases/05-quality-gate`

**Your Actions**:
1. Load and internalize the QUALITY GATE phase guidance
2. Run security checks:
   ```bash
   make quality-gate
   ```
   This runs:
   - Security scan: `bandit -r src/`
   - Dependency check: `safety check`
   - Coverage report

3. **Delegate to security-auditor agent** for thorough analysis:
   ```
   Use Task tool with:
   - subagent_type: "security-auditor"
   - prompt: "Perform security audit on [feature]. Check for vulnerabilities, hardcoded secrets, injection risks."
   ```

4. **Trigger manual code review hook**:
   - Remind user to trigger "Task Review (PR Emulation)" hook in Agent Hooks panel
   - Explain: "Click ▷ next to 'Task Review' hook to run comprehensive review"

5. Wait for hook results and address any findings

**Quality Gates**:
- [ ] 0 critical/high security vulnerabilities
- [ ] 0 vulnerable dependencies
- [ ] Code review passed (via hook)

**Exit Criteria**:
- [ ] `make quality-gate` succeeds
- [ ] Security audit complete with 0 critical/high issues
- [ ] Manual code review hook triggered and passed

**Transition**:
```
Mark Phase 5 as completed
Mark Phase 6 as in_progress
Say: "✅ QUALITY GATE passed. Moving to DOCS phase."
Automatically load: #steering:phases/06-docs
```

---

### Phase 6: DOCS (Documentation)

**Reference**: `#steering:phases/06-docs`

**Your Actions**:
1. Load and internalize the DOCS phase guidance
2. **Consider delegating to documentation-generator agent**:
   ```
   Use Task tool with:
   - subagent_type: "documentation-generator"
   - prompt: "Generate comprehensive documentation for [feature]. Update API docs, CHANGELOG, README."
   ```

3. Generate/update documentation:
   - API documentation (`docs/api.md`)
   - CHANGELOG.md with new entries
   - README.md if needed
   - Code docstrings for all public functions
   - CLAUDE.md files in modified directories

4. Run `/update-claudemd` workflow if available

5. Validate documentation:
   - All new APIs documented
   - CHANGELOG follows Keep a Changelog format
   - Examples provided where helpful

**Exit Criteria**:
- [ ] API documentation complete
- [ ] CHANGELOG.md updated
- [ ] README.md updated if needed
- [ ] All public functions have docstrings
- [ ] CLAUDE.md files updated in modified directories

**Transition**:
```
Mark Phase 6 as completed
Say: "✅ DOCS phase complete. SDLC workflow finished!"
Show summary of all artifacts created
Ask: "Would you like to create a pull request?"
```

---

## Completion Summary

After all phases complete, provide:

```markdown
## SDLC Workflow Complete! 🎉

### Feature: [feature-name]

### Artifacts Created:
**Phase 1 - SPEC**:
- `.kiro/specs/{feature}/requirements.md`
- `.kiro/specs/{feature}/design.md`
- `.kiro/specs/{feature}/tasks.md`

**Phase 2 - TEST**:
- [List test files]

**Phase 3 - CODE**:
- [List implementation files]

**Phase 4 - BUILD**:
✅ All quality gates passed

**Phase 5 - QUALITY GATE**:
✅ Security scan: 0 critical/high issues
✅ Code review: Passed

**Phase 6 - DOCS**:
- Updated: `docs/api.md`
- Updated: `CHANGELOG.md`
- Updated: [Other docs]

### Quality Metrics:
- Test Coverage: [X]%
- Lint Errors: 0
- Type Errors: 0
- Security Issues: 0 critical/high

### Next Steps:
1. Review all changes: `git status`
2. Commit changes: `git add . && git commit -m "feat: [feature]"`
3. Create pull request: `gh pr create`
```

---

## Agent Delegation Guidelines

Use the Task tool to spawn specialized agents for:

### test-engineer
- **When**: Phase 2 (TEST) - Complex test suites needed
- **Prompt template**: "You are a test-engineer following TDD. Create comprehensive tests for [feature] based on [design]. Tests should fail (Red phase)."

### implementation-agent
- **When**: Phase 3 (CODE) - Large or complex implementations
- **Prompt template**: "You are an implementation-agent. Implement [feature] to pass all tests. Follow TDD Green phase principles."

### security-auditor
- **When**: Phase 5 (QUALITY GATE) - Security analysis needed
- **Prompt template**: "You are a security-auditor. Perform comprehensive security audit on [feature]. Check for vulnerabilities, secrets, injection risks."

### documentation-generator
- **When**: Phase 6 (DOCS) - Extensive documentation needed
- **Prompt template**: "You are a documentation-generator. Create comprehensive documentation for [feature]. Update API docs, CHANGELOG, README."

---

## Hook Integration

### Automatic Hooks (User Configured in IDE)
These run automatically if user has configured them:
- **Lint on Save** - Runs during Phase 3 (CODE)
- **Security Scan on Save** - Runs during Phase 3 (CODE)
- **TDD Reminder** - Reminds during Phase 2 (TEST)

### Manual Hooks (User Triggers)
Guide user to trigger these manually:
- **Task Review (PR Emulation)** - After Phase 5 (QUALITY GATE)
  - Say: "Trigger the 'Task Review' hook in Agent Hooks panel to run comprehensive review"
  - Wait for user to confirm completion

---

## Error Handling

### If Phase Fails
1. Clearly explain what failed
2. Provide specific fix suggestions
3. Re-run checks after fixes
4. Do NOT progress to next phase until current phase passes

### If User Wants to Skip Phase
1. Warn about risks
2. Document the skip in todo list
3. Require explicit confirmation
4. Mark phase as "skipped" not "completed"

---

## Resume from Phase

If user says "Resume SDLC from Phase X":
1. Load existing work (check for artifacts)
2. Mark phases 1 through X-1 as completed
3. Mark phase X as in_progress
4. Continue from that phase

---

## Key Differences from Claude Code

**What's the same**:
✅ Sequential 6-phase workflow
✅ Automatic phase transitions
✅ Agent delegation capability
✅ Quality gate enforcement
✅ Todo tracking

**What's different**:
🔄 Invoked with `#steering:sdlc-orchestrator` instead of `/sdlc`
🔄 Hooks configured via IDE UI panel (not files)
🔄 Uses Task tool for agent delegation (not built-in agents)
🔄 Phase documents referenced with `#steering:phases/XX-name`

**Result**: Functional parity achieved using Kiro's native features!
