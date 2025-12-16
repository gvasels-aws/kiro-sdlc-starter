"""Unit tests for UserService - Written BEFORE implementation (TDD Red Phase)."""

import pytest

from src.models.user import CreateUserRequest, User
from src.services.user_service import UserService


class TestUserService:
    """Test suite for UserService."""

    @pytest.fixture
    def service(self) -> UserService:
        """Create a fresh UserService instance."""
        return UserService()

    @pytest.fixture
    def sample_user(self) -> User:
        """Create a sample user for testing."""
        return User(id="usr_test", name="Test User", email="test@example.com")

    # === Happy Path Tests ===

    def test_create_user_success(self, service: UserService) -> None:
        """Test creating a user with valid input."""
        request = CreateUserRequest(name="John Doe", email="john@example.com")

        user = service.create_user(request)

        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.id.startswith("usr_")

    def test_get_user_exists(self, service: UserService, sample_user: User) -> None:
        """Test retrieving an existing user by ID."""
        service.add_user(sample_user)

        result = service.get_user(sample_user.id)

        assert result is not None
        assert result.id == sample_user.id
        assert result.name == sample_user.name
        assert result.email == sample_user.email

    def test_add_user(self, service: UserService) -> None:
        """Test adding a user directly."""
        user = User(id="usr_direct", name="Direct Add", email="direct@example.com")

        service.add_user(user)
        result = service.get_user("usr_direct")

        assert result is not None
        assert result.name == "Direct Add"

    def test_list_users_empty(self, service: UserService) -> None:
        """Test listing users when empty."""
        result = service.list_users()

        assert result == []

    def test_list_users_with_data(self, service: UserService) -> None:
        """Test listing users with data."""
        for i in range(5):
            service.add_user(User(id=f"usr_{i}", name=f"User {i}"))

        result = service.list_users()

        assert len(result) == 5

    # === Error Cases ===

    def test_get_user_not_found(self, service: UserService) -> None:
        """Test retrieving a non-existent user returns None."""
        result = service.get_user("nonexistent_id")

        assert result is None

    def test_create_user_invalid_email(self, service: UserService) -> None:
        """Test creating user with invalid email raises error."""
        request = CreateUserRequest(name="John", email="not-an-email")

        with pytest.raises(ValueError, match="Invalid email"):
            service.create_user(request)

    def test_create_user_empty_name(self, service: UserService) -> None:
        """Test creating user with empty name raises error."""
        request = CreateUserRequest(name="", email="john@example.com")

        with pytest.raises(ValueError, match="Name cannot be empty"):
            service.create_user(request)

    def test_create_user_whitespace_name(self, service: UserService) -> None:
        """Test creating user with whitespace-only name raises error."""
        request = CreateUserRequest(name="   ", email="john@example.com")

        with pytest.raises(ValueError, match="Name cannot be empty"):
            service.create_user(request)

    # === Pagination Edge Cases ===

    @pytest.mark.parametrize(
        "limit,offset,expected_count",
        [
            (5, 0, 5),  # First page
            (10, 0, 10),  # Full list
            (10, 8, 2),  # Partial page at end
            (100, 0, 10),  # More than available
            (5, 100, 0),  # Offset beyond data
            (0, 0, 0),  # Zero limit
        ],
    )
    def test_list_users_pagination(
        self,
        service: UserService,
        limit: int,
        offset: int,
        expected_count: int,
    ) -> None:
        """Test pagination with various limit/offset combinations."""
        # Setup: add 10 users
        for i in range(10):
            service.add_user(User(id=f"usr_{i}", name=f"User {i}"))

        result = service.list_users(limit=limit, offset=offset)

        assert len(result) == expected_count

    def test_list_users_ordering(self, service: UserService) -> None:
        """Test that list_users returns users in consistent order."""
        for i in range(3):
            service.add_user(User(id=f"usr_{i}", name=f"User {i}"))

        result1 = service.list_users()
        result2 = service.list_users()

        assert [u.id for u in result1] == [u.id for u in result2]
