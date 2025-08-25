from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest
from api.logic.assignment_logic import AssignmentLogic, ViewType
from api.storage.models import (
    Assignment,
    AssignmentRequest,
    AssignmentRequestStatus,
    AssignmentSlot,
    AssignmentStatus,
    Level,
    Location,
    Subject,
)
from fastapi import HTTPException


class TestAssignmentLogicSimple:
    """Simple tests for AssignmentLogic that work with the actual API"""

    @pytest.mark.unit
    @pytest.mark.logic
    def test_view_type_enum_values(self):
        """Test ViewType enum values"""
        assert ViewType.OWNER.value == "owner"
        assert ViewType.PUBLIC.value == "public"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_convert_assignment_to_view_public_simple(self):
        """Test converting assignment to public view with minimal mocking"""
        # Create mock session
        mock_session = Mock()

        # Create mock assignment with minimal required attributes
        mock_assignment = Mock(spec=Assignment)
        mock_assignment.id = 1
        mock_assignment.created_at = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_assignment.updated_at = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_assignment.title = "Math Tutoring"
        mock_assignment.owner_id = 123
        mock_assignment.estimated_rate_hourly = 50
        mock_assignment.lesson_duration = 60
        mock_assignment.weekly_frequency = 2
        mock_assignment.special_requests = "Need help with calculus"
        mock_assignment.status = AssignmentStatus.OPEN
        mock_assignment.available_slots = []
        mock_assignment.subjects = []
        mock_assignment.assignment_requests = []

        # Mock level and location
        mock_level = Mock(spec=Level)
        mock_level.name = "University"
        mock_assignment.level = mock_level

        mock_location = Mock(spec=Location)
        mock_location.name = "Singapore"
        mock_assignment.location = mock_location

        # Call function
        result = AssignmentLogic.convert_assignment_to_view(
            mock_session, mock_assignment, ViewType.PUBLIC
        )

        # Verify result
        assert result.id == 1
        assert result.title == "Math Tutoring"
        assert result.owner_id == 123
        assert result.estimated_rate_hourly == 50
        assert result.lesson_duration == 60
        assert result.weekly_frequency == 2
        assert result.special_requests == "Need help with calculus"
        assert result.status == "OPEN"  # Enum value as string
        assert result.subjects == []
        assert result.level == "University"
        assert result.location == "Singapore"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_convert_assignment_to_view_with_subjects(self):
        """Test converting assignment with subjects"""
        # Create mock session
        mock_session = Mock()

        # Create mock assignment
        mock_assignment = Mock(spec=Assignment)
        mock_assignment.id = 1
        mock_assignment.created_at = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_assignment.updated_at = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_assignment.title = "Math Tutoring"
        mock_assignment.owner_id = 123
        mock_assignment.estimated_rate_hourly = 50
        mock_assignment.lesson_duration = 60
        mock_assignment.weekly_frequency = 2
        mock_assignment.special_requests = "Need help with calculus"
        mock_assignment.status = AssignmentStatus.OPEN
        mock_assignment.available_slots = []
        mock_assignment.assignment_requests = []

        # Mock subjects
        mock_subject1 = Mock(spec=Subject)
        mock_subject1.name = "Mathematics"
        mock_subject2 = Mock(spec=Subject)
        mock_subject2.name = "Physics"
        mock_assignment.subjects = [mock_subject1, mock_subject2]

        # Mock level and location
        mock_level = Mock(spec=Level)
        mock_level.name = "University"
        mock_assignment.level = mock_level

        mock_location = Mock(spec=Location)
        mock_location.name = "Singapore"
        mock_assignment.location = mock_location

        # Call function
        result = AssignmentLogic.convert_assignment_to_view(
            mock_session, mock_assignment, ViewType.PUBLIC
        )

        # Verify result
        assert result.subjects == ["Mathematics", "Physics"]

    @pytest.mark.unit
    @pytest.mark.logic
    def test_convert_assignment_to_view_with_slots(self):
        """Test converting assignment with available slots"""
        # Create mock session
        mock_session = Mock()

        # Create mock assignment
        mock_assignment = Mock(spec=Assignment)
        mock_assignment.id = 1
        mock_assignment.created_at = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_assignment.updated_at = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_assignment.title = "Math Tutoring"
        mock_assignment.owner_id = 123
        mock_assignment.estimated_rate_hourly = 50
        mock_assignment.lesson_duration = 60
        mock_assignment.weekly_frequency = 2
        mock_assignment.special_requests = "Need help with calculus"
        mock_assignment.status = AssignmentStatus.OPEN
        mock_assignment.subjects = []
        mock_assignment.assignment_requests = []

        # Mock available slots
        mock_slot1 = Mock(spec=AssignmentSlot)
        mock_slot1.id = 1
        mock_slot1.day = "Monday"
        mock_slot1.start_time = "10:00"
        mock_slot1.end_time = "11:00"

        mock_slot2 = Mock(spec=AssignmentSlot)
        mock_slot2.id = 2
        mock_slot2.day = "Wednesday"
        mock_slot2.start_time = "14:00"
        mock_slot2.end_time = "15:00"

        mock_assignment.available_slots = [mock_slot1, mock_slot2]

        # Mock level and location
        mock_level = Mock(spec=Level)
        mock_level.name = "University"
        mock_assignment.level = mock_level

        mock_location = Mock(spec=Location)
        mock_location.name = "Singapore"
        mock_assignment.location = mock_location

        # Call function
        result = AssignmentLogic.convert_assignment_to_view(
            mock_session, mock_assignment, ViewType.PUBLIC
        )

        # Verify result
        assert len(result.available_slots) == 2
        assert result.available_slots[0].id == 1
        assert result.available_slots[0].day == "Monday"
        assert result.available_slots[0].start_time == "10:00"
        assert result.available_slots[0].end_time == "11:00"
        assert result.available_slots[1].id == 2
        assert result.available_slots[1].day == "Wednesday"
        assert result.available_slots[1].start_time == "14:00"
        assert result.available_slots[1].end_time == "15:00"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_convert_assignment_to_view_owner_applied(self):
        """Test converting assignment to public view when user has applied"""
        # Create mock session
        mock_session = Mock()

        # Create mock assignment
        mock_assignment = Mock(spec=Assignment)
        mock_assignment.id = 1
        mock_assignment.created_at = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_assignment.updated_at = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_assignment.title = "Math Tutoring"
        mock_assignment.owner_id = 123
        mock_assignment.estimated_rate_hourly = 50
        mock_assignment.lesson_duration = 60
        mock_assignment.weekly_frequency = 2
        mock_assignment.special_requests = "Need help with calculus"
        mock_assignment.status = AssignmentStatus.OPEN
        mock_assignment.available_slots = []
        mock_assignment.subjects = []

        # Mock assignment request for user 456
        mock_request = Mock(spec=AssignmentRequest)
        mock_request.tutor_id = 456
        mock_request.status = AssignmentRequestStatus.PENDING
        mock_assignment.assignment_requests = [mock_request]

        # Mock level and location
        mock_level = Mock(spec=Level)
        mock_level.name = "University"
        mock_assignment.level = mock_level

        mock_location = Mock(spec=Location)
        mock_location.name = "Singapore"
        mock_assignment.location = mock_location

        # Call function with user_id 456 (who has applied)
        result = AssignmentLogic.convert_assignment_to_view(
            mock_session, mock_assignment, ViewType.PUBLIC, user_id=456
        )

        # Verify result shows user has applied
        assert result.applied is True
        assert result.request_status.value == "PENDING"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_convert_assignment_to_view_owner_cannot_apply(self):
        """Test that assignment owner cannot apply to their own assignment"""
        # Create mock session
        mock_session = Mock()

        # Create mock assignment
        mock_assignment = Mock(spec=Assignment)
        mock_assignment.id = 1
        mock_assignment.created_at = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_assignment.updated_at = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_assignment.title = "Math Tutoring"
        mock_assignment.owner_id = 123
        mock_assignment.estimated_rate_hourly = 50
        mock_assignment.lesson_duration = 60
        mock_assignment.weekly_frequency = 2
        mock_assignment.special_requests = "Need help with calculus"
        mock_assignment.status = AssignmentStatus.OPEN
        mock_assignment.available_slots = []
        mock_assignment.subjects = []
        mock_assignment.assignment_requests = []

        # Mock level and location
        mock_level = Mock(spec=Level)
        mock_level.name = "University"
        mock_assignment.level = mock_level

        mock_location = Mock(spec=Location)
        mock_location.name = "Singapore"
        mock_assignment.location = mock_location

        # Call function with owner_id as user_id
        result = AssignmentLogic.convert_assignment_to_view(
            mock_session, mock_assignment, ViewType.PUBLIC, user_id=123
        )

        # Verify result shows owner cannot apply
        assert result.applied is True
        assert result.request_status.value == "REJECTED"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_convert_assignment_to_view_user_not_applied(self):
        """Test converting assignment when user has not applied"""
        # Create mock session
        mock_session = Mock()

        # Create mock assignment
        mock_assignment = Mock(spec=Assignment)
        mock_assignment.id = 1
        mock_assignment.created_at = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_assignment.updated_at = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_assignment.title = "Math Tutoring"
        mock_assignment.owner_id = 123
        mock_assignment.estimated_rate_hourly = 50
        mock_assignment.lesson_duration = 60
        mock_assignment.weekly_frequency = 2
        mock_assignment.special_requests = "Need help with calculus"
        mock_assignment.status = AssignmentStatus.OPEN
        mock_assignment.available_slots = []
        mock_assignment.subjects = []
        mock_assignment.assignment_requests = []

        # Mock level and location
        mock_level = Mock(spec=Level)
        mock_level.name = "University"
        mock_assignment.level = mock_level

        mock_location = Mock(spec=Location)
        mock_location.name = "Singapore"
        mock_assignment.location = mock_location

        # Call function with user_id 999 (who has not applied)
        result = AssignmentLogic.convert_assignment_to_view(
            mock_session, mock_assignment, ViewType.PUBLIC, user_id=999
        )

        # Verify result shows user has not applied
        assert result.applied is False
        assert result.request_status.value == "NOT_SUBMITTED"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_assignment_by_id_success(self):
        """Test getting assignment by ID successfully"""
        with patch("api.logic.assignment_logic.StorageService.engine") as mock_engine:
            with patch("api.logic.assignment_logic.Session") as mock_session_class:
                with patch(
                    "api.logic.assignment_logic.StorageService.find"
                ) as mock_find:
                    # Mock assignment
                    mock_assignment = Mock(spec=Assignment)
                    mock_assignment.id = 1
                    mock_assignment.owner_id = 123
                    mock_find.return_value = mock_assignment

                    # Mock session
                    mock_session = Mock()
                    mock_session_class.return_value.__enter__.return_value = (
                        mock_session
                    )

                    # Mock convert_assignment_to_view
                    with patch(
                        "api.logic.assignment_logic.AssignmentLogic.convert_assignment_to_view"
                    ) as mock_convert:
                        mock_convert.return_value = Mock()

                        result = AssignmentLogic.get_assignment_by_id(1, user_id=123)

                        assert result is not None
                        mock_find.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_assignment_by_id_not_found(self):
        """Test getting assignment by ID when not found"""
        with patch("api.logic.assignment_logic.StorageService.engine") as mock_engine:
            with patch("api.logic.assignment_logic.Session") as mock_session_class:
                with patch(
                    "api.logic.assignment_logic.StorageService.find"
                ) as mock_find:
                    # Mock assignment not found
                    mock_find.return_value = None

                    # Mock session
                    mock_session = Mock()
                    mock_session_class.return_value.__enter__.return_value = (
                        mock_session
                    )

                    with pytest.raises(HTTPException) as exc_info:
                        AssignmentLogic.get_assignment_by_id(999)

                    assert exc_info.value.status_code == 404
                    assert exc_info.value.detail == "Assignment not found"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_created_assignments(self):
        """Test getting assignments created by user"""
        with patch("api.logic.assignment_logic.StorageService.engine") as mock_engine:
            with patch("api.logic.assignment_logic.Session") as mock_session_class:
                with patch(
                    "api.logic.assignment_logic.StorageService.find"
                ) as mock_find:
                    # Mock assignments
                    mock_assignment1 = Mock(spec=Assignment)
                    mock_assignment1.id = 1
                    mock_assignment2 = Mock(spec=Assignment)
                    mock_assignment2.id = 2
                    mock_find.return_value = [mock_assignment1, mock_assignment2]

                    # Mock session
                    mock_session = Mock()
                    mock_session_class.return_value.__enter__.return_value = (
                        mock_session
                    )

                    # Mock convert_assignment_to_view
                    with patch(
                        "api.logic.assignment_logic.AssignmentLogic.convert_assignment_to_view"
                    ) as mock_convert:
                        mock_convert.return_value = Mock()

                        result = AssignmentLogic.get_created_assignments(123)

                        assert len(result) == 2
                        mock_find.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_created_assignments_empty(self):
        """Test getting assignments created by user when none exist"""
        with patch("api.logic.assignment_logic.StorageService.engine") as mock_engine:
            with patch("api.logic.assignment_logic.Session") as mock_session_class:
                with patch(
                    "api.logic.assignment_logic.StorageService.find"
                ) as mock_find:
                    # Mock no assignments
                    mock_find.return_value = None

                    # Mock session
                    mock_session = Mock()
                    mock_session_class.return_value.__enter__.return_value = (
                        mock_session
                    )

                    result = AssignmentLogic.get_created_assignments(123)

                    assert result == []

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_applied_assignments(self):
        """Test getting assignments applied by user"""
        with patch("api.logic.assignment_logic.StorageService.engine") as mock_engine:
            with patch("api.logic.assignment_logic.Session") as mock_session_class:
                # Mock session and query
                mock_session = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session

                # Mock assignments
                mock_assignment1 = Mock(spec=Assignment)
                mock_assignment1.id = 1
                mock_assignment2 = Mock(spec=Assignment)
                mock_assignment2.id = 2

                # Mock query chain
                mock_query = Mock()
                mock_session.query.return_value = mock_query
                mock_query.join.return_value = mock_query
                mock_query.filter.return_value = mock_query
                mock_query.all.return_value = [mock_assignment1, mock_assignment2]

                # Mock convert_assignment_to_view
                with patch(
                    "api.logic.assignment_logic.AssignmentLogic.convert_assignment_to_view"
                ) as mock_convert:
                    mock_convert.return_value = Mock()

                    result = AssignmentLogic.get_applied_assignments(123)

                    assert len(result) == 2
                    mock_query.all.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_applied_assignments_empty(self):
        """Test getting assignments applied by user when none exist"""
        with patch("api.logic.assignment_logic.StorageService.engine") as mock_engine:
            with patch("api.logic.assignment_logic.Session") as mock_session_class:
                # Mock session and query
                mock_session = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session

                # Mock query chain
                mock_query = Mock()
                mock_session.query.return_value = mock_query
                mock_query.join.return_value = mock_query
                mock_query.filter.return_value = mock_query
                mock_query.all.return_value = []

                result = AssignmentLogic.get_applied_assignments(123)

                assert result == []

    @pytest.mark.unit
    @pytest.mark.logic
    def test_accept_assignment_request_success(self):
        """Test accepting assignment request successfully"""
        with patch("api.logic.assignment_logic.StorageService.engine") as mock_engine:
            with patch("api.logic.assignment_logic.Session") as mock_session_class:
                # Mock session
                mock_session = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session

                # Mock assignment request
                mock_request = Mock(spec=AssignmentRequest)
                mock_request.id = 1
                mock_request.status = AssignmentRequestStatus.PENDING
                mock_request.tutor_id = 456

                # Mock assignment
                mock_assignment = Mock(spec=Assignment)
                mock_assignment.id = 1
                mock_assignment.owner_id = 123
                mock_assignment.status = AssignmentStatus.OPEN
                mock_assignment.assignment_requests = [mock_request]
                mock_request.assignment = mock_assignment

                # Mock query
                mock_query = Mock()
                mock_session.query.return_value = mock_query
                mock_query.filter_by.return_value = mock_query
                mock_query.first.return_value = mock_request

                result = AssignmentLogic.accept_assignment_request(1)

                assert result == (123, 456)
                assert mock_assignment.status == AssignmentStatus.FILLED
                assert mock_assignment.tutor_id == 456
                assert mock_request.status == AssignmentRequestStatus.ACCEPTED
                mock_session.commit.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    def test_accept_assignment_request_not_found(self):
        """Test accepting assignment request when not found"""
        with patch("api.logic.assignment_logic.StorageService.engine") as mock_engine:
            with patch("api.logic.assignment_logic.Session") as mock_session_class:
                # Mock session
                mock_session = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session

                # Mock query
                mock_query = Mock()
                mock_session.query.return_value = mock_query
                mock_query.filter_by.return_value = mock_query
                mock_query.first.return_value = None

                with pytest.raises(HTTPException) as exc_info:
                    AssignmentLogic.accept_assignment_request(999)

                assert exc_info.value.status_code == 404
                assert exc_info.value.detail == "Assignment request not found"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_accept_assignment_request_not_pending(self):
        """Test accepting assignment request that is not pending"""
        with patch("api.logic.assignment_logic.StorageService.engine") as mock_engine:
            with patch("api.logic.assignment_logic.Session") as mock_session_class:
                # Mock session
                mock_session = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session

                # Mock assignment request
                mock_request = Mock(spec=AssignmentRequest)
                mock_request.id = 1
                mock_request.status = AssignmentRequestStatus.ACCEPTED

                # Mock query
                mock_query = Mock()
                mock_session.query.return_value = mock_query
                mock_query.filter_by.return_value = mock_query
                mock_query.first.return_value = mock_request

                with pytest.raises(HTTPException) as exc_info:
                    AssignmentLogic.accept_assignment_request(1)

                assert exc_info.value.status_code == 409
                assert "not pending" in exc_info.value.detail

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_assignment_owner_id(self):
        """Test getting assignment owner ID"""
        with patch("api.logic.assignment_logic.StorageService.engine") as mock_engine:
            with patch("api.logic.assignment_logic.Session") as mock_session_class:
                # Mock session
                mock_session = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session

                # Mock assignment request
                mock_request = Mock(spec=AssignmentRequest)
                mock_request.id = 1

                # Mock assignment
                mock_assignment = Mock(spec=Assignment)
                mock_assignment.owner_id = 123
                mock_request.assignment = mock_assignment

                # Mock query
                mock_query = Mock()
                mock_session.query.return_value = mock_query
                mock_query.options.return_value = mock_query
                mock_query.filter_by.return_value = mock_query
                mock_query.first.return_value = mock_request

                result = AssignmentLogic.get_assignment_owner_id(1)

                assert result == 123

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_assignment_owner_id_request_not_found(self):
        """Test getting assignment owner ID when request not found"""
        with patch("api.logic.assignment_logic.StorageService.engine") as mock_engine:
            with patch("api.logic.assignment_logic.Session") as mock_session_class:
                # Mock session
                mock_session = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session

                # Mock query
                mock_query = Mock()
                mock_session.query.return_value = mock_query
                mock_query.options.return_value = mock_query
                mock_query.filter_by.return_value = mock_query
                mock_query.first.return_value = None

                with pytest.raises(HTTPException) as exc_info:
                    AssignmentLogic.get_assignment_owner_id(999)

                assert exc_info.value.status_code == 404
                assert exc_info.value.detail == "Assignment request not found"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_lesson_duration(self):
        """Test getting lesson duration"""
        with patch("api.logic.assignment_logic.StorageService.engine") as mock_engine:
            with patch("api.logic.assignment_logic.Session") as mock_session_class:
                # Mock session
                mock_session = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session

                # Mock assignment request
                mock_request = Mock(spec=AssignmentRequest)
                mock_request.id = 1

                # Mock assignment
                mock_assignment = Mock(spec=Assignment)
                mock_assignment.lesson_duration = 60
                mock_request.assignment = mock_assignment

                # Mock query
                mock_query = Mock()
                mock_session.query.return_value = mock_query
                mock_query.options.return_value = mock_query
                mock_query.filter.return_value = mock_query
                mock_query.first.return_value = mock_request

                result = AssignmentLogic.get_lesson_duration(1)

                assert result == 60

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_request_hourly_rate(self):
        """Test getting request hourly rate"""
        with patch("api.logic.assignment_logic.StorageService.engine") as mock_engine:
            with patch("api.logic.assignment_logic.Session") as mock_session_class:
                # Mock session
                mock_session = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session

                # Mock assignment request
                mock_request = Mock(spec=AssignmentRequest)
                mock_request.id = 1
                mock_request.requested_rate_hourly = 50

                # Mock query
                mock_query = Mock()
                mock_session.query.return_value = mock_query
                mock_query.filter_by.return_value = mock_query
                mock_query.first.return_value = mock_request

                result = AssignmentLogic.get_request_hourly_rate(1)

                assert result == 50
