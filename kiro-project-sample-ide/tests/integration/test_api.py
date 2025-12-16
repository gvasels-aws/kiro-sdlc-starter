"""Integration tests for Sample API - Written BEFORE implementation (TDD Red Phase)."""

import pytest

from src.api.sample_api import create_user, get_user_by_id, get_users, validate_input


class TestGetUsers:
    """Integration tests for get_users API."""

    def test_get_users_returns_list(self) -> None:
        """Test that get_users returns a list."""
        result = get_users()

        assert isinstance(result, list)

    def test_get_users_default_pagination(self) -> None:
        """Test get_users with default limit and offset."""
        result = get_users()

        assert len(result) <= 10  # Default limit

    def test_get_users_custom_limit(self) -> None:
        """Test get_users with custom limit."""
        result = get_users(limit=5)

        assert len(result) <= 5

    def test_get_users_with_offset(self) -> None:
        """Test get_users with offset."""
        result = get_users(limit=5, offset=2)

        assert isinstance(result, list)

    def test_get_users_returns_dicts(self) -> None:
        """Test that get_users returns list of dictionaries."""
        result = get_users(limit=1)

        if result:
            assert isinstance(result[0], dict)
            assert "id" in result[0]
            assert "name" in result[0]


class TestGetUserById:
    """Integration tests for get_user_by_id API."""

    def test_get_user_by_id_found(self) -> None:
        """Test retrieving an existing user."""
        # First create a user
        created = create_user(name="Test User", email="test@example.com")
        user_id = created["id"]

        result = get_user_by_id(user_id)

        assert result is not None
        assert result["id"] == user_id

    def test_get_user_by_id_not_found(self) -> None:
        """Test retrieving a non-existent user returns None."""
        result = get_user_by_id("not_found_id_12345")

        assert result is None

    def test_get_user_by_id_returns_dict(self) -> None:
        """Test that found user is returned as dictionary."""
        created = create_user(name="Dict Test", email="dict@example.com")

        result = get_user_by_id(created["id"])

        assert isinstance(result, dict)
        assert "id" in result
        assert "name" in result
        assert "email" in result


class TestCreateUser:
    """Integration tests for create_user API."""

    def test_create_user_success(self) -> None:
        """Test creating a user successfully."""
        result = create_user(name="New User", email="new@example.com")

        assert isinstance(result, dict)
        assert "id" in result
        assert result["name"] == "New User"
        assert result["email"] == "new@example.com"

    def test_create_user_generates_id(self) -> None:
        """Test that create_user generates an ID."""
        result = create_user(name="ID Test", email="id@example.com")

        assert result["id"].startswith("usr_")

    def test_create_user_invalid_email(self) -> None:
        """Test create_user with invalid email raises error."""
        with pytest.raises(ValueError, match="Invalid email"):
            create_user(name="Bad Email", email="invalid")

    def test_create_user_empty_name(self) -> None:
        """Test create_user with empty name raises error."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            create_user(name="", email="valid@example.com")


class TestValidateInput:
    """Integration tests for validate_input helper."""

    def test_validate_input_valid(self) -> None:
        """Test validation with valid data."""
        data = {"name": "Test", "email": "test@example.com"}

        result = validate_input(data)

        assert result is True

    def test_validate_input_empty(self) -> None:
        """Test validation with empty data."""
        result = validate_input({})

        assert result is False

    def test_validate_input_none(self) -> None:
        """Test validation with None."""
        result = validate_input(None)  # type: ignore

        assert result is False

    def test_validate_input_missing_name(self) -> None:
        """Test validation with missing name."""
        data = {"email": "test@example.com"}

        result = validate_input(data)

        assert result is False

    def test_validate_input_missing_email(self) -> None:
        """Test validation with missing email."""
        data = {"name": "Test"}

        result = validate_input(data)

        assert result is False
