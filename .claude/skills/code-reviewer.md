---
description: Comprehensive code review with security, performance, and quality analysis
tools: read, grep, diff, lint_runner
---

# Code Reviewer Skill

Provides comprehensive code review capabilities focusing on quality, security, and maintainability.

## Capabilities

- **Quality Analysis**: Code style, readability, maintainability
- **Security Review**: Vulnerability detection, OWASP checks
- **Performance Analysis**: Bottlenecks, optimization opportunities
- **Best Practices**: Pattern adherence, anti-pattern detection
- **Test Coverage**: Test quality and coverage assessment

## Review Categories

### Code Quality
- Naming conventions
- Function length and complexity
- Code duplication
- Comment quality
- Error handling

### Security
- Input validation
- Authentication checks
- Authorization controls
- Data sanitization
- Secret management

### Performance
- Algorithm efficiency
- Database query optimization
- Memory management
- Async/await usage
- Caching opportunities

### Maintainability
- Single responsibility
- Dependency management
- Abstraction levels
- Documentation
- Test coverage

## Output Format

Reviews are structured with:
1. Summary of changes
2. Critical findings (must fix)
3. Suggestions (should consider)
4. Positive observations
5. Overall verdict

## Usage

This skill is automatically available. It's commonly used:
- During code review requests
- By the security-checker plugin
- By agents that need code analysis
