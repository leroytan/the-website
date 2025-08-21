import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timedelta

from api.logic.assignment_logic import AssignmentLogic, ViewType
from api.storage.models import Assignment, User, Tutor, AssignmentStatus, AssignmentRequestStatus
from api.router.models import NewAssignment, NewAssignmentRequest, SearchQuery


class TestAssignmentLogic:
    """Test cases for AssignmentLogic class"""

    @pytest.mark.unit
    @pytest.mark.logic
    def test_new_assignment_success(self):
        """Test successful assignment creation"""
        # Mock assignment data
        assignment_data = Mock(spec=NewAssignment)
        assignment_data.title = "Test Assignment"
        assignment_data.level = "Primary"
        assignment_data.estimated_rate_hourly = 50
        assignment_data.lesson_duration = 60
        assignment_data.weekly_frequency = 2
        assignment_data.special_requests = "Test Description"
        assignment_data.location = "Singapore"
        assignment_data.subjects = ["Mathematics"]
        assignment_data.available_slots = []
        
        user_id = 1
        
        with patch('api.logic.assignment_logic.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock Level and Location queries
            mock_level = Mock()
            mock_level.id = 1
            mock_location = Mock()
            mock_location.id = 1
            
            mock_session.query.return_value.filter_by.return_value.one.side_effect = [
                mock_level, mock_location
            ]
            
            # Mock Subject query
            mock_subject = Mock()
            mock_session.query.return_value.filter.return_value.all.return_value = [mock_subject]
            
            # Mock assignment slot query
            mock_session.query.return_value.filter.return_value.all.return_value = []
            
            # Mock the actual assignment object that gets created
            with patch('api.logic.assignment_logic.Assignment') as mock_assignment_class:
                mock_assignment_instance = Mock()
                mock_assignment_instance.id = 1
                mock_assignment_instance.title = "Test Assignment"
                mock_assignment_instance.owner_id = user_id
                mock_assignment_instance.status = AssignmentStatus.OPEN
                mock_assignment_instance.available_slots = []
                mock_assignment_instance.subjects = [mock_subject]
                mock_assignment_instance.level = mock_level
                mock_assignment_instance.location = mock_location
                mock_assignment_instance.created_at = datetime.now()
                mock_assignment_instance.updated_at = datetime.now()
                mock_assignment_instance.estimated_rate_hourly = 50
                mock_assignment_instance.lesson_duration = 60
                mock_assignment_instance.weekly_frequency = 2
                mock_assignment_instance.special_requests = "Test Description"
                mock_assignment_instance.tutor_id = None
                mock_assignment_instance.assignment_requests = []
                mock_assignment_class.return_value = mock_assignment_instance
            
            mock_session.add.return_value = None
            mock_session.commit.return_value = None
            mock_session.refresh.return_value = None
            
            # Mock the convert_assignment_to_view method to avoid complex object creation
            with patch.object(AssignmentLogic, 'convert_assignment_to_view') as mock_convert:
                mock_convert.return_value = Mock()
                
                # Test assignment creation
                result = AssignmentLogic.new_assignment(assignment_data, user_id)
                
                assert result is not None
                mock_session.add.assert_called()
                mock_session.commit.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_assignment_by_id_success(self):
        """Test successful assignment retrieval by ID"""
        assignment_id = 1
        user_id = 1
        
        with patch('api.logic.assignment_logic.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock assignment
            mock_assignment = Mock()
            mock_assignment.id = assignment_id
            mock_assignment.title = "Test Assignment"
            mock_assignment.owner_id = user_id
            mock_assignment.status = AssignmentStatus.OPEN
            mock_assignment.available_slots = []
            mock_assignment.subjects = []
            mock_assignment.level = Mock()
            mock_assignment.level.name = "Primary"
            mock_assignment.location = Mock()
            mock_assignment.location.name = "Singapore"
            mock_assignment.created_at = datetime.now()
            mock_assignment.updated_at = datetime.now()
            mock_assignment.estimated_rate_hourly = 50
            mock_assignment.lesson_duration = 60
            mock_assignment.weekly_frequency = 2
            mock_assignment.special_requests = "Test Description"
            mock_assignment.tutor_id = None
            mock_assignment.assignment_requests = []
            
            with patch('api.logic.assignment_logic.StorageService.find') as mock_find:
                mock_find.return_value = mock_assignment
                
                # Test assignment retrieval
                result = AssignmentLogic.get_assignment_by_id(assignment_id, user_id)
                
                assert result is not None
                assert result.id == assignment_id
                assert result.title == "Test Assignment"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_assignment_by_id_not_found(self):
        """Test assignment retrieval with non-existent ID"""
        assignment_id = 999
        user_id = 1
        
        with patch('api.logic.assignment_logic.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            with patch('api.logic.assignment_logic.StorageService.find') as mock_find:
                mock_find.return_value = None
                
                # Test assignment retrieval with non-existent ID
                with pytest.raises(HTTPException) as exc_info:
                    AssignmentLogic.get_assignment_by_id(assignment_id, user_id)
                
                assert exc_info.value.status_code == 404

    @pytest.mark.unit
    @pytest.mark.logic
    def test_update_assignment_by_id_success(self):
        """Test successful assignment update"""
        assignment_id = 1
        user_id = 1
        
        # Mock assignment update data
        assignment_update = Mock(spec=NewAssignment)
        assignment_update.title = "Updated Assignment"
        assignment_update.level = "Secondary"
        assignment_update.estimated_rate_hourly = 75
        assignment_update.lesson_duration = 90
        assignment_update.weekly_frequency = 3
        assignment_update.special_requests = "Updated Description"
        assignment_update.location = "Malaysia"
        assignment_update.subjects = ["Physics"]
        assignment_update.available_slots = []
        assignment_update.model_dump.return_value = {
            "title": "Updated Assignment",
            "level": "Secondary",
            "estimated_rate_hourly": 75,
            "lesson_duration": 90,
            "weekly_frequency": 3,
            "special_requests": "Updated Description",
            "location": "Malaysia",
            "subjects": ["Physics"],
            "available_slots": []
        }
        
        # Mock authorization function
        def mock_assert_user_authorized(owner_id):
            assert owner_id == user_id
        
        with patch('api.logic.assignment_logic.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock Level query
            mock_level = Mock()
            mock_level.id = 2
            mock_session.query.return_value.filter_by.return_value.one.return_value = mock_level
            
            # Mock assignment
            mock_assignment = Mock()
            mock_assignment.id = assignment_id
            mock_assignment.owner_id = user_id
            mock_assignment.title = "Updated Assignment"
            mock_assignment.available_slots = []
            mock_assignment.subjects = []
            mock_assignment.level = mock_level
            mock_assignment.location = Mock()
            mock_assignment.location.name = "Malaysia"
            mock_assignment.created_at = datetime.now()
            mock_assignment.updated_at = datetime.now()
            mock_assignment.estimated_rate_hourly = 75
            mock_assignment.lesson_duration = 90
            mock_assignment.weekly_frequency = 3
            mock_assignment.special_requests = "Updated Description"
            mock_assignment.tutor_id = None
            mock_assignment.assignment_requests = []
            
            # Mock assignment slot with proper attributes
            mock_slot = Mock()
            mock_slot.id = 1
            mock_slot.day = "Monday"
            mock_slot.start_time = "09:00"
            mock_slot.end_time = "10:00"
            mock_assignment.available_slots = [mock_slot]
            
            with patch('api.logic.assignment_logic.StorageService.update') as mock_update:
                mock_update.return_value = mock_assignment
                
                # Mock Subject query
                mock_subject = Mock()
                mock_session.query.return_value.filter.return_value.all.return_value = [mock_subject]
                
                # Mock assignment slot operations
                with patch('api.logic.assignment_logic.StorageService.delete') as mock_delete:
                    with patch('api.logic.assignment_logic.StorageService.insert') as mock_insert:
                        mock_insert.return_value = Mock()
                        
                        # Mock the convert_assignment_to_view method to avoid complex object creation
                        with patch.object(AssignmentLogic, 'convert_assignment_to_view') as mock_convert:
                            mock_convert.return_value = Mock()
                            
                            # Test assignment update
                            result = AssignmentLogic.update_assignment_by_id(
                                assignment_id, assignment_update, mock_assert_user_authorized
                            )
                            
                            assert result is not None
                            mock_update.assert_called_once()
                            mock_session.commit.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    def test_request_assignment_success(self):
        """Test successful assignment request"""
        # Mock assignment request data
        assignment_request_data = Mock(spec=NewAssignmentRequest)
        assignment_request_data.assignment_id = 1
        assignment_request_data.requested_rate_hourly = 60
        assignment_request_data.requested_duration = 90
        assignment_request_data.available_slots = []
        
        tutor_id = 2
        origin = "web"
        
        with patch('api.logic.assignment_logic.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock assignment
            mock_assignment = Mock()
            mock_assignment.id = 1
            mock_assignment.status = AssignmentStatus.OPEN
            mock_assignment.tutor_id = None
            mock_assignment.owner_id = 1
            mock_assignment.owner = Mock()
            mock_assignment.owner.email = "owner@example.com"
            mock_assignment.title = "Test Assignment"
            
            mock_session.query.return_value.filter_by.return_value.options.return_value.first.return_value = mock_assignment
            
            # Mock assignment request
            mock_assignment_request = Mock()
            mock_assignment_request.id = 1
            
            mock_session.add.return_value = None
            mock_session.flush.return_value = None
            mock_session.commit.return_value = None
            
            with patch('api.logic.assignment_logic.GmailEmailService.notify_new_assignment_request') as mock_email:
                # Test assignment request
                AssignmentLogic.request_assignment(assignment_request_data, tutor_id, origin)
                
                mock_session.add.assert_called()
                mock_session.commit.assert_called_once()
                mock_email.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    def test_request_assignment_not_open(self):
        """Test assignment request when assignment is not open"""
        # Mock assignment request data
        assignment_request_data = Mock(spec=NewAssignmentRequest)
        assignment_request_data.assignment_id = 1
        
        tutor_id = 2
        origin = "web"
        
        with patch('api.logic.assignment_logic.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock assignment that is not open
            mock_assignment = Mock()
            mock_assignment.id = 1
            mock_assignment.status = AssignmentStatus.FILLED
            mock_assignment.tutor_id = 3
            
            mock_session.query.return_value.filter_by.return_value.options.return_value.first.return_value = mock_assignment
            
            # Test assignment request when not open
            with pytest.raises(HTTPException) as exc_info:
                AssignmentLogic.request_assignment(assignment_request_data, tutor_id, origin)
            
            assert exc_info.value.status_code == 400

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_created_assignments_success(self):
        """Test successful retrieval of created assignments"""
        user_id = 1
        
        with patch('api.logic.assignment_logic.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock assignments
            mock_assignment = Mock()
            mock_assignment.id = 1
            mock_assignment.title = "Test Assignment"
            mock_assignment.owner_id = user_id
            mock_assignment.status = AssignmentStatus.OPEN
            mock_assignment.available_slots = []
            mock_assignment.subjects = []
            mock_assignment.level = Mock()
            mock_assignment.level.name = "Primary"
            mock_assignment.location = Mock()
            mock_assignment.location.name = "Singapore"
            mock_assignment.created_at = datetime.now()
            mock_assignment.updated_at = datetime.now()
            mock_assignment.estimated_rate_hourly = 50
            mock_assignment.lesson_duration = 60
            mock_assignment.weekly_frequency = 2
            mock_assignment.special_requests = "Test Description"
            mock_assignment.tutor_id = None
            mock_assignment.assignment_requests = []
            
            with patch('api.logic.assignment_logic.StorageService.find') as mock_find:
                mock_find.return_value = [mock_assignment]
                
                # Test getting created assignments
                result = AssignmentLogic.get_created_assignments(user_id)
                
                assert len(result) == 1
                assert result[0].id == 1
                assert result[0].title == "Test Assignment"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_applied_assignments_success(self):
        """Test successful retrieval of applied assignments"""
        user_id = 1
        
        with patch('api.logic.assignment_logic.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock assignments
            mock_assignment = Mock()
            mock_assignment.id = 1
            mock_assignment.title = "Test Assignment"
            mock_assignment.owner_id = 2
            mock_assignment.status = AssignmentStatus.OPEN
            mock_assignment.available_slots = []
            mock_assignment.subjects = []
            mock_assignment.level = Mock()
            mock_assignment.level.name = "Primary"
            mock_assignment.location = Mock()
            mock_assignment.location.name = "Singapore"
            mock_assignment.created_at = datetime.now()
            mock_assignment.updated_at = datetime.now()
            mock_assignment.estimated_rate_hourly = 50
            mock_assignment.lesson_duration = 60
            mock_assignment.weekly_frequency = 2
            mock_assignment.special_requests = "Test Description"
            mock_assignment.tutor_id = None
            mock_assignment.assignment_requests = []
            
            mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = [mock_assignment]
            
            # Test getting applied assignments
            result = AssignmentLogic.get_applied_assignments(user_id)
            
            assert len(result) == 1
            assert result[0].id == 1
            assert result[0].title == "Test Assignment"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_accept_assignment_request_success(self):
        """Test successful assignment request acceptance"""
        assignment_request_id = 1
        
        with patch('api.logic.assignment_logic.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock assignment request
            mock_assignment_request = Mock()
            mock_assignment_request.id = assignment_request_id
            mock_assignment_request.status = AssignmentRequestStatus.PENDING
            mock_assignment_request.tutor_id = 2
            
            # Mock assignment
            mock_assignment = Mock()
            mock_assignment.id = 1
            mock_assignment.status = AssignmentStatus.OPEN
            mock_assignment.owner_id = 1
            mock_assignment.assignment_requests = [mock_assignment_request]
            
            mock_assignment_request.assignment = mock_assignment
            
            mock_session.query.return_value.filter_by.return_value.first.return_value = mock_assignment_request
            mock_session.commit.return_value = None
            
            # Test assignment request acceptance
            result = AssignmentLogic.accept_assignment_request(assignment_request_id)
            
            assert result == (1, 2)
            assert mock_assignment.status == AssignmentStatus.FILLED
            assert mock_assignment.tutor_id == 2
            assert mock_assignment_request.status == AssignmentRequestStatus.ACCEPTED
            mock_session.commit.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    def test_accept_assignment_request_not_pending(self):
        """Test assignment request acceptance when not pending"""
        assignment_request_id = 1
        
        with patch('api.logic.assignment_logic.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock assignment request that is not pending
            mock_assignment_request = Mock()
            mock_assignment_request.id = assignment_request_id
            mock_assignment_request.status = AssignmentRequestStatus.ACCEPTED
            
            mock_session.query.return_value.filter_by.return_value.first.return_value = mock_assignment_request
            
            # Test assignment request acceptance when not pending
            with pytest.raises(HTTPException) as exc_info:
                AssignmentLogic.accept_assignment_request(assignment_request_id)
            
            assert exc_info.value.status_code == 409

    @pytest.mark.unit
    @pytest.mark.logic
    def test_search_assignments_success(self):
        """Test successful assignment search"""
        # Mock search query
        search_query = Mock(spec=SearchQuery)
        search_query.query = "math"
        search_query.filter_by = "subject:Mathematics"
        search_query.sort_by = "created_at"
        search_query.page_number = 1
        search_query.page_size = 10
        
        user_id = 1
        
        with patch('api.logic.assignment_logic.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock query builder
            mock_statement = Mock()
            mock_session.query.return_value = mock_statement
            mock_statement.outerjoin.return_value = mock_statement
            mock_statement.filter.return_value = mock_statement
            mock_statement.order_by.return_value = mock_statement
            mock_statement.offset.return_value = mock_statement
            mock_statement.limit.return_value = mock_statement
            mock_statement.count.return_value = 5
            mock_statement.all.return_value = []
            
            with patch('api.logic.assignment_logic.FilterLogic.parse_filters') as mock_parse_filters:
                mock_parse_filters.return_value = {"subject": ["Mathematics"]}
                
                with patch('api.logic.assignment_logic.SortLogic.get_sorting') as mock_get_sorting:
                    mock_get_sorting.return_value = Mock()
                    
                    # Test assignment search
                    result = AssignmentLogic.search_assignments(search_query, user_id)
                    
                    assert result is not None
                    assert "results" in result
                    assert "num_pages" in result
                    assert result["num_pages"] == 1

    @pytest.mark.unit
    @pytest.mark.logic
    def test_convert_assignment_to_view_owner(self):
        """Test assignment conversion to owner view"""
        with patch('api.logic.assignment_logic.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock assignment
            mock_assignment = Mock()
            mock_assignment.id = 1
            mock_assignment.title = "Test Assignment"
            mock_assignment.owner_id = 1
            mock_assignment.status = AssignmentStatus.OPEN
            mock_assignment.available_slots = []
            mock_assignment.subjects = []
            mock_assignment.level = Mock()
            mock_assignment.level.name = "Primary"
            mock_assignment.location = Mock()
            mock_assignment.location.name = "Singapore"
            mock_assignment.created_at = datetime.now()
            mock_assignment.updated_at = datetime.now()
            mock_assignment.estimated_rate_hourly = 50
            mock_assignment.lesson_duration = 60
            mock_assignment.weekly_frequency = 2
            mock_assignment.special_requests = "Test Description"
            mock_assignment.tutor_id = None
            mock_assignment.assignment_requests = []
            
            mock_session.add.return_value = None
            
            # Test conversion to owner view
            result = AssignmentLogic.convert_assignment_to_view(
                mock_session, mock_assignment, ViewType.OWNER, 1
            )
            
            assert result is not None
            assert result.id == 1
            assert result.title == "Test Assignment"
            assert result.owner_id == 1

    @pytest.mark.unit
    @pytest.mark.logic
    def test_convert_assignment_to_view_public(self):
        """Test assignment conversion to public view"""
        with patch('api.logic.assignment_logic.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session
            
            # Mock assignment
            mock_assignment = Mock()
            mock_assignment.id = 1
            mock_assignment.title = "Test Assignment"
            mock_assignment.owner_id = 2
            mock_assignment.status = AssignmentStatus.OPEN
            mock_assignment.available_slots = []
            mock_assignment.subjects = []
            mock_assignment.level = Mock()
            mock_assignment.level.name = "Primary"
            mock_assignment.location = Mock()
            mock_assignment.location.name = "Singapore"
            mock_assignment.created_at = datetime.now()
            mock_assignment.updated_at = datetime.now()
            mock_assignment.estimated_rate_hourly = 50
            mock_assignment.lesson_duration = 60
            mock_assignment.weekly_frequency = 2
            mock_assignment.special_requests = "Test Description"
            mock_assignment.tutor_id = None
            mock_assignment.assignment_requests = []
            
            mock_session.add.return_value = None
            
            # Test conversion to public view
            result = AssignmentLogic.convert_assignment_to_view(
                mock_session, mock_assignment, ViewType.PUBLIC, 1
            )
            
            assert result is not None
            assert result.id == 1
            assert result.title == "Test Assignment"
            assert result.owner_id == 2 