# Complete Hooks Setup for SDLC Parity

**Purpose**: Configure Kiro IDE hooks to replicate Claude Code's automated SDLC workflow

## Overview

This guide provides **exact instructions** for configuring all hooks needed to achieve SDLC parity between Claude Code and Kiro IDE.

## Quick Setup Checklist

- [ ] Hook 1: Lint on Save (auto quality check)
- [ ] Hook 2: Security Scan on Save (auto vulnerability detection)
- [ ] Hook 3: TDD Reminder on File Create (enforce test-first)
- [ ] Hook 4: Task Review - PR Emulation (manual, comprehensive review)
- [ ] Hook 5: Spec Review - Full Validation (manual, pre-PR check)
- [ ] Hook 6: SDLC Phase Transition (manual, orchestration helper)

---

## Hook 1: Lint on Save

### Configuration

**Open**: Kiro IDE → Agent Hooks Panel → Click `+`

| Field | Value |
|-------|-------|
| **Name** | Lint on Save |
| **Trigger** | File Save |
| **File Pattern** | `**/*.py` |
| **Enabled** | ✅ Yes |

**Instructions**:
```
When a Python file is saved:

1. Run ruff check on the saved file:
   - Command: ruff check {file_path}

2. If lint errors found:
   - Display errors with line numbers
   - Provide auto-fix suggestions
   - Show: "Run 'ruff check --fix {file}' to auto-fix"

3. If no errors:
   - Silent success (no notification)

Do NOT auto-fix unless user explicitly requests it.
```

---

## Hook 2: Security Scan on Save

### Configuration

**Open**: Kiro IDE → Agent Hooks Panel → Click `+`

| Field | Value |
|-------|-------|
| **Name** | Security Scan on Save |
| **Trigger** | File Save |
| **File Pattern** | `src/**/*.py` |
| **Enabled** | ✅ Yes |

**Instructions**:
```
When a Python source file in src/ is saved:

1. Run bandit security scan:
   - Command: bandit {file_path} -f txt

2. Categorize findings by severity:
   - CRITICAL: Show immediately with 🔴
   - HIGH: Show with 🟠
   - MEDIUM: Show with 🟡
   - LOW: Log only (no notification)

3. For CRITICAL or HIGH findings:
   - Display vulnerability details
   - Provide remediation suggestions
   - Reference: OWASP guidelines if applicable

4. If no critical/high issues:
   - Silent success
```

---

## Hook 3: TDD Reminder on File Create

### Configuration

**Open**: Kiro IDE → Agent Hooks Panel → Click `+`

| Field | Value |
|-------|-------|
| **Name** | TDD Reminder |
| **Trigger** | File Create |
| **File Pattern** | `src/**/*.py` |
| **Enabled** | ✅ Yes |

**Instructions**:
```
When a new Python file is created in src/:

1. Determine corresponding test file path:
   - If: src/models/user.py → tests/unit/test_user.py
   - If: src/services/auth_service.py → tests/unit/test_auth_service.py
   - If: src/api/user_api.py → tests/integration/test_user_api.py

2. Check if test file exists:
   - If exists: ✅ "Test file found: {test_path}"
   - If NOT exists: 💡 Reminder message

3. Show TDD reminder:
   "📝 TDD Reminder: Consider creating {test_path} first!

   Following TDD (Test-Driven Development):
   1. Write failing tests first (Red)
   2. Implement to pass tests (Green)
   3. Refactor while keeping tests green

   Reference: #steering:sdlc-workflow for TDD guidance"

4. Offer to create test file:
   "Would you like me to create the test file skeleton?"
```

---

## Hook 4: Task Review (PR Emulation)

### Configuration

**Open**: Kiro IDE → Agent Hooks Panel → Click `+`

| Field | Value |
|-------|-------|
| **Name** | Task Review (PR Emulation) |
| **Trigger** | Manual |
| **File Pattern** | (leave empty) |
| **Enabled** | ✅ Yes |

**Instructions**:
```
Perform a comprehensive PR-level review after completing a task.

## Review Process

### 1. Identify Changed Files
Run: git diff --stat HEAD~3..HEAD
Show: Files changed, lines added/removed

### 2. Run Quality Checks
Execute all checks and report results:
- Lint: ruff check src/ tests/
- Type: mypy src/
- Tests: pytest --cov=src --cov-report=term-missing --cov-fail-under=80
- Security: bandit -r src/

### 3. Review Changed Files
For each changed file, check:

**Code Quality**:
- Naming: Clear, descriptive names?
- Single Responsibility: Each function does one thing?
- DRY: No duplicated code?
- Complexity: Functions < 20 lines, cyclomatic complexity < 10?
- Error Handling: Appropriate exceptions, no bare except?

**Security**:
- Input Validation: All external input validated?
- No Secrets: No hardcoded passwords, API keys, tokens?
- SQL Safety: Parameterized queries (if applicable)?
- Path Safety: No path traversal vulnerabilities?

**Performance**:
- Algorithm Efficiency: No O(n²) where O(n) possible?
- Resource Cleanup: Files/connections properly closed?
- Caching: Appropriate caching for expensive operations?

**Testing**:
- Coverage: 80%+ line coverage?
- Edge Cases: Boundary conditions tested?
- Error Cases: Exception paths tested?
- Meaningful Assertions: Tests verify behavior, not implementation?

### 4. Generate Review Report

Format:
```markdown
# Task Review Report

**Task**: [Infer from changed files]
**Files Changed**: X | **Lines Added**: Y | **Lines Removed**: Z

## Quality Checks

✅/❌ Lint: [result]
✅/❌ Type Check: [result]
✅/❌ Tests: [result]
✅/❌ Coverage: [percentage]
✅/❌ Security: [result]

## Code Quality Review

**Rating: X/5** - [Brief assessment]

**Strengths**:
- [List strengths]

**Findings**:

1. **[CRITICAL/MAJOR/MINOR]** `file:line`
   - [Issue description]
   - [Suggested fix]

## Security Review

✅/❌ [Security checklist results]

## Approval Status

**[APPROVED | CHANGES REQUESTED | BLOCKED]**

## Next Steps

[Either: "Ready to merge" or "Fix issues: [list]"]
```

Be thorough but constructive. Prioritize critical issues.
```

---

## Hook 5: Spec Review (Full Validation)

### Configuration

**Open**: Kiro IDE → Agent Hooks Panel → Click `+`

| Field | Value |
|-------|-------|
| **Name** | Spec Review (Full Validation) |
| **Trigger** | Manual |
| **File Pattern** | (leave empty) |
| **Enabled** | ✅ Yes |

**Instructions**:
```
Comprehensive review after all tasks in a spec are completed.
Validates entire feature before creating PR to main.

## Review Process

### 1. Verify Spec Completion
- Check .kiro/specs/{spec-name}/tasks.md
- Confirm all tasks marked as completed
- List any incomplete tasks

### 2. Run Full Build
Execute: make build
Report: Lint, type check, tests, coverage results

### 3. Run Quality Gate
Execute: make quality-gate
Report: Security scan, dependency check results

### 4. Review All Changes Since Spec Started
Run: git diff --stat main..HEAD
Show: Total files changed, lines added/removed

### 5. Validate API Contracts (if applicable)
- Check if API documentation exists
- Verify all endpoints documented
- Validate request/response examples

### 6. Check Documentation Completeness
Verify:
- [ ] CHANGELOG.md updated
- [ ] API documentation updated (docs/api.md)
- [ ] README.md updated if needed
- [ ] CLAUDE.md files updated in modified directories
- [ ] All public functions have docstrings

### 7. Integration Test Validation
Run: pytest tests/integration/ -v
Report: Integration test results

### 8. Generate Spec Review Report

Format:
```markdown
# Spec Review Report

**Spec**: [spec-name]
**Branch**: [current branch]

## Spec Completion Status

✅/❌ All tasks completed: X/Y tasks
[List any incomplete tasks]

## Quality Gate Results

**Build Status**:
✅/❌ Lint: 0 errors
✅/❌ Type Check: 0 errors
✅/❌ Tests: X/Y passing
✅/❌ Coverage: X% (threshold: 80%+)

**Security Status**:
✅/❌ Critical vulnerabilities: X
✅/❌ High vulnerabilities: X
✅/❌ Vulnerable dependencies: X

## Changes Summary

**Files Changed**: X
**Lines Added**: Y
**Lines Removed**: Z

## Documentation Status

✅/❌ CHANGELOG.md updated
✅/❌ API docs updated
✅/❌ README.md current
✅/❌ CLAUDE.md files updated

## Integration Tests

✅/❌ All integration tests passing

## Overall Assessment

**Status: [READY FOR PR | NEEDS WORK | BLOCKED]**

### If READY FOR PR:
```bash
# Create PR to main
gh pr create --base main --head [current-branch] --title "[title]" --body "[description]"
```

### If NEEDS WORK:
**Issues to address**:
1. [Issue 1]
2. [Issue 2]
...

**Priority**: [Critical issues first]
```

Provide comprehensive assessment for production readiness.
```

---

## Hook 6: SDLC Phase Transition Helper

### Configuration

**Open**: Kiro IDE → Agent Hooks Panel → Click `+`

| Field | Value |
|-------|-------|
| **Name** | SDLC Phase Transition |
| **Trigger** | Manual |
| **File Pattern** | (leave empty) |
| **Enabled** | ✅ Yes |

**Instructions**:
```
Help user transition between SDLC phases with validation and guidance.

When user triggers this hook:

1. **Detect Current Phase**:
   - Check TodoWrite for active phase
   - Or ask: "Which phase did you just complete?"

2. **Validate Phase Completion**:

**If Phase 1 (SPEC)**:
- Check files exist: requirements.md, design.md, tasks.md
- Verify they're not empty
- ✅ Ready to move to Phase 2 (TEST)

**If Phase 2 (TEST)**:
- Run: pytest tests/ --collect-only
- Verify: Test files exist
- Run tests to ensure they fail (Red phase)
- ✅ Ready to move to Phase 3 (CODE)

**If Phase 3 (CODE)**:
- Run: pytest tests/ -v
- Verify: All tests passing (Green phase)
- ✅ Ready to move to Phase 4 (BUILD)

**If Phase 4 (BUILD)**:
- Run: make build
- Verify: 0 lint errors, 0 type errors, 80%+ coverage
- ✅ Ready to move to Phase 5 (QUALITY GATE)

**If Phase 5 (QUALITY GATE)**:
- Run: make quality-gate
- Verify: 0 critical/high security issues
- Suggest: "Trigger 'Task Review' hook for PR emulation"
- ✅ Ready to move to Phase 6 (DOCS)

**If Phase 6 (DOCS)**:
- Check: CHANGELOG.md updated
- Check: API docs updated
- ✅ SDLC complete! Ready for PR

3. **Update Todo List**:
   - Mark current phase as completed
   - Mark next phase as in_progress

4. **Load Next Phase Guidance**:
   - Say: "Loading guidance for Phase X..."
   - Reference: #steering:phases/0X-[name].md

5. **Show Transition Summary**:
```markdown
✅ Phase [N] ([NAME]) complete!
🚀 Moving to Phase [N+1] ([NAME])

**Next Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Phase Guidance**: Loaded from #steering:phases/0[N+1]-[name].md
```
```

---

## Hook Priority & Order

Hooks execute in the order they're created. For optimal workflow:

1. **Create automatic hooks first** (Lint, Security, TDD Reminder)
2. **Then create manual hooks** (Task Review, Spec Review, Phase Transition)

## Testing Your Hooks

### Test Lint on Save
1. Open any `.py` file
2. Add a syntax error (e.g., missing colon)
3. Save file
4. **Expected**: Lint error displayed with suggestion

### Test Security Scan on Save
1. Open `src/` file
2. Add: `password = "hardcoded123"`
3. Save file
4. **Expected**: Security warning about hardcoded secret

### Test TDD Reminder
1. Create new file: `src/models/test_model.py`
2. **Expected**: Reminder to create `tests/unit/test_test_model.py` first

### Test Task Review
1. Make some code changes
2. Open Agent Hooks panel
3. Click ▷ next to "Task Review (PR Emulation)"
4. **Expected**: Comprehensive review report generated

### Test Spec Review
1. Complete a spec (all tasks done)
2. Open Agent Hooks panel
3. Click ▷ next to "Spec Review (Full Validation)"
4. **Expected**: Full validation report with PR readiness

### Test Phase Transition
1. Complete a phase (e.g., all tests passing)
2. Open Agent Hooks panel
3. Click ▷ next to "SDLC Phase Transition"
4. **Expected**: Validation passed, next phase guidance loaded

## Troubleshooting

### Hook Doesn't Run
- Check hook is enabled (eye icon should be visible)
- Verify file pattern matches (for automatic hooks)
- Check Kiro Output panel for errors

### Hook Runs But Shows No Output
- Check instructions are clear and use bash commands
- Ensure commands use full paths (not relative)
- Add explicit "output results" instruction

### Hook Runs Too Slowly
- Consider disabling verbose hooks during heavy development
- Use manual triggers for expensive operations
- Narrow file patterns to reduce trigger frequency

---

## Integration with SDLC Orchestrator

When using `#steering:sdlc-orchestrator`:

1. **Automatic hooks run in background** (Lint, Security, TDD)
2. **Orchestrator guides manual hook usage**:
   - "Trigger Task Review hook to validate this phase"
   - "Run Spec Review hook before creating PR"
3. **Phase Transition hook** can be triggered to help move between phases

---

## Summary

With all 6 hooks configured:

✅ **Automatic Quality**: Lint & security on every save
✅ **TDD Enforcement**: Reminders for test-first development
✅ **PR Emulation**: Comprehensive task reviews
✅ **Pre-PR Validation**: Full spec reviews
✅ **Phase Orchestration**: Guided phase transitions

**Result**: SDLC parity with Claude Code achieved using Kiro's native features!
