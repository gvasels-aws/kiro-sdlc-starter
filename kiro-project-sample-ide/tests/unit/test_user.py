"""Unit tests for User model - Written BEFORE implementation (TDD Red Phase)."""

from src.models.user import CreateUserRequest, User


class TestUser:
    """Test suite for User dataclass."""

    def test_user_creation_with_all_fields(self) -> None:
        """Test creating a User with all fields."""
        user = User(id="usr_123", name="Test User", email="test@example.com")

        assert user.id == "usr_123"
        assert user.name == "Test User"
        assert user.email == "test@example.com"

    def test_user_creation_with_default_email(self) -> None:
        """Test creating a User with default empty email."""
        user = User(id="usr_456", name="No Email User")

        assert user.id == "usr_456"
        assert user.name == "No Email User"
        assert user.email == ""

    def test_user_equality(self) -> None:
        """Test that two users with same fields are equal."""
        user1 = User(id="usr_789", name="Same", email="same@test.com")
        user2 = User(id="usr_789", name="Same", email="same@test.com")

        assert user1 == user2

    def test_user_inequality(self) -> None:
        """Test that users with different IDs are not equal."""
        user1 = User(id="usr_001", name="User", email="user@test.com")
        user2 = User(id="usr_002", name="User", email="user@test.com")

        assert user1 != user2


class TestCreateUserRequest:
    """Test suite for CreateUserRequest dataclass."""

    def test_create_user_request(self) -> None:
        """Test creating a CreateUserRequest."""
        request = CreateUserRequest(name="New User", email="new@example.com")

        assert request.name == "New User"
        assert request.email == "new@example.com"

    def test_create_user_request_equality(self) -> None:
        """Test that two requests with same fields are equal."""
        req1 = CreateUserRequest(name="Test", email="test@test.com")
        req2 = CreateUserRequest(name="Test", email="test@test.com")

        assert req1 == req2
