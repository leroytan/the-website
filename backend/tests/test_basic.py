import pytest
from api.auth.auth_service import AuthService
from api.router.models import LoginRequest


class TestBasicSetup:
    """Basic tests to verify the testing setup works"""

    @pytest.mark.unit
    def test_auth_service_import(self):
        """Test that AuthService can be imported and instantiated"""
        # This test verifies that the basic imports work
        assert AuthService is not None

        # Test basic password hashing
        password = "testpassword123"
        hashed = AuthService.hash_password(password)

        assert hashed != password
        assert len(hashed) > 0
        assert AuthService.verify_password(password, hashed) is True

    @pytest.mark.unit
    def test_model_validation(self):
        """Test that Pydantic models work correctly"""
        # Test valid login request
        login_data = {"email": "test@example.com", "password": "testpassword123"}

        login_request = LoginRequest(**login_data)
        assert login_request.email == "test@example.com"
        assert login_request.password == "testpassword123"

    @pytest.mark.unit
    def test_pytest_working(self):
        """Basic test to verify pytest is working"""
        assert True
        assert 1 + 1 == 2

    @pytest.mark.unit
    def test_mock_working(self):
        """Test that mocking works correctly"""
        from unittest.mock import Mock

        mock_obj = Mock()
        mock_obj.some_method.return_value = "mocked_value"

        assert mock_obj.some_method() == "mocked_value"
        mock_obj.some_method.assert_called_once()

    @pytest.mark.unit
    def test_fixtures_working(self, sample_user_data):
        """Test that fixtures are working"""
        assert sample_user_data["email"] == "test@example.com"
        assert sample_user_data["name"] == "Test User"
        assert "password" in sample_user_data

    @pytest.mark.unit
    def test_test_structure(self):
        """Test that the test structure is properly organized"""
        # Verify that test directories exist and are properly structured
        import os

        # Check that all test directories exist
        test_dirs = ["auth", "router", "logic", "storage", "services", "common"]
        for test_dir in test_dirs:
            assert os.path.exists(f"tests/{test_dir}"), (
                f"Test directory tests/{test_dir} does not exist"
            )
            assert os.path.exists(f"tests/{test_dir}/__init__.py"), (
                f"__init__.py missing in tests/{test_dir}"
            )

        # Check that all test files exist
        test_files = [
            # Auth tests
            "tests/auth/test_auth_service.py",
            # Router tests
            "tests/router/test_auth.py",
            "tests/router/test_auth_utils.py",
            "tests/router/test_models.py",
            # Logic tests
            "tests/logic/test_auth_logic.py",
            "tests/logic/test_user_logic.py",
            "tests/logic/test_tutor_logic.py",
            "tests/logic/test_payment_logic.py",
            "tests/logic/test_sort_logic.py",
            "tests/logic/test_filter_logic.py",
            "tests/logic/test_course_logic.py",
            "tests/logic/test_assignment_logic.py",
            "tests/logic/test_assignment_logic_simple.py",
            "tests/logic/test_auth_logic_simple.py",
            # Storage tests
            "tests/storage/test_models.py",
            # Services tests
            "tests/services/test_email_service.py",
            "tests/services/test_content_filter_service.py",
            # Common tests
            "tests/common/test_constants.py",
            "tests/common/test_utils.py",
            # Root test files
            "tests/test_basic.py",
            "tests/conftest.py",
        ]

        for test_file in test_files:
            assert os.path.exists(test_file), f"Test file {test_file} does not exist"

        # Check that no integration directory exists (since we removed it)
        assert not os.path.exists("tests/integration"), (
            "Integration directory should not exist"
        )

        # Additional strict validations
        # Check that all test files have proper naming convention
        for test_file in test_files:
            if test_file.endswith(".py") and "test_" in test_file:
                filename = os.path.basename(test_file)
                assert filename.startswith("test_"), (
                    f"Test file {filename} should start with 'test_'"
                )

        # Check that all test directories have __init__.py files
        for test_dir in test_dirs:
            init_file = f"tests/{test_dir}/__init__.py"
            assert os.path.exists(init_file), f"Missing __init__.py in {test_dir}"

        # Check that we have a reasonable number of test files
        assert len(test_files) >= 15, (
            f"Expected at least 15 test files, found {len(test_files)}"
        )

        # Check that pytest.ini exists and is properly configured
        assert os.path.exists("pytest.ini"), "pytest.ini configuration file missing"

        # Check that conftest.py exists and is properly configured
        assert os.path.exists("tests/conftest.py"), "conftest.py missing"
