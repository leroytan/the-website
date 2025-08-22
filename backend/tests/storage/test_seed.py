from unittest.mock import Mock, patch

import pytest
from api.storage.seed import seed_database


class TestSeed:
    """Test cases for database seeding functions"""

    @pytest.mark.unit
    @pytest.mark.storage
    @patch("api.storage.seed.seed_locations")
    @patch("api.storage.seed.seed_levels")
    @patch("api.storage.seed.seed_subjects")
    def test_seed_database_success(
        self, mock_seed_subjects, mock_seed_levels, mock_seed_locations
    ):
        """Test successful database seeding"""
        # Mock session
        mock_session = Mock()

        # Call function
        seed_database(mock_session)

        # Verify all seeding functions were called
        mock_seed_subjects.assert_called_once_with(mock_session)
        mock_seed_levels.assert_called_once_with(mock_session)
        mock_seed_locations.assert_called_once_with(mock_session)

    @pytest.mark.unit
    @pytest.mark.storage
    @patch("api.storage.seed.seed_locations")
    @patch("api.storage.seed.seed_levels")
    @patch("api.storage.seed.seed_subjects")
    def test_seed_database_exception_handling(
        self, mock_seed_subjects, mock_seed_levels, mock_seed_locations
    ):
        """Test database seeding with exception handling"""
        # Mock session
        mock_session = Mock()

        # Mock exception during seeding
        mock_seed_subjects.side_effect = Exception("Database error")

        # Call function and expect exception to be raised
        with pytest.raises(Exception, match="Database error"):
            seed_database(mock_session)
