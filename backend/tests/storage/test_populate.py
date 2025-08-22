import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, patch

from api.storage.populate import utc_now, generate_bulk_assignments


class TestPopulate:
    """Test cases for populate module"""

    @pytest.mark.unit
    @pytest.mark.storage
    def test_utc_now(self):
        """Test utc_now function returns current UTC datetime"""
        result = utc_now()

        assert isinstance(result, datetime)
        assert result.tzinfo == timezone.utc
        assert result.tzinfo is not None

    @pytest.mark.unit
    @pytest.mark.storage
    @patch("api.storage.populate.random")
    def test_generate_bulk_assignments_basic(self, mock_random):
        """Test generate_bulk_assignments with basic setup"""
        # Mock session
        mock_session = Mock()

        # Mock data
        mock_users = [Mock(), Mock()]
        mock_tutors = [Mock(), Mock()]
        mock_subjects = [Mock(name="Math"), Mock(name="Science")]
        mock_levels = [Mock(), Mock()]
        mock_locations = [Mock(), Mock()]

        # Mock random choices - need more calls for the full function
        mock_random.choice.side_effect = [
            mock_users[0],  # requester
            mock_tutors[0],  # assigned_tutor
            mock_levels[0],  # level
            mock_subjects[0],  # subject
            mock_locations[0],  # location
            "OPEN",  # status
            mock_tutors[0],  # assigned_tutor again
            "Need help with exam preparation",  # special_request
            ("Monday", "16:00", "18:00"),  # time_slot
            ("Wednesday", "18:00", "20:00"),  # time_slot
            ("Saturday", "10:00", "12:00"),  # time_slot
        ]

        # Call function
        result = generate_bulk_assignments(
            session=mock_session,
            users=mock_users,
            tutors=mock_tutors,
            subjects=mock_subjects,
            levels=mock_levels,
            locations=mock_locations,
            count=1,
            seed=42,
        )

        # Verify random.seed was called
        mock_random.seed.assert_called_once_with(42)

        # Verify random.choice was called multiple times
        assert mock_random.choice.call_count >= 6
