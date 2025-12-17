---
plugin: spec-writer
phase: 1
description: Create requirements, design, and task breakdown using spec-workflow MCP
---

# Spec Writer Plugin (CLI Template)

## Purpose

Guide the user through creating a complete specification using the spec-workflow MCP server before any code is written.

## Workflow

1. **Load Context**
   - Read `.kiro/steering/phases/01-spec.md` for detailed guidance
   - Reference existing specs in `.kiro/specs/` for examples

2. **Use spec-workflow MCP**
   - Invoke spec-workflow tools to create requirements.md
   - Invoke spec-workflow tools to create design.md
   - Invoke spec-workflow tools to create tasks.md

3. **Request Approval**
   - Use spec-workflow approval mechanism
   - Wait for user approval before proceeding to next phase

## Outputs

- `.kiro/specs/{spec-name}/requirements.md`
- `.kiro/specs/{spec-name}/design.md`
- `.kiro/specs/{spec-name}/tasks.md`

## Transition

Once spec is approved, transition to Phase 2 (TEST) - test-writer plugin.
