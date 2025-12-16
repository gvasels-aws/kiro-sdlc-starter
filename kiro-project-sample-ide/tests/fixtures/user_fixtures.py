"""Shared test fixtures for user-related tests."""

import pytest

from src.models.user import CreateUserRequest, User
from src.services.user_service import UserService


@pytest.fixture
def sample_user() -> User:
    """Create a standard test user."""
    return User(id="usr_fixture", name="Fixture User", email="fixture@example.com")


@pytest.fixture
def admin_user() -> User:
    """Create an admin test user."""
    return User(id="usr_admin", name="Admin User", email="admin@example.com")


@pytest.fixture
def create_user_request() -> CreateUserRequest:
    """Create a standard create user request."""
    return CreateUserRequest(name="New User", email="new@example.com")


@pytest.fixture
def user_list() -> list[User]:
    """Create a list of test users."""
    return [
        User(id=f"usr_{i}", name=f"User {i}", email=f"user{i}@example.com")
        for i in range(10)
    ]


@pytest.fixture
def populated_service(user_list: list[User]) -> UserService:
    """Create a UserService pre-populated with test users."""
    service = UserService()
    for user in user_list:
        service.add_user(user)
    return service
