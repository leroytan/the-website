import pytest

from api.common.utils import Utils


class TestUtilsValidation:
    """Test cases for Utils validation methods"""

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_string_valid(self):
        """Test validation with valid non-empty string"""
        # Should not raise any exception
        Utils.validate_non_empty(name="John Doe")
        Utils.validate_non_empty(email="test@example.com")

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_string_invalid_none(self):
        """Test validation with None value"""
        with pytest.raises(ValueError, match="name cannot be None"):
            Utils.validate_non_empty(name=None)

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_string_invalid_empty(self):
        """Test validation with empty string"""
        with pytest.raises(ValueError, match="email cannot be an empty string"):
            Utils.validate_non_empty(email="")

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_string_invalid_whitespace(self):
        """Test validation with whitespace-only string"""
        with pytest.raises(ValueError, match="title cannot be an empty string"):
            Utils.validate_non_empty(title="   ")

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_list_valid(self):
        """Test validation with valid non-empty list"""
        # Should not raise any exception
        Utils.validate_non_empty(items=[1, 2, 3])
        Utils.validate_non_empty(names=["Alice", "Bob"])

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_list_invalid_empty(self):
        """Test validation with empty list"""
        with pytest.raises(ValueError, match="items cannot be an empty list"):
            Utils.validate_non_empty(items=[])

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_list_invalid_none(self):
        """Test validation with None list"""
        with pytest.raises(ValueError, match="items cannot be None"):
            Utils.validate_non_empty(items=None)

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_dict_valid(self):
        """Test validation with valid non-empty dict"""
        # Should not raise any exception
        Utils.validate_non_empty(config={"key": "value"})
        Utils.validate_non_empty(settings={"debug": True, "port": 8000})

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_dict_invalid_empty(self):
        """Test validation with empty dict"""
        with pytest.raises(ValueError, match="config cannot be an empty dict"):
            Utils.validate_non_empty(config={})

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_dict_invalid_none(self):
        """Test validation with None dict"""
        with pytest.raises(ValueError, match="settings cannot be None"):
            Utils.validate_non_empty(settings=None)

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_set_valid(self):
        """Test validation with valid non-empty set"""
        # Should not raise any exception
        Utils.validate_non_empty(tags={1, 2, 3})
        Utils.validate_non_empty(categories={"tech", "science"})

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_set_invalid_empty(self):
        """Test validation with empty set"""
        with pytest.raises(ValueError, match="tags cannot be an empty set"):
            Utils.validate_non_empty(tags=set())

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_set_invalid_none(self):
        """Test validation with None set"""
        with pytest.raises(ValueError, match="categories cannot be None"):
            Utils.validate_non_empty(categories=None)

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_multiple_fields_valid(self):
        """Test validation with multiple valid fields"""
        # Should not raise any exception
        Utils.validate_non_empty(
            name="John Doe",
            email="john@example.com",
            items=[1, 2, 3],
            config={"debug": True}
        )

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_multiple_fields_invalid(self):
        """Test validation with multiple fields where one is invalid"""
        with pytest.raises(ValueError, match="email cannot be an empty string"):
            Utils.validate_non_empty(
                name="John Doe",
                email="",  # This should cause the error
                items=[1, 2, 3],
                config={"debug": True}
            )

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_mixed_types_valid(self):
        """Test validation with mixed valid types"""
        # Should not raise any exception
        Utils.validate_non_empty(
            string_field="valid string",
            list_field=[1, 2],
            dict_field={"key": "value"},
            set_field={1, 2, 3}
        )

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_numeric_values(self):
        """Test validation with numeric values (should pass)"""
        # Numeric values should be valid (not considered empty)
        Utils.validate_non_empty(
            count=0,  # Zero should be valid
            price=10.5,
            negative_value=-1
        )

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_boolean_values(self):
        """Test validation with boolean values (should pass)"""
        # Boolean values should be valid
        Utils.validate_non_empty(
            is_active=True,
            is_disabled=False
        )

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_error_message_format(self):
        """Test that error messages contain the correct field name"""
        with pytest.raises(ValueError) as exc_info:
            Utils.validate_non_empty(custom_field_name=None)
        
        assert "custom_field_name cannot be None" in str(exc_info.value)

    @pytest.mark.unit
    @pytest.mark.common
    def test_validate_non_empty_error_message_type_specific(self):
        """Test that error messages are type-specific"""
        # Test list error message
        with pytest.raises(ValueError) as exc_info:
            Utils.validate_non_empty(my_list=[])
        assert "cannot be an empty list" in str(exc_info.value)
        
        # Test dict error message
        with pytest.raises(ValueError) as exc_info:
            Utils.validate_non_empty(my_dict={})
        assert "cannot be an empty dict" in str(exc_info.value)
        
        # Test set error message
        with pytest.raises(ValueError) as exc_info:
            Utils.validate_non_empty(my_set=set())
        assert "cannot be an empty set" in str(exc_info.value)
