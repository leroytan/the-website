from unittest.mock import Mock, patch

import pytest
from api.logic.filter_logic import FilterLogic
from api.router.models import FilterChoice
from api.storage.models import Assignment, Level, Location, Subject, Tutor


class TestFilterLogic:
    """Test cases for FilterLogic class"""

    @pytest.mark.unit
    @pytest.mark.logic
    def test_parse_filters_empty_list(self):
        """Test parsing empty filter list"""
        filters = []
        result = FilterLogic.parse_filters(filters)
        assert result == {}

    @pytest.mark.unit
    @pytest.mark.logic
    def test_parse_filters_single_filter(self):
        """Test parsing single filter"""
        filters = ["subject_math"]
        result = FilterLogic.parse_filters(filters)
        assert result == {"subject": ["subject_math"]}

    @pytest.mark.unit
    @pytest.mark.logic
    def test_parse_filters_multiple_filters_same_type(self):
        """Test parsing multiple filters of same type"""
        filters = ["subject_math", "subject_science"]
        result = FilterLogic.parse_filters(filters)
        assert result == {"subject": ["subject_math", "subject_science"]}

    @pytest.mark.unit
    @pytest.mark.logic
    def test_parse_filters_multiple_filter_types(self):
        """Test parsing multiple filter types"""
        filters = ["subject_math", "level_beginner"]
        result = FilterLogic.parse_filters(filters)
        assert result == {"subject": ["subject_math"], "level": ["level_beginner"]}

    @pytest.mark.unit
    @pytest.mark.logic
    def test_parse_filters_mixed_types(self):
        """Test parsing mixed filter types"""
        filters = [
            "subject_math",
            "subject_science",
            "level_beginner",
            "level_intermediate",
        ]
        result = FilterLogic.parse_filters(filters)
        assert result == {
            "subject": ["subject_math", "subject_science"],
            "level": ["level_beginner", "level_intermediate"],
        }

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.filter_logic.StorageService")
    @patch("api.logic.filter_logic.Session")
    def test_get_filter_success(self, mock_session_class, mock_storage_service):
        """Test successful filter retrieval"""
        # Mock session
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        # Mock database response
        mock_row1 = Mock()
        mock_row1.filter_id = "1"
        mock_row1.name = "Mathematics"

        mock_row2 = Mock()
        mock_row2.filter_id = "2"
        mock_row2.name = "Science"

        mock_storage_service.find.return_value = [mock_row1, mock_row2]

        result = FilterLogic.get_filter(Subject)

        assert len(result) == 2
        assert result[0].id == "1"
        assert result[0].name == "Mathematics"
        assert result[1].id == "2"
        assert result[1].name == "Science"

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.filter_logic.StorageService")
    @patch("api.logic.filter_logic.Session")
    def test_get_filter_empty_result(self, mock_session_class, mock_storage_service):
        """Test filter retrieval with empty result"""
        # Mock session
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        # Mock empty database response
        mock_storage_service.find.return_value = []

        result = FilterLogic.get_filter(Subject)

        assert result == []

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.filter_logic.FilterLogic.get_filter")
    def test_get_filters_tutor(self, mock_get_filter):
        """Test getting filters for Tutor table"""
        # Mock filter responses
        mock_subjects = [FilterChoice(id="1", name="Math")]
        mock_levels = [FilterChoice(id="1", name="Beginner")]

        mock_get_filter.side_effect = (
            lambda table_class: mock_subjects if table_class == Subject else mock_levels
        )

        result = FilterLogic.get_filters(Tutor)

        assert "subjects" in result
        assert "levels" in result
        assert result["subjects"] == mock_subjects
        assert result["levels"] == mock_levels

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.filter_logic.FilterLogic.get_filter")
    def test_get_filters_assignment(self, mock_get_filter):
        """Test getting filters for Assignment table"""
        # Mock filter responses
        mock_subjects = [FilterChoice(id="1", name="Math")]
        mock_levels = [FilterChoice(id="1", name="Beginner")]
        mock_locations = [FilterChoice(id="1", name="Singapore")]

        def mock_get_filter_side_effect(table_class):
            if table_class == Subject:
                return mock_subjects
            elif table_class == Level:
                return mock_levels
            elif table_class == Location:
                return mock_locations
            return []

        mock_get_filter.side_effect = mock_get_filter_side_effect

        result = FilterLogic.get_filters(Assignment)

        assert "subjects" in result
        assert "levels" in result
        assert "locations" in result
        assert "courses" in result
        assert result["subjects"] == mock_subjects
        assert result["levels"] == mock_levels
        assert result["locations"] == mock_locations
        assert result["courses"] == []

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_filters_unsupported_table(self):
        """Test getting filters for unsupported table"""

        class UnsupportedTable:
            pass

        result = FilterLogic.get_filters(UnsupportedTable)
        assert result == {}

    @pytest.mark.unit
    @pytest.mark.logic
    def test_parse_filters_invalid_format(self):
        """Test parsing filters with invalid format"""
        filters = ["invalidfilter"]  # No underscore

        with pytest.raises(ValueError, match="not enough values to unpack"):
            FilterLogic.parse_filters(filters)
