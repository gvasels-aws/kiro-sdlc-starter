---
description: Perform a comprehensive code review of recent changes
---

# Code Review

Perform a comprehensive code review of the specified files or recent changes.

## Review Scope

If a path is provided, review those specific files/directories.
Otherwise, review recent uncommitted changes.

## Git Context

### Uncommitted Changes
!`git status --porcelain`

### Recent Diff
!`git diff --stat`

## Review Checklist

### Code Quality
- [ ] Clear, descriptive naming conventions
- [ ] Functions are single-purpose and appropriately sized
- [ ] No unnecessary code duplication
- [ ] Proper error handling implemented
- [ ] Code is self-documenting or has appropriate comments

### Security
- [ ] Input validation on all external data
- [ ] No hardcoded secrets or credentials
- [ ] Proper authentication/authorization checks
- [ ] SQL/injection vulnerabilities addressed
- [ ] Sensitive data is properly handled

### Performance
- [ ] No obvious performance bottlenecks
- [ ] Efficient database queries (no N+1)
- [ ] Appropriate use of async/await
- [ ] Resources are properly cleaned up

### Testing
- [ ] New code has corresponding tests
- [ ] Edge cases are covered
- [ ] Tests are meaningful (not just for coverage)

### Best Practices
- [ ] Follows project coding standards
- [ ] Consistent with existing codebase patterns
- [ ] Dependencies are appropriate
- [ ] No TODO comments without issue references

## Review Output Format

Provide review in this format:

```markdown
## Code Review Summary

### Overview
[Brief summary of changes and overall quality]

### Critical Issues
[Must be fixed before merge]

### Suggestions
[Recommended improvements]

### Positive Notes
[Things done well]

### Verdict
[ ] Approved
[ ] Approved with suggestions
[ ] Changes requested
```

## Instructions

1. Analyze the changes shown above
2. Check against each item in the review checklist
3. Provide specific, actionable feedback
4. Reference exact file:line locations for issues
5. Suggest concrete fixes where applicable
