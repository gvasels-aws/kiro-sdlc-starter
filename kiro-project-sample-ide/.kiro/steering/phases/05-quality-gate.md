---
inclusion: manual
---

# Phase 5: Quality Gate (QUALITY GATE)

**Mode**: Hook + Chat (security scans automated, code review chat-driven)
**Prerequisite**: Phase 4 (BUILD) complete with all checks passing

## Purpose

Ensure code meets security and quality standards before documentation. This phase combines automated security scanning with manual code review.

## Components

| Component | Mode | Purpose |
|-----------|------|---------|
| Security Scan | Hook (on save) | Detect vulnerabilities |
| Dependency Check | Manual | Check for vulnerable packages |
| Code Review | Chat-driven | Quality and maintainability |

## Security Scanning

### Bandit (Static Analysis)

Runs automatically on file save for `src/**/*.py`:

```bash
bandit -r src/
```

Expected output:
```
Run started:2025-01-15 10:30:00
Test results:
        No issues identified.

Code scanned:
        Total lines of code: 150
        Total lines skipped (#nosec): 0
```

#### Common Issues

| Issue | Severity | Fix |
|-------|----------|-----|
| B101 | Low | Assert used (OK in tests) |
| B105 | High | Hardcoded password |
| B608 | High | SQL injection |
| B602 | High | Shell injection |

Example fix:
```python
# BAD: Hardcoded password
password = "secret123"

# GOOD: Environment variable
import os
password = os.environ.get("DB_PASSWORD")
```

### Safety (Dependency Check)

```bash
safety check -r requirements.txt
```

Expected output:
```
No known security vulnerabilities found.
```

If vulnerabilities found:
1. Update the vulnerable package
2. If no fix available, assess risk
3. Document in security notes

## Code Review Checklist

### Code Quality

- [ ] **Naming**: Clear, descriptive names for variables, functions, classes
- [ ] **Single Responsibility**: Each function does one thing
- [ ] **DRY**: No duplicated code
- [ ] **Complexity**: Functions < 20 lines, cyclomatic complexity < 10
- [ ] **Error Handling**: Appropriate exceptions, no bare `except:`

### Security

- [ ] **Input Validation**: All external input validated
- [ ] **No Secrets**: No hardcoded passwords, API keys, or tokens
- [ ] **SQL Safety**: Parameterized queries (if applicable)
- [ ] **Path Safety**: No path traversal vulnerabilities
- [ ] **Auth Checks**: Authorization verified before operations

### Performance

- [ ] **Algorithm Efficiency**: No O(n²) where O(n) possible
- [ ] **Resource Cleanup**: Files/connections properly closed
- [ ] **Caching**: Appropriate caching for expensive operations
- [ ] **N+1 Queries**: No database query loops (if applicable)

### Testing

- [ ] **Coverage**: 80%+ line coverage
- [ ] **Edge Cases**: Boundary conditions tested
- [ ] **Error Cases**: Exception paths tested
- [ ] **Meaningful Assertions**: Tests verify behavior, not implementation

### Documentation

- [ ] **Docstrings**: All public functions documented
- [ ] **Type Hints**: All function signatures typed
- [ ] **Comments**: Complex logic explained (sparingly)

## Workflow

### Step 1: Run Security Scan

```bash
bandit -r src/ -f txt
```

Fix any HIGH or CRITICAL findings before proceeding.

### Step 2: Check Dependencies

```bash
safety check -r requirements.txt
safety check -r requirements-dev.txt
```

Update vulnerable packages or document exceptions.

### Step 3: Code Review

Use chat to review code:
```
Review the UserService implementation for:
1. Security issues
2. Code quality
3. Performance concerns
4. Test coverage gaps
```

### Step 4: Document Findings

Create review notes if significant issues found:
```markdown
## Code Review Notes

### Security
- No issues found

### Quality
- Consider extracting email validation to utility module

### Performance
- List operations could use pagination cursor for large datasets
```

## Quality Gates

| Check | Threshold |
|-------|-----------|
| Critical vulnerabilities | 0 |
| High vulnerabilities | 0 |
| Hardcoded secrets | 0 |
| Code review | Passed |

## Failure Handling

### Security Findings

1. **Critical/High**: Must fix before proceeding
2. **Medium**: Should fix, document if deferring
3. **Low**: Optional, fix if simple

### Code Review Issues

1. **Blockers**: Must fix (security, correctness)
2. **Major**: Should fix (maintainability)
3. **Minor**: Nice to have (style)

Return to appropriate phase:
- Security issues → Phase 3 (CODE)
- Test gaps → Phase 2 (TEST)
- Design issues → Phase 1 (SPEC)

## Exit Criteria

Before moving to Phase 6 (DOCS):
- [ ] `bandit` reports 0 critical/high issues
- [ ] `safety` reports 0 vulnerable dependencies
- [ ] Code review checklist passed
- [ ] All findings addressed or documented
- [ ] **Task review triggered** (comprehensive validation)

## 🔍 Review Checkpoint

**After completing the QUALITY GATE phase:**

1. **Trigger "Task Review (PR Emulation)" manual hook**:
   - Open Agent Hooks panel
   - Find "Task Review (PR Emulation)"
   - Click ▷ (play button) to run
2. Review comprehensive report including:
   - Quality checks (lint, type check, tests, coverage)
   - Security scan results
   - Code quality assessment
   - Performance review
3. Address any findings
4. Only proceed to DOCS phase if APPROVED

**Quality Gate + Task Review = Double validation**
- Automated checks catch technical issues
- Manual review catches design/architecture issues
- Together they ensure production-ready code

See: `docs/REVIEW_HOOKS_SETUP.md` for hook configuration

## Chat Invocation

```
# Reference this phase
#steering:phases/05-quality-gate

# Run quality gate
"Run security scan and code review"
```
