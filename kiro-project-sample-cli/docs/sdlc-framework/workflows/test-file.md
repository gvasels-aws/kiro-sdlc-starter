---
description: Generate comprehensive tests for a specific file
---

# Generate Tests for File

Generate comprehensive tests for the specified source file using TDD principles.

## Target File
$ARGUMENTS

## Instructions

1. **Read the source file** specified above
2. **Analyze the code** to identify:
   - Exported functions and classes
   - Input parameters and their types
   - Return values and their types
   - Error scenarios and edge cases
   - Dependencies that need mocking

3. **Generate tests** covering:
   - Happy path scenarios
   - Edge cases (empty inputs, nulls, boundaries)
   - Error handling paths
   - Integration with dependencies

## Test Structure

Use this structure for the generated tests:

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { FunctionUnderTest } from './source-file';

describe('FunctionUnderTest', () => {
  describe('when given valid input', () => {
    it('should return expected result', () => {
      // Arrange
      const input = createValidInput();

      // Act
      const result = FunctionUnderTest(input);

      // Assert
      expect(result).toEqual(expectedOutput);
    });
  });

  describe('when given invalid input', () => {
    it('should throw ValidationError', () => {
      // Arrange
      const input = createInvalidInput();

      // Act & Assert
      expect(() => FunctionUnderTest(input)).toThrow(ValidationError);
    });
  });

  describe('edge cases', () => {
    it('should handle empty input', () => {
      // ...
    });

    it('should handle boundary values', () => {
      // ...
    });
  });
});
```

## Output

1. Generate the complete test file
2. Place it in the appropriate `tests/` directory
3. Include any necessary test fixtures or helpers
4. Ensure tests follow the existing testing patterns in the project

## Test Coverage Goals

- Line coverage: 80%+
- Branch coverage: 70%+
- All public APIs tested
- Error paths tested
