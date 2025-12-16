# Design: Hello World Example

**Spec Name:** hello-world
**Version:** 1.0.0

## Architecture

### Layer Structure

```
┌─────────────────────────────┐
│        API Layer            │  src/api/greeting_api.py
│   (HTTP handlers)           │
├─────────────────────────────┤
│      Service Layer          │  src/services/greeting_service.py
│   (Business logic)          │
├─────────────────────────────┤
│       Model Layer           │  src/models/greeting.py
│   (Data structures)         │
└─────────────────────────────┘
```

## Data Models

### GreetingRequest

Request model for generating greetings.

```python
@dataclass
class GreetingRequest:
    """Request to generate a greeting."""
    name: str
    greeting_type: Optional[str] = "Hello"  # "Hello", "Hi", "Welcome"
```

### GreetingResponse

Response model containing the generated greeting.

```python
@dataclass
class GreetingResponse:
    """Generated greeting response."""
    message: str
    name: str
    greeting_type: str
```

## Service Design

### GreetingService

**Location:** `src/services/greeting_service.py`

**Purpose:** Generate personalized greetings with customizable greeting types.

**Methods:**

```python
class GreetingService:
    def __init__(self) -> None:
        """Initialize the greeting service."""
        pass

    def generate_greeting(
        self,
        request: GreetingRequest
    ) -> GreetingResponse:
        """
        Generate a personalized greeting.

        Args:
            request: The greeting request with name and type

        Returns:
            GreetingResponse with formatted message

        Raises:
            ValueError: If name is empty or invalid
        """
        pass

    def _validate_name(self, name: str) -> None:
        """
        Validate that name is not empty.

        Args:
            name: The name to validate

        Raises:
            ValueError: If name is empty or whitespace-only
        """
        pass
```

## API Design

### Greeting Endpoint

**Location:** `src/api/greeting_api.py`

**Endpoint:** `GET /greet`

**Query Parameters:**
- `name` (required): The name to greet
- `type` (optional): Greeting type ("Hello", "Hi", "Welcome")

**Success Response (200):**
```json
{
  "message": "Hello, John!",
  "name": "John",
  "greeting_type": "Hello"
}
```

**Error Response (400):**
```json
{
  "error": "Invalid request",
  "detail": "Name parameter is required"
}
```

**Implementation:**

```python
def greet(name: Optional[str] = None, type: str = "Hello") -> dict:
    """
    Generate a greeting via API.

    Args:
        name: The name to greet (query parameter)
        type: The greeting type (query parameter)

    Returns:
        JSON response with greeting

    Raises:
        HTTPException: 400 if validation fails
    """
    pass
```

## Testing Strategy

### Unit Tests

**Location:** `tests/unit/`

1. **test_greeting_service.py**
   - `test_generate_greeting_success`: Valid name returns greeting
   - `test_generate_greeting_custom_type`: Custom greeting type works
   - `test_generate_greeting_empty_name`: Empty name raises ValueError
   - `test_generate_greeting_whitespace_name`: Whitespace name raises ValueError

2. **test_greeting_api.py**
   - `test_greet_endpoint_success`: Valid request returns 200
   - `test_greet_endpoint_missing_name`: Missing name returns 400
   - `test_greet_endpoint_custom_type`: Custom type works

### Test Fixtures

**Location:** `tests/fixtures/greeting_fixtures.py`

```python
@pytest.fixture
def greeting_service() -> GreetingService:
    """Create a fresh greeting service instance."""
    return GreetingService()

@pytest.fixture
def valid_request() -> GreetingRequest:
    """Create a valid greeting request."""
    return GreetingRequest(name="John", greeting_type="Hello")
```

### Coverage Target

- **Overall:** 90%+
- **Service Layer:** 95%+
- **Model Layer:** 100%

## Error Handling

### Validation Errors

```python
if not name or not name.strip():
    raise ValueError("Name cannot be empty or whitespace")
```

### API Error Responses

```python
try:
    response = service.generate_greeting(request)
    return response
except ValueError as e:
    return {"error": "Invalid request", "detail": str(e)}, 400
```

## Security Considerations

1. **Input Validation:**
   - Validate name length (max 100 characters)
   - Strip whitespace from inputs
   - Sanitize against injection attacks

2. **Rate Limiting:**
   - (Out of scope for this example)

3. **Authentication:**
   - (Out of scope for this example)

## File Structure

```
src/
├── models/
│   └── greeting.py         # GreetingRequest, GreetingResponse
├── services/
│   └── greeting_service.py # GreetingService
└── api/
    └── greeting_api.py      # greet() endpoint

tests/
├── unit/
│   ├── test_greeting_service.py
│   └── test_greeting_api.py
└── fixtures/
    └── greeting_fixtures.py
```

## Implementation Notes

1. **TDD Approach:**
   - Write tests first (RED)
   - Implement minimal code (GREEN)
   - Refactor for clarity (REFACTOR)

2. **Type Hints:**
   - All public functions fully typed
   - Use `Optional[T]` for nullable types
   - Use dataclasses for models

3. **Documentation:**
   - Google-style docstrings
   - Examples in docstrings where helpful
   - API documentation in `docs/api.md`
