# Kiro Hooks Configuration

This document describes the hooks configured for the SDLC workflow automation.

## Overview

Hooks are automated triggers that execute predefined actions when specific events occur in the IDE. They implement the "hybrid automation" strategy for quality gates.

## Configured Hooks

### 1. Lint on Save

**Trigger:** File Save
**File Pattern:** `**/*.py`

**Description:**
Automatically runs `ruff check` on Python files when saved. Provides immediate feedback on code style and potential issues.

**Kiro Hook Setup:**
1. Open Kiro panel → Agent Hooks → Click `+`
2. Enter description:
   ```
   When a Python file is saved, run ruff check on the file.
   If there are lint errors, display them with suggestions for fixing.
   Do not auto-fix unless the user explicitly requests it.
   ```
3. Set trigger: File Save
4. Set pattern: `**/*.py`

**Expected Behavior:**
- On save, lint check runs automatically
- Errors displayed in Problems panel
- Suggestions provided inline

---

### 2. Security Scan on Save

**Trigger:** File Save
**File Pattern:** `src/**/*.py`

**Description:**
Runs `bandit` security analysis on source files when saved. Detects common security issues like hardcoded secrets, injection vulnerabilities, etc.

**Kiro Hook Setup:**
1. Open Kiro panel → Agent Hooks → Click `+`
2. Enter description:
   ```
   When a Python source file in src/ is saved, run bandit security scan.
   Report any findings with severity level (LOW, MEDIUM, HIGH, CRITICAL).
   For HIGH or CRITICAL findings, provide immediate remediation suggestions.
   ```
3. Set trigger: File Save
4. Set pattern: `src/**/*.py`

**Expected Behavior:**
- Security scan runs on source file save
- Findings categorized by severity
- Critical issues highlighted prominently

---

### 3. TDD Reminder on File Create

**Trigger:** File Create
**File Pattern:** `src/**/*.py`

**Description:**
Reminds developers to follow TDD when creating new source files. Suggests creating tests first.

**Kiro Hook Setup:**
1. Open Kiro panel → Agent Hooks → Click `+`
2. Enter description:
   ```
   When a new Python file is created in src/, remind the user:
   "Following TDD: Consider writing tests for this module first in tests/unit/"
   Suggest the corresponding test file path based on the source file location.
   Example: src/services/new_service.py → tests/unit/test_new_service.py
   ```
3. Set trigger: File Create
4. Set pattern: `src/**/*.py`

**Expected Behavior:**
- Notification appears when new source file created
- Suggests test file location
- Links to TDD workflow steering document

---

### 4. Code Review (Manual Trigger)

**Trigger:** Manual
**File Pattern:** N/A

**Description:**
Runs a comprehensive code review checklist on demand. Used during the Quality Gate phase.

**Kiro Hook Setup:**
1. Open Kiro panel → Agent Hooks → Click `+`
2. Enter description:
   ```
   Perform a comprehensive code review on the current file or selected files:

   Code Quality:
   - Check naming conventions (clear, descriptive)
   - Verify single responsibility principle
   - Identify code duplication
   - Check function length (< 20 lines preferred)
   - Review error handling patterns

   Security:
   - Check for input validation
   - Verify no hardcoded secrets
   - Review authentication/authorization
   - Check for injection vulnerabilities

   Performance:
   - Identify inefficient algorithms
   - Check for resource cleanup
   - Review caching opportunities

   Testing:
   - Verify test coverage exists
   - Check test quality (meaningful assertions)
   - Review edge case coverage

   Provide a summary with:
   - Overall rating (1-5)
   - Critical issues (must fix)
   - Suggestions (nice to have)
   ```
3. Set trigger: Manual
4. No file pattern needed

**Expected Behavior:**
- User manually triggers via play button
- Comprehensive review runs
- Summary with actionable feedback provided

---

## Hook Management

### Enable/Disable Hooks

Toggle hooks without deleting:
- Click eye icon next to hook name in Agent Hooks panel
- Or toggle "Hook Enabled" switch in hook view

### Edit Hooks

1. Select hook in Agent Hooks panel
2. Modify trigger, pattern, or instructions
3. Changes apply immediately

### Delete Hooks

1. Select hook in Agent Hooks panel
2. Click "Delete Hook" at bottom
3. Confirm deletion (permanent)

### Run Manual Hooks

- Click play button (▷) next to hook name
- Or select hook and click "Start Hook"

## Integration with SDLC Phases

| Hook | SDLC Phase | Purpose |
|------|------------|---------|
| Lint on Save | Phase 4: BUILD | Continuous quality feedback |
| Security Scan | Phase 5: QUALITY GATE | Automated vulnerability detection |
| TDD Reminder | Phase 2: TEST | Enforce test-first development |
| Code Review | Phase 5: QUALITY GATE | Manual quality assessment |

## Troubleshooting

### Hook Not Triggering

1. Check hook is enabled (eye icon visible)
2. Verify file pattern matches saved file
3. Check Kiro Output panel for errors

### Slow Performance

1. Consider narrowing file patterns
2. Disable verbose hooks during heavy coding
3. Use manual triggers for expensive operations

### Conflicting Hooks

- Hooks run in order they were created
- For dependent operations, use manual triggers
- Consider combining related checks into single hook
