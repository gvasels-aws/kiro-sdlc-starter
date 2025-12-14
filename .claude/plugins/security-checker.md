---
name: security-checker
description: Security vulnerability scanning and audit (runs in CI)
phase: pr-level
skills: [code-reviewer]
agents: [security-auditor]
mcp_servers: []
---

# Security Checker Plugin

Performs comprehensive security audits. **Runs automatically in CI when PR is created.**

## Phase Position

```
1. SPEC → 2. TEST → 3. CODE → 4. BUILD → 5. DOCS → CREATE PR
                                                        │
                                              ┌─────────┴─────────┐
                                              │  PR-Level (Auto)  │
                                              │ [SECURITY AUDIT]  │ ◄── YOU ARE HERE
                                              │  • Code Review    │
                                              └───────────────────┘
```

**Note**: This plugin documents what runs automatically in CI. You don't need to invoke it manually.

## Security Scan Pipeline (CI)

```
DEPENDENCY SCAN (npm audit, govulncheck, safety)
         │
         ▼
SECRETS SCAN (gitleaks, trufflehog)
         │
         ▼
SAST SCAN (semgrep, CodeQL, gosec)
         │
         ▼
INFRASTRUCTURE SCAN (checkov, tfsec for OpenTofu)
```

## Quality Gates

| Check | Threshold |
|-------|-----------|
| Critical vulnerabilities | 0 |
| High vulnerabilities | 0 |
| Hardcoded secrets | 0 |
| SAST critical findings | 0 |
| IaC critical misconfigs | 0 |

## CI Configuration

These checks are configured in `.github/workflows/claude-code-review.yml`:

```bash
# Secrets detection
gitleaks detect --source .

# Dependency vulnerabilities
npm audit --audit-level=high
govulncheck ./...

# Infrastructure security (if OpenTofu files changed)
checkov -d infrastructure/ --framework terraform

# SAST scan
semgrep --config=auto .
```

## When to Invoke Manually

Only invoke this plugin manually if:
- You want to run security checks before creating PR
- You need to investigate a specific security concern
- CI security checks are failing and you need details

```
Use Task tool with subagent_type='security-auditor'
Provide:
- List of files changed
- Authentication/authorization flows
- Data handling patterns
```
