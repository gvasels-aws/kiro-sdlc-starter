---
plugin: docs-generator
phase: 6
description: Generate documentation and update CHANGELOG
---

# Docs Generator Plugin (CLI Template)

## Purpose

Generate comprehensive documentation before creating a pull request.

## Workflow

1. **Load Context**
   - Read `.kiro/steering/phases/06-docs.md` for documentation guidance

2. **Update Documentation**

   **CHANGELOG.md** (REQUIRED):
   ```markdown
   ## [Unreleased]

   ### Added
   - [Your new feature]

   ### Changed
   - [Any changes to existing functionality]

   ### Fixed
   - [Any bug fixes]
   ```

   **CLAUDE.md Files**:
   - Create `CLAUDE.md` in new directories
   - Update existing `CLAUDE.md` with new functions/exports
   - Document purpose, functions, dependencies

   **API Documentation**:
   - Document new endpoints
   - Include request/response examples
   - Update `docs/api.md` if it exists

3. **Verify Documentation**
   - CHANGELOG.md has entry for this feature
   - All new directories have CLAUDE.md
   - API changes documented

## Quality Checks

- ✅ CHANGELOG.md updated
- ✅ CLAUDE.md files created/updated
- ✅ API documentation complete

## Transition

Documentation complete → Ready to create Pull Request (optional).
