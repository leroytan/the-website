from unittest.mock import patch

import pytest
from api.logic.course_logic import CourseLogic


class TestCourseLogic:
    """Test cases for CourseLogic class"""

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.course_logic.StorageService")
    def test_get_public_summaries_success(self, mock_storage_service):
        """Test successful retrieval of public course summaries"""
        # Mock storage service response
        mock_summaries = [
            {"id": 1, "title": "Course 1", "description": "Description 1"},
            {"id": 2, "title": "Course 2", "description": "Description 2"},
        ]
        mock_storage_service.get_course_summaries.return_value = mock_summaries

        # Test the method
        result = CourseLogic.get_public_summaries()

        assert result == mock_summaries
        mock_storage_service.get_course_summaries.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.course_logic.StorageService")
    def test_get_public_summaries_empty(self, mock_storage_service):
        """Test retrieval of public course summaries when empty"""
        # Mock empty response
        mock_storage_service.get_course_summaries.return_value = []

        # Test the method
        result = CourseLogic.get_public_summaries()

        assert result == []
        mock_storage_service.get_course_summaries.assert_called_once()
