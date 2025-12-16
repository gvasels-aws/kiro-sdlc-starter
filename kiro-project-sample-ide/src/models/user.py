"""User data models."""

from dataclasses import dataclass


@dataclass
class User:
    """User entity.

    Attributes:
        id: Unique identifier for the user (format: usr_XXXXXXXX)
        name: User's display name
        email: User's email address (optional, defaults to empty string)
    """

    id: str
    name: str
    email: str = ""


@dataclass
class CreateUserRequest:
    """Request model for creating a new user.

    Attributes:
        name: User's display name (required, non-empty)
        email: User's email address (required, valid email format)
    """

    name: str
    email: str
