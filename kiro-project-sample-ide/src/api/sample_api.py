"""Sample API module for user operations."""

from typing import Any

from src.models.user import CreateUserRequest, User
from src.services.user_service import UserService

# Module-level service instance
_service = UserService()


def get_users(limit: int = 10, offset: int = 0) -> list[dict[str, Any]]:
    """Get list of users with pagination.

    Args:
        limit: Maximum number of users to return (default: 10).
        offset: Number of users to skip (default: 0).

    Returns:
        List of user dictionaries with id, name, and email fields.
    """
    users = _service.list_users(limit=limit, offset=offset)
    return [_user_to_dict(u) for u in users]


def get_user_by_id(user_id: str) -> dict[str, Any] | None:
    """Get a single user by ID.

    Args:
        user_id: The unique identifier of the user.

    Returns:
        User dictionary if found, None otherwise.
    """
    user = _service.get_user(user_id)
    if user is None:
        return None
    return _user_to_dict(user)


def create_user(name: str, email: str) -> dict[str, Any]:
    """Create a new user.

    Args:
        name: User's display name.
        email: User's email address.

    Returns:
        Dictionary representation of created user.

    Raises:
        ValueError: If name is empty or email format is invalid.
    """
    request = CreateUserRequest(name=name, email=email)
    user = _service.create_user(request)
    return _user_to_dict(user)


def validate_input(data: dict[str, Any] | None) -> bool:
    """Validate input data for user creation.

    Args:
        data: Dictionary with expected 'name' and 'email' keys.

    Returns:
        True if data is valid, False otherwise.
    """
    if not data:
        return False
    for key in ["name", "email"]:
        if key not in data:
            return False
    return True


def _user_to_dict(user: User) -> dict[str, Any]:
    """Convert User to dictionary.

    Args:
        user: The User to convert.

    Returns:
        Dictionary with id, name, and email fields.
    """
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }
