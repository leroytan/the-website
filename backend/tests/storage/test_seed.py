from unittest.mock import Mock, patch

import pytest
from api.storage.seed import seed_database, seed_levels, seed_locations, seed_subjects


class TestSeed:
    """Test cases for database seeding functions"""

    @pytest.mark.unit
    @pytest.mark.storage
    def test_seed_subjects_basic(self):
        """Test basic subject seeding functionality"""
        mock_session = Mock()

        # Call function
        seed_subjects(mock_session)

        # Verify subjects were added
        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()

        # Verify the subjects list contains expected subjects
        call_args = mock_session.add_all.call_args[0][0]
        subject_names = [subject.name for subject in call_args]

        expected_subjects = [
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology",
            "English Literature",
            "Computer Science",
            "History",
            "Spanish",
            "Economics",
            "Music",
        ]

        assert len(call_args) == 10
        for expected_subject in expected_subjects:
            assert expected_subject in subject_names

    @pytest.mark.unit
    @pytest.mark.storage
    def test_seed_levels_basic(self):
        """Test basic level seeding functionality"""
        mock_session = Mock()

        # Call function
        seed_levels(mock_session)

        # Verify levels were added
        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()

        # Verify the levels list contains expected levels
        call_args = mock_session.add_all.call_args[0][0]
        level_names = [level.name for level in call_args]

        expected_levels = [
            "Primary 1",
            "Primary 2",
            "Primary 3",
            "Primary 4",
            "Primary 5",
            "Primary 6",
            # Temporarily excluded levels above Primary 6
            # "Secondary 1",
            # "Secondary 2",
            # "Secondary 3",
            # "Secondary 4",
            # "Secondary 5",
            # "Junior College 1",
            # "Junior College 2",
        ]

        assert len(call_args) == 6  # Only 6 levels now
        for expected_level in expected_levels:
            assert expected_level in level_names

    @pytest.mark.unit
    @pytest.mark.storage
    def test_seed_levels_sort_order(self):
        """Test that levels have correct sort order"""
        mock_session = Mock()

        # Call function
        seed_levels(mock_session)

        # Verify sort orders are sequential
        call_args = mock_session.add_all.call_args[0][0]
        sort_orders = [level.sort_order for level in call_args]

        # Sort orders should be 1 through 6 (temporarily)
        expected_orders = list(range(1, 7))
        assert sorted(sort_orders) == expected_orders

    @pytest.mark.unit
    @pytest.mark.storage
    def test_seed_locations_basic(self):
        """Test basic location seeding functionality"""
        mock_session = Mock()

        # Call function
        seed_locations(mock_session)

        # Verify locations were added
        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()

        # Verify locations list is not empty
        call_args = mock_session.add_all.call_args[0][0]
        assert len(call_args) > 0

        # Verify all locations are strings
        for location in call_args:
            assert hasattr(location, "name")
            assert isinstance(location.name, str)
            assert len(location.name) > 0

    @pytest.mark.unit
    @pytest.mark.storage
    def test_seed_locations_contains_expected_areas(self):
        """Test that location seeding includes expected Singapore areas"""
        mock_session = Mock()

        # Call function
        seed_locations(mock_session)

        # Verify some expected Singapore locations are included
        call_args = mock_session.add_all.call_args[0][0]
        location_names = [location.name for location in call_args]

        expected_locations = [
            "Ang Mo Kio",
            "Bedok North",
            "Bedok South",
            "Bishan",
            "Bukit Batok",
            "Bukit Merah",
            "Clementi",
            "Jurong East",
            "Orchard",
            "Tampines",
            "Woodlands",
        ]

        # Check that at least some expected locations are present
        found_locations = [loc for loc in expected_locations if loc in location_names]
        assert len(found_locations) >= 5, (
            f"Expected at least 5 common locations, found: {found_locations}"
        )

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

    @pytest.mark.unit
    @pytest.mark.storage
    def test_seed_subjects_empty_session(self):
        """Test subject seeding with mock session"""
        mock_session = Mock()

        # Call function
        seed_subjects(mock_session)

        # Verify session methods were called
        assert mock_session.add_all.called
        assert mock_session.commit.called

    @pytest.mark.unit
    @pytest.mark.storage
    def test_seed_levels_empty_session(self):
        """Test level seeding with mock session"""
        mock_session = Mock()

        # Call function
        seed_levels(mock_session)

        # Verify session methods were called
        assert mock_session.add_all.called
        assert mock_session.commit.called

    @pytest.mark.unit
    @pytest.mark.storage
    def test_seed_locations_empty_session(self):
        """Test location seeding with mock session"""
        mock_session = Mock()

        # Call function
        seed_locations(mock_session)

        # Verify session methods were called
        assert mock_session.add_all.called
        assert mock_session.commit.called
