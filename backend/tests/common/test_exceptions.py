import pytest
from api.exceptions import TableEmptyError, UserAlreadyExistsError, UserNotFoundError


class TestExceptions:
    """Test cases for custom exceptions"""

    @pytest.mark.unit
    @pytest.mark.common
    def test_table_empty_error(self):
        """Test TableEmptyError exception"""
        table_name = "users"
        error = TableEmptyError(table_name)

        assert str(error) == f"Table '{table_name}' is empty."
        assert isinstance(error, Exception)

    @pytest.mark.unit
    @pytest.mark.common
    def test_user_not_found_error(self):
        """Test UserNotFoundError exception"""
        query = {"email": "test@example.com"}
        user_type = "Student"
        error = UserNotFoundError(query, user_type)

        expected_message = f"{user_type} with the following details not found: {query}"
        assert str(error) == expected_message
        assert isinstance(error, Exception)

    @pytest.mark.unit
    @pytest.mark.common
    def test_user_already_exists_error(self):
        """Test UserAlreadyExistsError exception"""
        email = "test@example.com"
        user_type = "Tutor"
        error = UserAlreadyExistsError(email, user_type)

        expected_message = (
            f"User with email '{email}' and type '{user_type}' already exists."
        )
        assert str(error) == expected_message
        assert error.email == email
        assert error.userType == user_type
        assert isinstance(error, Exception)

    @pytest.mark.unit
    @pytest.mark.common
    def test_exception_inheritance(self):
        """Test that all custom exceptions inherit from Exception"""
        table_error = TableEmptyError("test_table")
        not_found_error = UserNotFoundError({"email": "test"}, "Student")
        exists_error = UserAlreadyExistsError("test@example.com", "Tutor")

        assert isinstance(table_error, Exception)
        assert isinstance(not_found_error, Exception)
        assert isinstance(exists_error, Exception)

    @pytest.mark.unit
    @pytest.mark.common
    def test_exception_attributes(self):
        """Test exception attributes are properly set"""
        # Test UserAlreadyExistsError attributes
        email = "test@example.com"
        user_type = "Student"
        error = UserAlreadyExistsError(email, user_type)

        assert hasattr(error, "email")
        assert hasattr(error, "userType")
        assert error.email == email
        assert error.userType == user_type
