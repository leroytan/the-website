from datetime import datetime, timezone

import pytest
from api.storage.models import (
    Assignment,
    AssignmentStatus,
    EmailVerificationStatus,
    Tutor,
    User,
    SpecialSkill,
    Subject,
    Level,
    Location,
    PrivateChat,
    ChatMessage,
)


class TestStorageModels:
    """Test cases for database storage models"""

    @pytest.mark.unit
    @pytest.mark.models
    def test_user_model_creation(self):
        """Test User model creation"""
        user = User(
            name="Test User",
            email="test@example.com",
            password_hash="hashed_password",
            email_verification_status=EmailVerificationStatus.VERIFIED,
            token_version=0,
            intends_to_be_tutor=False,
        )

        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.password_hash == "hashed_password"
        assert user.email_verification_status == EmailVerificationStatus.VERIFIED
        assert user.token_version == 0
        assert user.intends_to_be_tutor is False

    @pytest.mark.unit
    @pytest.mark.models
    def test_user_model_defaults(self):
        """Test User model with default values"""
        user = User(
            name="Test User",
            email="test@example.com",
            email_verification_status=EmailVerificationStatus.PENDING,
            token_version=0,
            intends_to_be_tutor=False,
        )

        assert user.email_verification_status == EmailVerificationStatus.PENDING
        assert user.token_version == 0
        assert user.intends_to_be_tutor is False

    @pytest.mark.unit
    @pytest.mark.models
    def test_tutor_model_creation(self):
        """Test Tutor model creation"""
        user = User(name="Test User", email="test@example.com")

        tutor = Tutor(
            id=user.id,
            highest_education="PhD",
            availability="Weekends",
            resume_url="https://example.com/resume.pdf",
            min_rate=50,
            max_rate=100,
            location="Singapore",
            rating=4.5,
            about_me="Experienced tutor",
            experience="5 years",
        )

        assert tutor.id == user.id
        assert tutor.highest_education == "PhD"
        assert tutor.availability == "Weekends"
        assert tutor.resume_url == "https://example.com/resume.pdf"
        assert tutor.min_rate == 50
        assert tutor.max_rate == 100
        assert tutor.location == "Singapore"
        assert tutor.rating == 4.5
        assert tutor.about_me == "Experienced tutor"
        assert tutor.experience == "5 years"

    @pytest.mark.unit
    @pytest.mark.models
    def test_assignment_model_creation(self):
        """Test Assignment model creation"""
        assignment = Assignment(
            title="Math Assignment", owner_id=1, status=AssignmentStatus.OPEN
        )

        assert assignment.title == "Math Assignment"
        assert assignment.owner_id == 1
        assert assignment.status == AssignmentStatus.OPEN

    @pytest.mark.unit
    @pytest.mark.models
    def test_email_verification_status_enum(self):
        """Test EmailVerificationStatus enum values"""
        assert EmailVerificationStatus.VERIFIED.value == "verified"
        assert EmailVerificationStatus.PENDING.value == "pending"
        assert EmailVerificationStatus.WAITLISTED.value == "waitlisted"

    @pytest.mark.unit
    @pytest.mark.models
    def test_assignment_status_enum(self):
        """Test AssignmentStatus enum values"""
        assert AssignmentStatus.OPEN.value == "OPEN"
        assert AssignmentStatus.FILLED.value == "FILLED"

    @pytest.mark.unit
    @pytest.mark.models
    def test_user_serialization(self):
        """Test User model serialization"""
        user = User(
            name="Test User",
            email="test@example.com",
            password_hash="hashed_password",
            email_verification_status=EmailVerificationStatus.VERIFIED,
            token_version=0,
        )

        # Test that the model can be serialized (SerializerMixin)
        serialized = user.to_dict()

        assert "name" in serialized
        assert "email" in serialized
        assert "email_verification_status" in serialized
        assert "token_version" in serialized
        # password_hash should not be in serialized output for security
        assert "password_hash" not in serialized

    @pytest.mark.unit
    @pytest.mark.models
    def test_assignment_serialization(self):
        """Test Assignment model serialization"""
        assignment = Assignment(
            title="Test Assignment", owner_id=1, status=AssignmentStatus.OPEN
        )

        # Test that the model can be serialized (SerializerMixin)
        serialized = assignment.to_dict()

        assert "title" in serialized
        assert "owner_id" in serialized
        assert "status" in serialized

    @pytest.mark.unit
    @pytest.mark.models
    def test_user_with_google_id(self):
        """Test User model with Google ID"""
        user = User(
            name="Test User",
            email="test@gmail.com",
            google_id="google_user_123",
            email_verification_status=EmailVerificationStatus.VERIFIED,
        )

        assert user.google_id == "google_user_123"
        assert user.password_hash is None  # Google users don't have password

    @pytest.mark.unit
    @pytest.mark.models
    def test_user_email_confirmation_fields(self):
        """Test User model email confirmation fields"""
        user = User(
            name="Test User",
            email="test@example.com",
            email_confirmation_token="confirmation_token_123",
            email_confirmation_token_expires_at=datetime.now(timezone.utc),
        )

        assert user.email_confirmation_token == "confirmation_token_123"
        assert user.email_confirmation_token_expires_at is not None

    @pytest.mark.unit
    @pytest.mark.models
    def test_user_password_reset_fields(self):
        """Test User model password reset fields"""
        user = User(
            name="Test User",
            email="test@example.com",
            password_reset_token="reset_token_123",
            password_reset_token_expires_at=datetime.now(timezone.utc),
        )

        assert user.password_reset_token == "reset_token_123"
        assert user.password_reset_token_expires_at is not None

    @pytest.mark.unit
    @pytest.mark.models
    def test_tutor_relationships(self):
        """Test Tutor model relationships"""
        user = User(name="Test User", email="test@example.com")

        tutor = Tutor(id=user.id, highest_education="PhD")

        # Add the relationship before testing
        tutor.user = user

        # Test that the relationship is set up correctly
        assert tutor.user == user
        assert user.tutor_role == tutor

    @pytest.mark.unit
    @pytest.mark.models
    def test_assignment_with_dates(self):
        """Test Assignment model with created/updated dates"""
        assignment = Assignment(
            title="Test Assignment", owner_id=1, status=AssignmentStatus.OPEN
        )

        # The Base model should automatically set created_at and updated_at
        # These are set by SQLAlchemy's server_default
        assert hasattr(assignment, "created_at")
        assert hasattr(assignment, "updated_at")

    @pytest.mark.unit
    @pytest.mark.models
    def test_special_skill_filter_id_hybrid_property(self):
        """Test SpecialSkill filter_id hybrid property"""
        skill = SpecialSkill(name="Advanced Mathematics")
        
        # Test the hybrid property (instance method)
        assert skill.filter_id == "special_skill_advanced_mathematics"
        
        # Test the hybrid property expression (class method)
        # This covers the @filter_id.expression decorator
        from sqlalchemy import select
        query = select(SpecialSkill).where(SpecialSkill.filter_id == "special_skill_advanced_mathematics")
        # The query should contain the concat and replace functions
        query_str = str(query)
        assert "concat" in query_str
        assert "replace" in query_str
        assert "lower" in query_str

    @pytest.mark.unit
    @pytest.mark.models
    def test_subject_filter_id_hybrid_property(self):
        """Test Subject filter_id hybrid property"""
        subject = Subject(name="Physics")
        
        # Test the hybrid property (instance method)
        assert subject.filter_id == "subject_physics"
        
        # Test the hybrid property expression (class method)
        # This covers the @filter_id.expression decorator
        from sqlalchemy import select
        query = select(Subject).where(Subject.filter_id == "subject_physics")
        # The query should contain the concat and replace functions
        query_str = str(query)
        assert "concat" in query_str
        assert "replace" in query_str
        assert "lower" in query_str

    @pytest.mark.unit
    @pytest.mark.models
    def test_level_filter_id_hybrid_property(self):
        """Test Level filter_id hybrid property"""
        level = Level(name="Primary 6")
        
        # Test the hybrid property (instance method)
        assert level.filter_id == "level_primary_6"
        
        # Test the hybrid property expression (class method)
        # This covers the @filter_id.expression decorator
        from sqlalchemy import select
        query = select(Level).where(Level.filter_id == "level_primary_6")
        # The query should contain the concat and replace functions
        query_str = str(query)
        assert "concat" in query_str
        assert "replace" in query_str
        assert "lower" in query_str

    @pytest.mark.unit
    @pytest.mark.models
    def test_location_filter_id_hybrid_property(self):
        """Test Location filter_id hybrid property"""
        location = Location(name="Central Area")
        
        # Test the hybrid property (instance method)
        assert location.filter_id == "location_central_area"
        
        # Test the hybrid property expression (class method)
        # This covers the @filter_id.expression decorator
        from sqlalchemy import select
        query = select(Location).where(Location.filter_id == "location_central_area")
        # The query should contain the concat and replace functions
        query_str = str(query)
        assert "concat" in query_str
        assert "replace" in query_str
        assert "lower" in query_str

    @pytest.mark.unit
    @pytest.mark.models
    def test_chat_message_receiver_id_hybrid_property(self):
        """Test ChatMessage receiver_id hybrid property"""
        # Create a chat with two users
        user1 = User(name="User 1", email="user1@example.com")
        user2 = User(name="User 2", email="user2@example.com")
        
        chat = PrivateChat(user1_id=1, user2_id=2)
        chat.user1 = user1
        chat.user2 = user2
        
        # Create a message from user1 to user2
        message = ChatMessage(
            content="Hello",
            sender_id=1,
            chat_id=1
        )
        message.chat = chat
        message.sender = user1
        
        # Test the hybrid property
        assert message.receiver_id == 2

    @pytest.mark.unit
    @pytest.mark.models
    def test_chat_message_receiver_hybrid_property(self):
        """Test ChatMessage receiver hybrid property"""
        # Create a chat with two users
        user1 = User(name="User 1", email="user1@example.com")
        user2 = User(name="User 2", email="user2@example.com")
        
        chat = PrivateChat(user1_id=1, user2_id=2)
        chat.user1 = user1
        chat.user2 = user2
        
        # Create a message from user1 to user2
        message = ChatMessage(
            content="Hello",
            sender_id=1,
            chat_id=1
        )
        message.chat = chat
        message.sender = user1
        
        # Test the hybrid property
        assert message.receiver == user2

    @pytest.mark.unit
    @pytest.mark.models
    def test_chat_message_receiver_id_from_chat_method(self):
        """Test ChatMessage receiver_id_from_chat method"""
        # Create a chat with two users
        user1 = User(name="User 1", email="user1@example.com")
        user2 = User(name="User 2", email="user2@example.com")
        
        chat = PrivateChat(user1_id=1, user2_id=2)
        chat.user1 = user1
        chat.user2 = user2
        
        # Create a message from user1 to user2
        message = ChatMessage(
            content="Hello",
            sender_id=1,
            chat_id=1
        )
        
        # Test the method directly
        assert message.receiver_id_from_chat(chat) == 2
        
        # Test with message from user2 to user1
        message2 = ChatMessage(
            content="Reply",
            sender_id=2,
            chat_id=1
        )
        assert message2.receiver_id_from_chat(chat) == 1
