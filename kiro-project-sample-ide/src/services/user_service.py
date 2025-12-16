"""User service with business logic."""

import re
import uuid

from src.models.user import CreateUserRequest, User


class UserService:
    """Service for user operations.

    Provides CRUD operations for users with validation.

    Attributes:
        _users: Internal storage for users (dict keyed by user ID)
    """

    def __init__(self) -> None:
        """Initialize the UserService with empty storage."""
        self._users: dict[str, User] = {}

    def create_user(self, request: CreateUserRequest) -> User:
        """Create a new user.

        Args:
            request: The user creation request with name and email.

        Returns:
            The created User with generated ID.

        Raises:
            ValueError: If name is empty or email format is invalid.
        """
        self._validate_request(request)

        user = User(
            id=self._generate_id(),
            name=request.name,
            email=request.email,
        )
        self._users[user.id] = user
        return user

    def get_user(self, user_id: str) -> User | None:
        """Get a user by ID.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            The User if found, None otherwise.
        """
        return self._users.get(user_id)

    def add_user(self, user: User) -> None:
        """Add a user directly to storage.

        Used for testing and data migration.

        Args:
            user: The User to add.
        """
        self._users[user.id] = user

    def list_users(self, limit: int = 10, offset: int = 0) -> list[User]:
        """List users with pagination.

        Args:
            limit: Maximum number of users to return (default: 10).
            offset: Number of users to skip (default: 0).

        Returns:
            List of User objects within the specified range.
        """
        users = list(self._users.values())
        return users[offset : offset + limit]

    def _generate_id(self) -> str:
        """Generate a unique user ID.

        Returns:
            A string ID in format 'usr_XXXXXXXX'.
        """
        return f"usr_{uuid.uuid4().hex[:8]}"

    def _validate_request(self, request: CreateUserRequest) -> None:
        """Validate a create user request.

        Args:
            request: The request to validate.

        Raises:
            ValueError: If name is empty or email format is invalid.
        """
        if not request.name or not request.name.strip():
            raise ValueError("Name cannot be empty")

        if not self._is_valid_email(request.email):
            raise ValueError("Invalid email format")

    def _is_valid_email(self, email: str) -> bool:
        """Check if email format is valid.

        Args:
            email: The email address to validate.

        Returns:
            True if email format is valid, False otherwise.
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))
