import pytest
from api.common.utils import Utils


class TestUtils:
    """Test cases for Utils class"""

    @pytest.mark.unit
    def test_validate_non_empty_string_valid(self):
        """Test validation with valid non-empty string"""
        Utils.validate_non_empty(name="test", email="test@example.com")

    @pytest.mark.unit
    def test_validate_non_empty_string_empty(self):
        """Test validation with empty string"""
        with pytest.raises(ValueError, match="name cannot be an empty string"):
            Utils.validate_non_empty(name="", email="test@example.com")

    @pytest.mark.unit
    def test_validate_non_empty_string_whitespace(self):
        """Test validation with whitespace-only string"""
        with pytest.raises(ValueError, match="name cannot be an empty string"):
            Utils.validate_non_empty(name="   ", email="test@example.com")

    @pytest.mark.unit
    def test_validate_non_empty_none(self):
        """Test validation with None value"""
        with pytest.raises(ValueError, match="name cannot be None"):
            Utils.validate_non_empty(name=None, email="test@example.com")

    @pytest.mark.unit
    def test_validate_non_empty_list_valid(self):
        """Test validation with valid non-empty list"""
        Utils.validate_non_empty(items=[1, 2, 3], name="test")

    @pytest.mark.unit
    def test_validate_non_empty_list_empty(self):
        """Test validation with empty list"""
        with pytest.raises(ValueError, match="items cannot be an empty list"):
            Utils.validate_non_empty(items=[], name="test")

    @pytest.mark.unit
    def test_validate_non_empty_dict_valid(self):
        """Test validation with valid non-empty dict"""
        Utils.validate_non_empty(data={"key": "value"}, name="test")

    @pytest.mark.unit
    def test_validate_non_empty_dict_empty(self):
        """Test validation with empty dict"""
        with pytest.raises(ValueError, match="data cannot be an empty dict"):
            Utils.validate_non_empty(data={}, name="test")

    @pytest.mark.unit
    def test_validate_non_empty_set_valid(self):
        """Test validation with valid non-empty set"""
        Utils.validate_non_empty(items={1, 2, 3}, name="test")

    @pytest.mark.unit
    def test_validate_non_empty_set_empty(self):
        """Test validation with empty set"""
        with pytest.raises(ValueError, match="items cannot be an empty set"):
            Utils.validate_non_empty(items=set(), name="test")

    @pytest.mark.unit
    def test_validate_non_empty_multiple_valid(self):
        """Test validation with multiple valid values"""
        Utils.validate_non_empty(
            name="test",
            email="test@example.com",
            items=[1, 2, 3],
            data={"key": "value"},
        )

    @pytest.mark.unit
    def test_validate_non_empty_multiple_invalid(self):
        """Test validation with multiple values where one is invalid"""
        with pytest.raises(ValueError, match="email cannot be an empty string"):
            Utils.validate_non_empty(name="test", email="", items=[1, 2, 3])

    @pytest.mark.unit
    def test_validate_non_empty_zero_number(self):
        """Test validation with zero number (should be valid)"""
        Utils.validate_non_empty(count=0, name="test")

    @pytest.mark.unit
    def test_validate_non_empty_false_boolean(self):
        """Test validation with False boolean (should be valid)"""
        Utils.validate_non_empty(active=False, name="test")

    @pytest.mark.unit
    def test_validate_non_empty_empty_tuple(self):
        """Test validation with empty tuple (should be valid as it's not in the check)"""
        Utils.validate_non_empty(items=(), name="test")
