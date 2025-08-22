from unittest.mock import Mock, patch

import pytest
from api.auth.auth_service import AuthService
from api.auth.models import TokenData
from api.index import app
from api.storage.models import Base, EmailVerificationStatus, User
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Register custom marks
def pytest_configure(config):
    """Register custom marks"""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "auth: Authentication related tests")
    config.addinivalue_line("markers", "logic: Business logic tests")
    config.addinivalue_line("markers", "models: Model tests")
    config.addinivalue_line("markers", "router: Router tests")
    config.addinivalue_line("markers", "services: Service layer tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "asyncio: pytest-asyncio plugin marker")
    config.addinivalue_line("markers", "core: Core application tests")
    config.addinivalue_line("markers", "common: Common utilities tests")
    config.addinivalue_line("markers", "storage: Storage layer tests")


# Test database URL - use SQLite for testing
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine"""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_session(test_engine):
    """Create a test database session"""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def mock_storage_service():
    """Mock the storage service"""
    with patch("api.storage.storage_service.StorageService") as mock:
        yield mock


@pytest.fixture
def mock_auth_service():
    """Mock the auth service"""
    with patch("api.auth.auth_service.AuthService") as mock:
        yield mock


@pytest.fixture
def mock_email_service():
    """Mock the email service"""
    with patch("api.services.email_service.GmailEmailService") as mock:
        yield mock


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User",
        "intends_to_be_tutor": False,
    }


@pytest.fixture
def sample_user(test_session, sample_user_data):
    """Create a sample user in the test database"""
    user = User(
        email=sample_user_data["email"],
        name=sample_user_data["name"],
        password_hash=AuthService.hash_password(sample_user_data["password"]),
        email_verification_status=EmailVerificationStatus.VERIFIED,
        token_version=0,
    )
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)
    return user


@pytest.fixture
def sample_pending_user(test_session, sample_user_data):
    """Create a sample pending user in the test database"""
    user = User(
        email="pending@example.com",
        name="Pending User",
        password_hash=AuthService.hash_password("password123"),
        email_verification_status=EmailVerificationStatus.PENDING,
        token_version=0,
    )
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)
    return user


@pytest.fixture
def sample_waitlisted_user(test_session):
    """Create a sample waitlisted user in the test database"""
    user = User(
        email="waitlisted@example.com",
        name="Waitlisted User",
        password_hash=AuthService.hash_password("password123"),
        email_verification_status=EmailVerificationStatus.WAITLISTED,
        token_version=0,
    )
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)
    return user


@pytest.fixture
def valid_token_pair(sample_user):
    """Create a valid token pair for testing"""
    token_data = TokenData(
        email=sample_user.email, token_version=sample_user.token_version
    )
    return AuthService.create_token_pair(token_data)


@pytest.fixture
def expired_token():
    """Create an expired token for testing"""
    # Create a token that expires in the past
    token_data = TokenData(email="test@example.com", token_version=0)
    return AuthService.create_token_pair(token_data, expires_in=-3600)


@pytest.fixture
def mock_google_auth():
    """Mock Google OAuth authentication"""
    with patch("api.auth.auth_service.AuthService.authenticate_google_user") as mock:
        mock.return_value = Mock(
            access_token="mock_access_token", refresh_token="mock_refresh_token"
        )
        yield mock


@pytest.fixture
def mock_settings():
    """Mock application settings"""
    with patch("api.config.settings") as mock_settings:
        mock_settings.google_client_id = "test_client_id"
        mock_settings.google_redirect_uri = (
            "http://localhost:8000/api/auth/google/callback"
        )
        mock_settings.frontend_domain = "http://localhost:3000"
        mock_settings.secret_key = "test_secret_key"
        mock_settings.algorithm = "HS256"
        mock_settings.access_token_expire_minutes = 30
        mock_settings.refresh_token_expire_days = 7
        yield mock_settings
