# Review Hooks Setup Guide (Kiro IDE)

This guide shows you how to configure manual review hooks in Kiro IDE to emulate PR-level reviews after task or spec completion.

## Why Manual Review Hooks?

Since Kiro IDE doesn't support automatic task-completion hooks yet, we use **manual trigger hooks** to run comprehensive reviews at key milestones:

- ✅ After completing a task (task-level review)
- ✅ After completing a spec (spec-level review)
- ✅ Before merging branches

---

## Hook 1: Task Review (After Task Completion)

### Setup in Agent Hooks Panel

1. **Open Kiro IDE** → Navigate to **Agent Hooks** panel
2. Click **+ Add Hook**
3. Configure as follows:

**Hook Configuration:**

```
Name: Task Review (PR Emulation)

Description:
Perform a comprehensive PR-level review after completing a task.

Review Process:
1. Identify changed files since task started
2. Run quality checks (lint, type check, tests, coverage)
3. Review code quality (naming, structure, duplication)
4. Check security (no secrets, input validation, auth)
5. Verify testing (coverage, edge cases, integration)
6. Generate approval report

Steps:
- Run: git diff --stat HEAD~3..HEAD
- Run: ruff check src/ tests/
- Run: mypy src/
- Run: pytest --cov=src --cov-report=term-missing --cov-fail-under=80
- Run: bandit -r src/
- Review changed files for:
  • Code quality (naming, SRP, no duplication)
  • Security (no hardcoded secrets, input validation)
  • Performance (efficient algorithms, resource cleanup)
  • Testing (coverage, meaningful assertions)

Generate a review report with:
- Files changed summary
- Quality check results (✅ or ❌)
- Code quality rating (1-5)
- Critical issues (must fix before merge)
- Suggestions (nice to have)
- Approval status: APPROVED | CHANGES REQUESTED | BLOCKED

End with: "Ready to merge to group branch?" or list required fixes.

Trigger: Manual
File Pattern: (leave empty)
```

### When to Use

**After marking a task as completed:**
```
1. Mark task as "completed" in TodoWrite
2. Open Agent Hooks panel
3. Click ▷ next to "Task Review (PR Emulation)"
4. Review the generated report
5. If APPROVED: merge to group branch
6. If CHANGES REQUESTED: fix issues and review again
```

---

## Hook 2: Spec Review (After All Tasks Complete)

### Setup in Agent Hooks Panel

1. **Open Kiro IDE** → Navigate to **Agent Hooks** panel
2. Click **+ Add Hook**
3. Configure as follows:

**Hook Configuration:**

```
Name: Spec Review (Full Validation)

Description:
Comprehensive review after all tasks in a spec are completed.
This validates the entire feature before creating a PR to main.

Review Process:
1. Verify all spec tasks are completed
2. Run full test suite with coverage
3. Run security scan on entire codebase
4. Review all changes since spec started
5. Validate API contracts (OpenAPI if applicable)
6. Check documentation completeness
7. Perform integration testing

Steps:
- Use spec-workflow MCP to check spec status
- Run: git diff --stat main..HEAD
- Run: make build (or equivalent: lint + type check + tests)
- Run: make quality-gate (or: bandit + coverage report)
- Check: All spec tasks marked as completed
- Check: CHANGELOG.md updated
- Check: API documentation updated
- Check: Integration tests passing
- Check: No critical/high security vulnerabilities

Generate a spec review report with:
- Spec completion status
- Total files changed / lines added / lines removed
- Quality gate results (✅ or ❌)
- Test coverage % (must be 80%+)
- Security scan results (0 critical/high)
- Documentation status
- Integration test results
- Overall approval: READY FOR PR | NEEDS WORK | BLOCKED

If READY FOR PR:
- Suggest creating PR to main branch
- Provide PR description template

If NEEDS WORK:
- List specific issues to address
- Prioritize critical vs. nice-to-have fixes

Trigger: Manual
File Pattern: (leave empty)
```

### When to Use

**After all tasks in a spec are completed:**
```
1. Verify all tasks marked "completed" in spec
2. Open Agent Hooks panel
3. Click ▷ next to "Spec Review (Full Validation)"
4. Review the comprehensive report
5. If READY FOR PR: create PR to main
6. If NEEDS WORK: address issues and review again
```

---

## Hook 3: Quick Quality Check (Anytime)

For faster checks during development:

### Setup in Agent Hooks Panel

**Hook Configuration:**

```
Name: Quick Quality Check

Description:
Fast quality check without full review.
Use during development for quick feedback.

Steps:
- Run: ruff check src/ tests/
- Run: mypy src/
- Run: pytest tests/ -x --tb=short
- Report: Pass/Fail for each check
- If any failed: show errors with suggestions

Trigger: Manual
File Pattern: (leave empty)
```

### When to Use

**During development for quick feedback:**
```
- After making changes to multiple files
- Before switching tasks
- When you want fast validation without full review
```

---

## Workflow Integration

### Task Completion Flow

```
1. Work on task → Implement code
2. Mark task as "completed" in TodoWrite
3. 🔍 Trigger "Task Review (PR Emulation)" hook
4. Review report → Fix issues if needed
5. If APPROVED → Merge to group branch
6. Start next task
```

### Spec Completion Flow

```
1. Complete all tasks in spec
2. 🔍 Trigger "Spec Review (Full Validation)" hook
3. Review comprehensive report
4. If READY FOR PR → Create PR to main
5. If NEEDS WORK → Fix and review again
```

### Development Flow (Quick Checks)

```
1. Make changes
2. 🔍 Trigger "Quick Quality Check" hook
3. Get fast feedback
4. Continue development
```

---

## Quality Gates Reference

### Task-Level Gates

| Check | Tool | Threshold |
|-------|------|-----------|
| Lint | ruff | 0 errors |
| Type Check | mypy | 0 errors |
| Tests | pytest | All passing |
| Coverage | pytest-cov | 80%+ |
| Security | bandit | 0 critical/high |

### Spec-Level Gates

| Check | Tool | Threshold |
|-------|------|-----------|
| Full Build | make build | Success |
| Security Scan | bandit | 0 critical/high |
| Integration Tests | pytest integration/ | All passing |
| Coverage | pytest-cov | 80%+ |
| Documentation | Manual review | Complete |
| CHANGELOG | Manual check | Updated |

---

## Tips for Effective Reviews

### 1. Review Small Batches
- Review after each task (small changes)
- Easier to spot issues than reviewing entire spec at once

### 2. Use Checklists
- The hooks provide structured checklists
- Don't skip items even if they seem minor

### 3. Run Checks Locally
- Don't rely only on the hooks
- Run `make build` yourself to see full output

### 4. Document Findings
- If you find issues, document them clearly
- Use the generated report format

### 5. Be Consistent
- Always trigger reviews at the same milestones
- Don't merge without review approval

---

## Troubleshooting

### Hook Not Running

**Problem:** Hook doesn't execute when clicked
**Solution:**
1. Check hook is enabled (eye icon visible)
2. Verify Kiro Output panel for errors
3. Try disabling/re-enabling the hook

### Hook Runs But No Output

**Problem:** Hook runs but shows no results
**Solution:**
1. Check the instructions are clear and actionable
2. Ensure commands use full paths
3. Add explicit "output results" instruction

### Quality Checks Fail

**Problem:** Lint/tests fail during review
**Solution:**
1. This is expected! The review catches issues
2. Fix the reported issues
3. Re-run the hook to verify fixes

### Review Too Slow

**Problem:** Full spec review takes too long
**Solution:**
1. Use "Quick Quality Check" during development
2. Save "Spec Review" for final validation only
3. Consider reviewing after each task group instead

---

## Example Review Report

```markdown
# Task Review Report

**Task**: 3.2 - Implement user API endpoints
**Branch**: task-3.2/user-endpoints
**Files Changed**: 4 | **Lines Added**: 156 | **Lines Removed**: 12

## Quality Checks

✅ Lint: 0 errors (ruff check)
✅ Type Check: 0 errors (mypy)
✅ Tests: 23/23 passing (pytest)
✅ Coverage: 87% (target: 80%+)
✅ Security: 0 critical/high vulnerabilities (bandit)

## Code Quality Review

**Rating: 4/5** - Well-structured with minor improvements

**Strengths:**
- Clear function names and docstrings
- Good error handling patterns
- Comprehensive test coverage

**Findings:**

1. **[SUGGESTION]** `src/api/user_endpoints.py:45`
   - Consider extracting validation logic to separate function
   - Current function is 28 lines (target: <20)

2. **[INFO]** `tests/integration/test_user_api.py:67`
   - Edge case for empty user list could be tested
   - Not blocking, but would improve coverage

## Security Review

✅ No hardcoded secrets
✅ Input validation present on all endpoints
✅ Authentication checks in place
✅ SQL injection protection via ORM

## Approval Status

**✅ APPROVED - Ready to merge to group branch**

## Next Steps

```bash
git checkout group-3/user-management
git merge task-3.2/user-endpoints
git branch -d task-3.2/user-endpoints
```

Optional improvements for future:
- Refactor validation logic (task 3.2)
- Add edge case tests
```

---

## Summary

1. **Set up 3 manual hooks** in Agent Hooks panel:
   - Task Review (after each task)
   - Spec Review (after full spec)
   - Quick Quality Check (during development)

2. **Trigger hooks manually** at key milestones:
   - After marking tasks as "completed"
   - Before merging branches
   - Before creating PRs

3. **Follow the review reports**:
   - Fix critical issues immediately
   - Document suggestions for future
   - Only merge when APPROVED

4. **Integrate with SDLC workflow**:
   - Reviews are checkpoints between phases
   - Emulate PR-level quality without actual PRs
   - Maintain high code quality throughout
