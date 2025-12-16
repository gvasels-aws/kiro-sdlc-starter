# API Documentation

## Overview

This document describes the User API endpoints for the Kiro SDLC Sample Project.

## Endpoints

### GET /users

Retrieve a list of users with pagination.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| limit | int | No | 10 | Maximum number of users to return |
| offset | int | No | 0 | Number of users to skip |

**Response (200 OK):**

```json
[
  {
    "id": "usr_abc123",
    "name": "John Doe",
    "email": "john@example.com"
  },
  {
    "id": "usr_def456",
    "name": "Jane Smith",
    "email": "jane@example.com"
  }
]
```

**Example:**

```python
from src.api.sample_api import get_users

# Get first 5 users
users = get_users(limit=5)

# Get second page
users_page2 = get_users(limit=5, offset=5)
```

---

### GET /users/{user_id}

Retrieve a single user by their unique identifier.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| user_id | string | Yes | The user's unique identifier |

**Response (200 OK):**

```json
{
  "id": "usr_abc123",
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Response (404 Not Found):**

Returns `None` if user is not found.

**Example:**

```python
from src.api.sample_api import get_user_by_id

# Get user by ID
user = get_user_by_id("usr_abc123")
if user:
    print(f"Found: {user['name']}")
else:
    print("User not found")
```

---

### POST /users

Create a new user account.

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | User's display name (non-empty) |
| email | string | Yes | User's email address (valid email format) |

**Request Example:**

```json
{
  "name": "New User",
  "email": "new@example.com"
}
```

**Response (201 Created):**

```json
{
  "id": "usr_xyz789",
  "name": "New User",
  "email": "new@example.com"
}
```

**Response (400 Bad Request):**

- `ValueError: Name cannot be empty` - When name is empty or whitespace only
- `ValueError: Invalid email format` - When email doesn't match expected format

**Example:**

```python
from src.api.sample_api import create_user

try:
    user = create_user(name="John Doe", email="john@example.com")
    print(f"Created user with ID: {user['id']}")
except ValueError as e:
    print(f"Validation error: {e}")
```

---

## Data Models

### User

```python
@dataclass
class User:
    id: str      # Format: usr_XXXXXXXX
    name: str    # User's display name
    email: str   # User's email address (default: "")
```

### CreateUserRequest

```python
@dataclass
class CreateUserRequest:
    name: str    # Required, non-empty
    email: str   # Required, valid email format
```

---

## Validation

### Email Validation

Emails must match the pattern:
```
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

**Valid examples:**
- `user@example.com`
- `first.last@company.co.uk`
- `user+tag@domain.org`

**Invalid examples:**
- `user` (no domain)
- `@example.com` (no local part)
- `user@` (no domain)
- `user@.com` (invalid domain)

### Name Validation

- Must not be empty
- Must not be whitespace only
- No length restrictions

---

## Error Handling

All validation errors raise `ValueError` with descriptive messages:

```python
try:
    user = create_user(name="", email="test@example.com")
except ValueError as e:
    # e.args[0] == "Name cannot be empty"
    pass

try:
    user = create_user(name="Test", email="invalid")
except ValueError as e:
    # e.args[0] == "Invalid email format"
    pass
```

---

## Helper Functions

### validate_input

Validate input data before processing.

```python
from src.api.sample_api import validate_input

data = {"name": "Test", "email": "test@example.com"}
if validate_input(data):
    # Safe to process
    pass
else:
    # Missing required fields
    pass
```

**Returns:** `True` if data contains both `name` and `email` keys, `False` otherwise.
