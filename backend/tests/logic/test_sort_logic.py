import pytest
from api.logic.sort_logic import SortLogic
from api.router.models import AssignmentSortField, SortChoice, SortOrder
from api.storage.models import Assignment, Tutor


class TestSortLogic:
    """Test cases for SortLogic class"""

    @pytest.mark.unit
    @pytest.mark.logic
    def test_parse_sort_id_empty_string(self):
        """Test parsing empty sort ID"""
        result = SortLogic.parse_sort_id("")
        assert result == ("", SortOrder.DESC)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_parse_sort_id_valid_format(self):
        """Test parsing valid sort ID format"""
        result = SortLogic.parse_sort_id("created_at_desc")
        assert result == ("created_at", SortOrder.DESC)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_parse_sort_id_asc_order(self):
        """Test parsing sort ID with ascending order"""
        result = SortLogic.parse_sort_id("title_asc")
        assert result == ("title", SortOrder.ASC)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_parse_sort_id_invalid_format(self):
        """Test parsing invalid sort ID format"""
        with pytest.raises(ValueError, match="Invalid sort_id format"):
            SortLogic.parse_sort_id("invalid")

    @pytest.mark.unit
    @pytest.mark.logic
    def test_parse_sort_id_case_insensitive_order(self):
        """Test parsing sort ID with case insensitive order"""
        result = SortLogic.parse_sort_id("level_ASC")
        assert result == ("level", SortOrder.ASC)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_sorting_assignment_created_at_desc(self):
        """Test getting sorting for assignment created_at desc"""
        result = SortLogic.get_sorting(Assignment, "created_at_desc")
        assert "created_at" in str(result)
        assert "DESC" in str(result)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_sorting_assignment_created_at_asc(self):
        """Test getting sorting for assignment created_at asc"""
        result = SortLogic.get_sorting(Assignment, "created_at_asc")
        assert "created_at" in str(result)
        assert "ASC" in str(result)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_sorting_assignment_rate_desc(self):
        """Test getting sorting for assignment rate desc"""
        result = SortLogic.get_sorting(Assignment, "estimated_rate_hourly_desc")
        assert "estimated_rate_hourly" in str(result)
        assert "DESC" in str(result)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_sorting_assignment_rate_asc(self):
        """Test getting sorting for assignment rate asc"""
        result = SortLogic.get_sorting(Assignment, "estimated_rate_hourly_asc")
        assert "estimated_rate_hourly" in str(result)
        assert "ASC" in str(result)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_sorting_assignment_weekly_frequency_desc(self):
        """Test getting sorting for assignment weekly_frequency desc"""
        result = SortLogic.get_sorting(Assignment, "weekly_frequency_desc")
        assert "weekly_frequency" in str(result)
        assert "DESC" in str(result)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_sorting_assignment_level_desc(self):
        """Test getting sorting for assignment level desc"""
        result = SortLogic.get_sorting(Assignment, "level_desc")
        assert "sort_order" in str(result)
        assert "DESC" in str(result)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_sorting_assignment_title_desc(self):
        """Test getting sorting for assignment title desc"""
        result = SortLogic.get_sorting(Assignment, "title_desc")
        assert "title" in str(result)
        assert "DESC" in str(result)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_sorting_assignment_location_unsupported(self):
        """Test getting sorting for assignment location (unsupported)"""
        with pytest.raises(ValueError, match="Location sorting is not supported yet"):
            SortLogic.get_sorting(Assignment, "location_asc")

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_sorting_assignment_relevance_unsupported(self):
        """Test getting sorting for assignment relevance (unsupported)"""
        with pytest.raises(ValueError, match="Relevance sorting is not supported yet"):
            SortLogic.get_sorting(Assignment, "relevance_desc")

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_sorting_unsupported_table(self):
        """Test getting sorting for unsupported table"""

        class UnsupportedTable:
            pass

        with pytest.raises(ValueError, match="Unsupported TableClass"):
            SortLogic.get_sorting(UnsupportedTable, "created_at_desc")

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_allowed_orders_created_at(self):
        """Test getting allowed orders for created_at field"""
        result = SortLogic.get_allowed_orders(AssignmentSortField.CREATED_AT)
        assert SortOrder.ASC in result
        assert SortOrder.DESC in result

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_allowed_orders_estimated_rate_hourly(self):
        """Test getting allowed orders for estimated_rate_hourly field"""
        result = SortLogic.get_allowed_orders(AssignmentSortField.estimated_rate_hourly)
        assert SortOrder.ASC in result
        assert SortOrder.DESC in result

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_allowed_orders_weekly_frequency(self):
        """Test getting allowed orders for weekly_frequency field"""
        result = SortLogic.get_allowed_orders(AssignmentSortField.WEEKLY_FREQUENCY)
        assert SortOrder.ASC in result
        assert SortOrder.DESC in result

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_allowed_orders_level(self):
        """Test getting allowed orders for level field"""
        result = SortLogic.get_allowed_orders(AssignmentSortField.LEVEL)
        assert SortOrder.ASC in result
        assert SortOrder.DESC in result

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_allowed_orders_title(self):
        """Test getting allowed orders for title field"""
        result = SortLogic.get_allowed_orders(AssignmentSortField.TITLE)
        assert SortOrder.ASC in result
        assert SortOrder.DESC in result

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_allowed_orders_relevance(self):
        """Test getting allowed orders for relevance field"""
        result = SortLogic.get_allowed_orders(AssignmentSortField.RELEVANCE)
        assert SortOrder.DESC in result
        assert SortOrder.ASC not in result

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_allowed_orders_location(self):
        """Test getting allowed orders for location field"""
        result = SortLogic.get_allowed_orders(AssignmentSortField.LOCATION)
        assert SortOrder.ASC in result
        assert SortOrder.DESC not in result

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_choices_created_at(self):
        """Test getting choices for created_at field"""
        result = SortLogic.get_choices(AssignmentSortField.CREATED_AT)
        assert len(result) == 2

        # Check for asc choice
        asc_choice = next((c for c in result if c.id == "created_at_asc"), None)
        assert asc_choice is not None
        assert asc_choice.name == "Created at (Asc)"

        # Check for desc choice
        desc_choice = next((c for c in result if c.id == "created_at_desc"), None)
        assert desc_choice is not None
        assert desc_choice.name == "Created at (Desc)"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_choices_relevance(self):
        """Test getting choices for relevance field"""
        result = SortLogic.get_choices(AssignmentSortField.RELEVANCE)
        assert len(result) == 1

        # Check for desc choice only
        desc_choice = result[0]
        assert desc_choice.id == "relevance_desc"
        assert desc_choice.name == "Relevance (Desc)"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_sorts_tutor(self):
        """Test getting sorts for Tutor table"""
        result = SortLogic.get_sorts(Tutor)
        assert len(result) == 3

        expected_ids = ["name", "rating", "price"]
        for choice in result:
            assert choice.id in expected_ids

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_sorts_assignment(self):
        """Test getting sorts for Assignment table"""
        result = SortLogic.get_sorts(Assignment)
        assert len(result) > 0

        # Should have choices for all AssignmentSortField values
        for choice in result:
            assert isinstance(choice, SortChoice)
            assert choice.id is not None
            assert choice.name is not None

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_sorts_unsupported_table(self):
        """Test getting sorts for unsupported table"""

        class UnsupportedTable:
            pass

        result = SortLogic.get_sorts(UnsupportedTable)
        assert result == []
