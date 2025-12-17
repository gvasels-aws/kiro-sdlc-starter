---
plugin: code-implementer
phase: 3
description: Implement minimal code to make tests pass (TDD Green phase)
---

# Code Implementer Plugin (CLI Template)

## Purpose

Write minimal implementation code to make the failing tests pass, following TDD principles.

## Workflow

1. **Load Context**
   - Read `.kiro/steering/phases/03-code.md` for implementation guidance
   - Review the failing tests to understand what needs to be implemented
   - Follow the design from design.md

2. **Implement in Order**
   - **Data Models** first (`src/models/`)
   - **Business Logic** next (`src/services/`)
   - **API Layer** last (`src/api/`)

3. **TDD Cycle**
   - Write minimal code to pass one test
   - Run tests: `pytest`
   - If tests pass → Refactor (optional)
   - If tests fail → Continue implementing
   - Repeat until all tests pass (Green phase)

4. **Avoid Over-Engineering**
   - Only write code needed to pass tests
   - Don't add features not in the spec
   - Keep it simple

## Quality Checks

- All tests passing (Green phase)
- No unnecessary code added
- Follows design contracts
- Code is readable and maintainable

## Transition

Once all tests pass, transition to Phase 4 (BUILD) - builder plugin.
