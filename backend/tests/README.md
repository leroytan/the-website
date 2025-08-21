# Testing Guide

This directory contains all tests for the backend API. The test suite is organized by functionality and follows best practices for Python testing.

## 🏗️ Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and configuration
├── test_basic.py            # Basic setup and validation tests
├── auth/                    # Authentication tests
│   ├── __init__.py
│   └── test_auth_service.py
├── router/                  # API router tests
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_auth_utils.py
│   └── test_models.py
├── logic/                   # Business logic tests
│   ├── __init__.py
│   ├── test_auth_logic.py
│   ├── test_user_logic.py
│   ├── test_tutor_logic.py
│   ├── test_payment_logic.py
│   ├── test_chat_logic.py
│   ├── test_sort_logic.py
│   ├── test_filter_logic.py
│   ├── test_course_logic.py
│   └── test_assignment_logic.py
├── storage/                 # Database model tests
│   ├── __init__.py
│   └── test_models.py
├── services/                # Service layer tests
│   ├── __init__.py
│   ├── test_email_service.py
│   └── test_content_filter_service.py
└── common/                  # Common utilities tests
    ├── __init__.py
    ├── test_constants.py
    └── test_utils.py
```

## 🚀 Running Tests

### Quick Start
```bash
# Run all tests
poetry run pytest tests/

# Run with coverage
poetry run pytest tests/ --cov=api --cov-report=term-missing

# Run specific test file
poetry run pytest tests/auth/test_auth_service.py

# Run specific test class
poetry run pytest tests/auth/test_auth_service.py::TestAuthService

# Run specific test method
poetry run pytest tests/auth/test_auth_service.py::TestAuthService::test_hash_password
```

### Using the Test Script
```bash
# Run comprehensive test suite with coverage
./scripts/run_tests.sh
```

### Test Categories
```bash
# Run by markers
poetry run pytest tests/ -m unit      # Unit tests
poetry run pytest tests/ -m auth      # Authentication tests
poetry run pytest tests/ -m logic     # Business logic tests
poetry run pytest tests/ -m router    # Router tests
poetry run pytest tests/ -m services  # Service tests
poetry run pytest tests/ -m models    # Model tests

# Run by directory
poetry run pytest tests/auth/         # All auth tests
poetry run pytest tests/router/       # All router tests
poetry run pytest tests/logic/        # All logic tests
poetry run pytest tests/services/     # All service tests
```

## 📊 Coverage Reports

### Understanding Coverage
The test suite generates coverage data in a `.coverage` file (SQLite database). This file is not human-readable but can be used to generate various reports.

### Coverage Commands
```bash
# Terminal report
poetry run coverage report

# Terminal report with missing lines
poetry run coverage report --show-missing

# HTML report (interactive)
poetry run coverage html
open htmlcov/index.html

# XML report (for CI/CD)
poetry run coverage xml

# JSON report
poetry run coverage json

# Branch coverage
poetry run coverage report --branch
```

### Coverage Configuration
Coverage is configured in `.coveragerc`:
- **Source**: `api/` directory
- **Excluded**: `tests/`, `migrations/`, `__pycache__/`, `venv/`
- **HTML output**: `htmlcov/` directory

### Coverage Data Management
```bash
# Erase coverage data
poetry run coverage erase

# Combine multiple coverage files
poetry run coverage combine

# Debug coverage data
poetry run coverage debug data
```

## 🏷️ Test Markers

### Available Markers
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests (removed)
- `@pytest.mark.auth` - Authentication tests
- `@pytest.mark.logic` - Business logic tests
- `@pytest.mark.models` - Model tests
- `@pytest.mark.router` - Router tests
- `@pytest.mark.services` - Service layer tests
- `@pytest.mark.slow` - Slow running tests
- `@pytest.mark.asyncio` - Async tests

### Using Markers
```python
@pytest.mark.unit
@pytest.mark.auth
def test_user_login():
    """Test user login functionality"""
    pass
```

## 🔧 Test Configuration

### pytest.ini
- **Test paths**: `tests/`
- **Python files**: `test_*.py`
- **Python classes**: `Test*`
- **Python functions**: `test_*`
- **Options**: Verbose, short tracebacks, coverage
- **Async mode**: Strict

### conftest.py
- **Database fixtures**: Test engine and sessions
- **Mock fixtures**: Storage, auth, email services
- **Sample data**: User data, test data
- **Custom marks**: Registration of test markers

## 🗄️ Database Testing

### Test Database
- **Type**: SQLite in-memory database
- **URL**: `sqlite:///./test.db`
- **Scope**: Session-level (recreated for each test session)
- **Cleanup**: Automatic after each test

### Database Fixtures
```python
@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    
@pytest.fixture
def test_session(test_engine):
    """Create test database session"""
```

## 🎭 Mocking

### Mock Strategy
- **Heavy mocking** for unit tests
- **Real database** for integration scenarios
- **Mock external services** (email, payment, etc.)

### Common Mocks
```python
@patch('api.logic.auth_logic.StorageService')
@patch('api.logic.auth_logic.AuthService')
@patch('api.logic.auth_logic.GmailEmailService')
def test_function(mock_email, mock_auth, mock_storage):
    pass
```

## 📝 Test Writing Guidelines

### Test Structure
```python
@pytest.mark.unit
@pytest.mark.auth
def test_function_name():
    """Test description"""
    # Arrange
    # Act
    # Assert
```

### Naming Conventions
- **Files**: `test_*.py`
- **Classes**: `Test*`
- **Methods**: `test_*`
- **Descriptive names**: `test_user_login_success`

### Assertions
```python
# Basic assertions
assert result == expected
assert response.status_code == 200
assert "success" in response.json()["message"]

# Exception testing
with pytest.raises(ValueError):
    function_that_raises_error()

# Mock verification
mock_service.method.assert_called_once()
mock_service.method.assert_called_with(expected_args)
```

## 🚨 Common Issues

### Database Issues
- **Unique constraint violations**: Use unique test data
- **Session isolation**: Each test gets a fresh session
- **Transaction rollback**: Automatic after each test

### Import Issues
- **Module not found**: Ensure proper PYTHONPATH
- **Circular imports**: Use lazy imports in tests

### Mock Issues
- **Mock not working**: Check import path in patch decorator
- **Assertion failures**: Verify mock was called correctly

## 🔍 Debugging Tests

### Verbose Output
```bash
poetry run pytest tests/ -v -s
```

### Debug Specific Test
```bash
poetry run pytest tests/auth/test_auth_service.py::TestAuthService::test_hash_password -v -s
```

### Print Debug Info
```python
def test_debug():
    print("Debug info")
    assert True
```

## 📈 Test Metrics

### Current Status
- **Total Tests**: 248
- **Passing**: 246
- **Failing**: 2 (Google OAuth router tests)
- **Coverage**: 69%
- **Warnings**: 0

### Coverage Breakdown
- **Auth Service**: 85%
- **Auth Logic**: 66%
- **Router Tests**: 95%
- **Storage Models**: 97%
- **Email Service**: 68%

## 🧹 Maintenance

### Cleaning Up
```bash
# Remove coverage data
poetry run coverage erase

# Remove test database
rm test.db

# Remove HTML coverage reports
rm -rf htmlcov/

# Remove pytest cache
rm -rf .pytest_cache/
```

### Adding New Tests
1. Create test file in appropriate directory
2. Follow naming conventions
3. Add appropriate markers
4. Update this README if needed

### Test Validation
The `test_basic.py` file includes a comprehensive test structure validation that ensures:
- All test directories exist
- All test files exist
- Proper naming conventions
- Configuration files exist
- No integration directory (removed)

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [coverage.py Documentation](https://coverage.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites) 