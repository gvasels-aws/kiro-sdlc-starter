---
plugin: security-checker
phase: 5
description: Run security scans and dependency checks
---

# Security Checker Plugin (CLI Template)

## Purpose

Execute security scanning and dependency vulnerability checks.

## Workflow

1. **Load Context**
   - Read `.kiro/steering/phases/05-quality-gate.md` for security guidance

2. **Execute Quality Gate Script**
   ```bash
   ./scripts/quality-gate.sh
   ```

   This runs:
   - `./scripts/security-scan.sh` - Bandit security analysis
   - Safety check for dependency vulnerabilities

3. **Handle Findings**
   - Critical/High vulnerabilities: Must fix before proceeding
   - Medium vulnerabilities: Document and plan fix
   - Low/Info: Optional fixes

## Quality Gates

- ✅ 0 critical/high security vulnerabilities
- ✅ No known vulnerable dependencies

## Transition

Once security checks pass, transition to Phase 6 (DOCS) - docs-generator plugin.
