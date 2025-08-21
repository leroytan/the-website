import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation, ForeignKeyViolation

from api.logic.tutor_logic import TutorLogic
from api.router.models import NewTutorProfile, SearchQuery, TutorPublicSummary, TutorProfile
from api.storage.models import Tutor, User, Subject, Level, SpecialSkill


class TestTutorLogic:
    """Test cases for TutorLogic class"""

    @pytest.mark.unit
    @pytest.mark.logic
    def test_convert_tutor_to_public_summary_success(self):
        """Test successful conversion of tutor to public summary"""
        # Mock session
        mock_session = Mock()
        
        # Mock tutor
        mock_tutor = Mock()
        mock_tutor.id = 1
        mock_tutor.user.name = "Test Tutor"
        mock_tutor.highest_education = "Bachelor's"
        mock_tutor.min_rate = 30
        mock_tutor.max_rate = 50
        mock_tutor.rating = 4.5
        mock_tutor.about_me = "Experienced tutor"
        mock_tutor.resume_url = "https://example.com/resume"
        mock_tutor.experience = "5 years"
        mock_tutor.availability = "Weekdays"
        
        # Mock subjects
        mock_subject1 = Mock()
        mock_subject1.name = "Mathematics"
        mock_subject2 = Mock()
        mock_subject2.name = "Physics"
        mock_tutor.subjects = [mock_subject1, mock_subject2]
        
        # Mock levels
        mock_level1 = Mock()
        mock_level1.name = "Primary"
        mock_level2 = Mock()
        mock_level2.name = "Secondary"
        mock_tutor.levels = [mock_level1, mock_level2]
        
        # Mock special skills
        mock_skill1 = Mock()
        mock_skill1.name = "Special Education"
        mock_tutor.special_skills = [mock_skill1]
        
        # Mock session.merge to return the same tutor
        mock_session.merge.return_value = mock_tutor
        
        # Mock UserLogic
        with patch('api.logic.tutor_logic.UserLogic') as mock_user_logic:
            mock_user_logic.get_profile_photo_url.return_value = "https://example.com/photo.jpg"
            
            # Test the method
            result = TutorLogic.convert_tutor_to_public_summary(mock_session, mock_tutor)
            
            assert isinstance(result, TutorPublicSummary)
            assert result.id == 1
            assert result.name == "Test Tutor"
            assert result.highest_education == "Bachelor's"
            assert result.min_rate == 30
            assert result.max_rate == 50
            assert result.rating == 4.5
            assert result.subjects_teachable == ["Mathematics", "Physics"]
            assert result.levels_teachable == ["Primary", "Secondary"]
            assert result.special_skills == ["Special Education"]

    @pytest.mark.unit
    @pytest.mark.logic
    def test_convert_tutor_to_profile_success(self):
        """Test successful conversion of tutor to profile"""
        # Mock session
        mock_session = Mock()
        
        # Mock tutor
        mock_tutor = Mock()
        mock_tutor.id = 1
        mock_tutor.user.name = "Test Tutor"
        mock_tutor.user.email = "tutor@example.com"
        mock_tutor.highest_education = "Bachelor's"
        mock_tutor.min_rate = 30
        mock_tutor.max_rate = 50
        mock_tutor.location = "Singapore"
        mock_tutor.rating = 4.5
        mock_tutor.about_me = "Experienced tutor"
        mock_tutor.resume_url = "https://example.com/resume"
        mock_tutor.experience = "5 years"
        mock_tutor.availability = "Weekdays"
        
        # Mock subjects
        mock_subject1 = Mock()
        mock_subject1.name = "Mathematics"
        mock_tutor.subjects = [mock_subject1]
        
        # Mock levels
        mock_level1 = Mock()
        mock_level1.name = "Primary"
        mock_tutor.levels = [mock_level1]
        
        # Mock special skills
        mock_skill1 = Mock()
        mock_skill1.name = "Special Education"
        mock_tutor.special_skills = [mock_skill1]
        
        # Mock session.merge to return the same tutor
        mock_session.merge.return_value = mock_tutor
        
        # Mock UserLogic
        with patch('api.logic.tutor_logic.UserLogic') as mock_user_logic:
            mock_user_logic.get_profile_photo_url.return_value = "https://example.com/photo.jpg"
            
            # Test the method
            result = TutorLogic.convert_tutor_to_profile(mock_session, mock_tutor)
            
            assert isinstance(result, TutorProfile)
            assert result.id == 1
            assert result.name == "Test Tutor"
            assert result.email == "tutor@example.com"
            assert result.location == "Singapore"
            assert result.subjects_teachable == ["Mathematics"]
            assert result.levels_teachable == ["Primary"]
            assert result.special_skills == ["Special Education"]

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.tutor_logic.StorageService')
    @patch('api.logic.tutor_logic.FilterLogic')
    def test_search_tutors_success(self, mock_filter_logic, mock_storage_service):
        """Test successful tutor search"""
        # Mock storage service
        mock_storage_service.engine = Mock()
        
        # Mock session
        mock_session = Mock()
        
        # Mock search query
        search_query = SearchQuery(
            query="math",
            filter_by=["subject:mathematics", "level:primary"],
            sort_by="rating_desc",
            page_number=1,
            page_size=10
        )
        
        # Mock filter logic
        mock_filter_logic.parse_filters.return_value = {
            "subject": ["mathematics"],
            "level": ["primary"]
        }
        
        # Mock tutor
        mock_tutor = Mock()
        mock_tutor.id = 1
        mock_tutor.user.name = "Math Tutor"
        mock_tutor.rating = 4.5
        
        # Mock session context manager
        with patch('api.logic.tutor_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock query chain
            mock_statement = Mock()
            mock_session.query.return_value = mock_statement
            mock_statement.join.return_value = mock_statement
            mock_statement.filter.return_value = mock_statement
            mock_statement.order_by.return_value = mock_statement
            mock_statement.offset.return_value = mock_statement
            mock_statement.limit.return_value = mock_statement
            mock_statement.all.return_value = [mock_tutor]
            mock_statement.count.return_value = 1
            
            # Mock convert method
            with patch.object(TutorLogic, 'convert_tutor_to_public_summary') as mock_convert:
                mock_convert.return_value = TutorPublicSummary(
                    id=1, name="Math Tutor", photo_url="", highest_education="",
                    min_rate=0, max_rate=0, rating=4.5, about_me="",
                    subjects_teachable=[], levels_teachable=[], special_skills=[],
                    resume_url="", experience="", availability=""
                )
                
                # Test the method
                result = TutorLogic.search_tutors(search_query)
                
                assert "results" in result
                assert "num_pages" in result
                assert len(result["results"]) == 1
                assert result["num_pages"] == 1

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.tutor_logic.StorageService')
    def test_new_tutor_success(self, mock_storage_service):
        """Test successful tutor creation"""
        # Mock storage service
        mock_storage_service.engine = Mock()
        
        # Mock session
        mock_session = Mock()
        
        # Mock tutor profile
        tutor_profile = NewTutorProfile(
            highest_education="Bachelor's",
            min_rate=30,
            max_rate=50,
            location="Singapore",
            about_me="Experienced tutor",
            resume_url="https://example.com/resume",
            experience="5 years",
            availability="Weekdays",
            subjects_teachable=["Mathematics"],
            levels_teachable=["Primary"],
            special_skills=["Special Education"]
        )
        
        # Mock tutor
        mock_tutor = Mock()
        mock_tutor.id = 1
        
        # Mock subjects
        mock_subject = Mock()
        mock_subject.name = "Mathematics"
        
        # Mock levels
        mock_level = Mock()
        mock_level.name = "Primary"
        
        # Mock special skills
        mock_skill = Mock()
        mock_skill.name = "Special Education"
        
        # Mock session context manager
        with patch('api.logic.tutor_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock storage service insert
            mock_storage_service.insert.return_value = mock_tutor
            
            # Mock query chain for subjects, levels, and skills
            mock_session.query.return_value.filter.return_value.all.side_effect = [
                [mock_subject],  # subjects
                [mock_level],    # levels
                [mock_skill]     # special_skills
            ]
            
            # Mock convert method
            with patch.object(TutorLogic, 'convert_tutor_to_profile') as mock_convert:
                mock_convert.return_value = TutorProfile(
                    id=1, name="Test Tutor", contact="", email="", photo_url="",
                    highest_education="Bachelor's", min_rate=30, max_rate=50,
                    location="Singapore", rating=0, about_me="", subjects_teachable=[],
                    levels_teachable=[], special_skills=[], resume_url="",
                    experience="", availability=""
                )
                
                # Test the method
                result = TutorLogic.new_tutor(tutor_profile, 1)
                
                assert isinstance(result, TutorProfile)
                mock_storage_service.insert.assert_called_once()
                mock_session.commit.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    def test_new_tutor_unique_violation_error(self):
        """Test new_tutor with UniqueViolation error"""
        with patch('api.logic.tutor_logic.StorageService') as mock_storage:
            with patch('api.logic.tutor_logic.Session') as mock_session:
                # Mock the session context manager
                mock_session_instance = Mock()
                mock_session.return_value.__enter__.return_value = mock_session_instance
                mock_session.return_value.__exit__.return_value = None
                
                # Mock the insert to raise UniqueViolation
                mock_storage.insert.side_effect = IntegrityError("", "", UniqueViolation())
                
                tutor_profile = NewTutorProfile(
                    highest_education="PhD",
                    experience="5 years",
                    subjects_teachable=["Math"],
                    levels_teachable=["Primary"],
                    special_skills=["Advanced Mathematics"],
                    availability="Weekdays",
                    resume_url="https://example.com/resume",
                    min_rate=30,
                    max_rate=50,
                    location="Singapore",
                    about_me="Experienced tutor"
                )
                
                with pytest.raises(HTTPException) as exc_info:
                    TutorLogic.new_tutor(tutor_profile, 1)
                
                assert exc_info.value.status_code == 409
                assert "Tutor with this email already exists" in exc_info.value.detail

    @pytest.mark.unit
    @pytest.mark.logic
    def test_new_tutor_foreign_key_violation_error(self):
        """Test new_tutor with ForeignKeyViolation error"""
        with patch('api.logic.tutor_logic.StorageService') as mock_storage:
            with patch('api.logic.tutor_logic.Session') as mock_session:
                # Mock the session context manager
                mock_session_instance = Mock()
                mock_session.return_value.__enter__.return_value = mock_session_instance
                mock_session.return_value.__exit__.return_value = None
                
                # Mock the insert to raise ForeignKeyViolation
                mock_storage.insert.side_effect = IntegrityError("", "", ForeignKeyViolation())
                
                tutor_profile = NewTutorProfile(
                    highest_education="PhD",
                    experience="5 years",
                    subjects_teachable=["Math"],
                    levels_teachable=["Primary"],
                    special_skills=["Advanced Mathematics"],
                    availability="Weekdays",
                    resume_url="https://example.com/resume",
                    min_rate=30,
                    max_rate=50,
                    location="Singapore",
                    about_me="Experienced tutor"
                )
                
                with pytest.raises(HTTPException) as exc_info:
                    TutorLogic.new_tutor(tutor_profile, 1)
                
                assert exc_info.value.status_code == 409
                assert "User with this email does not exist" in exc_info.value.detail

    @pytest.mark.unit
    @pytest.mark.logic
    def test_new_tutor_other_integrity_error(self):
        """Test new_tutor with other IntegrityError"""
        with patch('api.logic.tutor_logic.StorageService') as mock_storage:
            with patch('api.logic.tutor_logic.Session') as mock_session:
                # Mock the session context manager
                mock_session_instance = Mock()
                mock_session.return_value.__enter__.return_value = mock_session_instance
                mock_session.return_value.__exit__.return_value = None
                
                # Mock the insert to raise a generic IntegrityError
                mock_storage.insert.side_effect = IntegrityError("", "", Exception())
                
                tutor_profile = NewTutorProfile(
                    highest_education="PhD",
                    experience="5 years",
                    subjects_teachable=["Math"],
                    levels_teachable=["Primary"],
                    special_skills=["Advanced Mathematics"],
                    availability="Weekdays",
                    resume_url="https://example.com/resume",
                    min_rate=30,
                    max_rate=50,
                    location="Singapore",
                    about_me="Experienced tutor"
                )
                
                with pytest.raises(HTTPException) as exc_info:
                    TutorLogic.new_tutor(tutor_profile, 1)
                
                assert exc_info.value.status_code == 500
                assert "Internal server error" in exc_info.value.detail

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.tutor_logic.StorageService')
    def test_find_profile_by_id_public_success(self, mock_storage_service):
        """Test successful tutor profile retrieval (public view)"""
        # Mock storage service
        mock_storage_service.engine = Mock()
        
        # Mock session
        mock_session = Mock()
        
        # Mock tutor
        mock_tutor = Mock()
        mock_tutor.id = 1
        mock_tutor.user.name = "Test Tutor"
        
        # Mock session context manager
        with patch('api.logic.tutor_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock storage service find
            mock_storage_service.find.return_value = mock_tutor
            
            # Mock convert method
            with patch.object(TutorLogic, 'convert_tutor_to_public_summary') as mock_convert:
                mock_convert.return_value = TutorPublicSummary(
                    id=1, name="Test Tutor", photo_url="", highest_education="",
                    min_rate=0, max_rate=0, rating=0, about_me="",
                    subjects_teachable=[], levels_teachable=[], special_skills=[],
                    resume_url="", experience="", availability=""
                )
                
                # Test the method
                result = TutorLogic.find_profile_by_id(1, is_self=False)
                
                assert isinstance(result, TutorPublicSummary)
                mock_storage_service.find.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.tutor_logic.StorageService')
    def test_find_profile_by_id_private_success(self, mock_storage_service):
        """Test successful tutor profile retrieval (private view)"""
        # Mock storage service
        mock_storage_service.engine = Mock()
        
        # Mock session
        mock_session = Mock()
        
        # Mock tutor
        mock_tutor = Mock()
        mock_tutor.id = 1
        mock_tutor.user.name = "Test Tutor"
        
        # Mock session context manager
        with patch('api.logic.tutor_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock storage service find
            mock_storage_service.find.return_value = mock_tutor
            
            # Mock convert method
            with patch.object(TutorLogic, 'convert_tutor_to_profile') as mock_convert:
                mock_convert.return_value = TutorProfile(
                    id=1, name="Test Tutor", contact="", email="", photo_url="",
                    highest_education="", min_rate=0, max_rate=0, location="",
                    rating=0, about_me="", subjects_teachable=[], levels_teachable=[],
                    special_skills=[], resume_url="", experience="", availability=""
                )
                
                # Test the method
                result = TutorLogic.find_profile_by_id(1, is_self=True)
                
                assert isinstance(result, TutorProfile)
                mock_storage_service.find.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.tutor_logic.StorageService')
    def test_find_profile_by_id_not_found(self, mock_storage_service):
        """Test tutor profile retrieval for non-existent tutor"""
        # Mock storage service
        mock_storage_service.engine = Mock()
        
        # Mock session context manager
        with patch('api.logic.tutor_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = Mock()
            
            # Mock storage service find returning None
            mock_storage_service.find.return_value = None
            
            # Test the method
            with pytest.raises(HTTPException) as exc_info:
                TutorLogic.find_profile_by_id(999, is_self=False)
            
            assert exc_info.value.status_code == 404
            assert "Tutor not found" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.tutor_logic.StorageService')
    def test_update_profile_success(self, mock_storage_service):
        """Test successful tutor profile update"""
        # Mock storage service
        mock_storage_service.engine = Mock()
        
        # Mock session
        mock_session = Mock()
        
        # Mock existing tutor
        mock_tutor = Mock()
        mock_tutor.id = 1
        mock_tutor.subjects = []
        mock_tutor.levels = []
        mock_tutor.special_skills = []
        
        # Mock tutor profile update
        tutor_profile = NewTutorProfile(
            highest_education="Master's",
            min_rate=40,
            max_rate=60,
            location="Singapore",
            about_me="Updated about me",
            resume_url="https://example.com/updated-resume",
            experience="7 years",
            availability="Weekends",
            subjects_teachable=["Physics"],
            levels_teachable=["Secondary"],
            special_skills=["Advanced Math"]
        )
        
        # Mock subjects
        mock_subject = Mock()
        mock_subject.name = "Physics"
        
        # Mock levels
        mock_level = Mock()
        mock_level.name = "Secondary"
        
        # Mock special skills
        mock_skill = Mock()
        mock_skill.name = "Advanced Math"
        
        # Mock session context manager
        with patch('api.logic.tutor_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock query chain
            mock_session.query.return_value.options.return_value.filter.return_value.first.return_value = mock_tutor
            
            # Mock query chain for subjects, levels, and skills
            mock_session.query.return_value.filter.return_value.all.side_effect = [
                [mock_subject],  # subjects
                [mock_level],    # levels
                [mock_skill]     # special_skills
            ]
            
            # Mock convert method
            with patch.object(TutorLogic, 'convert_tutor_to_profile') as mock_convert:
                mock_convert.return_value = TutorProfile(
                    id=1, name="Test Tutor", contact="", email="", photo_url="",
                    highest_education="Master's", min_rate=40, max_rate=60,
                    location="Singapore", rating=0, about_me="", subjects_teachable=[],
                    levels_teachable=[], special_skills=[], resume_url="",
                    experience="", availability=""
                )
                
                # Test the method
                result = TutorLogic.update_profile(tutor_profile, 1)
                
                assert isinstance(result, TutorProfile)
                mock_session.commit.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.tutor_logic.StorageService')
    def test_update_profile_not_found(self, mock_storage_service):
        """Test tutor profile update for non-existent tutor"""
        # Mock storage service
        mock_storage_service.engine = Mock()
        
        # Mock session
        mock_session = Mock()
        
        # Mock tutor profile update
        tutor_profile = NewTutorProfile(
            highest_education="Master's",
            min_rate=40,
            max_rate=60,
            location="Singapore",
            about_me="Updated about me",
            resume_url="https://example.com/updated-resume",
            experience="7 years",
            availability="Weekends",
            subjects_teachable=["Physics"],
            levels_teachable=["Secondary"],
            special_skills=["Advanced Math"]
        )
        
        # Mock session context manager
        with patch('api.logic.tutor_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock query chain returning None
            mock_session.query.return_value.options.return_value.filter.return_value.first.return_value = None
            
            # Test the method
            with pytest.raises(HTTPException) as exc_info:
                TutorLogic.update_profile(tutor_profile, 999)
            
            assert exc_info.value.status_code == 404
            assert "Tutor not found" in str(exc_info.value.detail) 