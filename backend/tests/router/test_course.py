from unittest.mock import patch

import pytest
from api.router.course import router
from fastapi.testclient import TestClient


class TestCourseRouter:
    """Test cases for course router endpoints"""

    @pytest.mark.unit
    @pytest.mark.router
    def test_get_courses_success(self):
        """Test successful courses retrieval"""
        with patch(
            "api.logic.course_logic.CourseLogic.get_public_summaries"
        ) as mock_get:
            mock_get.return_value = []

            client = TestClient(router)

            response = client.get("/api/courses")

            assert response.status_code == 200
            assert response.json() == []

    @pytest.mark.unit
    @pytest.mark.router
    def test_get_course_about_success(self):
        """Test successful course about retrieval"""
        # Test the function directly
        from api.router.course import get_course_about

        result = get_course_about("CS1010")

        # Since it's async, we need to await it
        import asyncio

        result = asyncio.run(result)

        assert result is None

    @pytest.mark.unit
    @pytest.mark.router
    def test_get_course_modules_success(self):
        """Test successful course modules retrieval"""
        # Test the function directly
        from api.router.course import get_course_modules

        result = get_course_modules("CS1010")

        # Since it's async, we need to await it
        import asyncio

        result = asyncio.run(result)

        assert result == []

    @pytest.mark.unit
    @pytest.mark.router
    def test_get_course_module_content_success(self):
        """Test successful course module content retrieval"""
        # Test the function directly
        from api.router.course import get_course_module_content

        result = get_course_module_content("CS1010", 1)

        # Since it's async, we need to await it
        import asyncio

        result = asyncio.run(result)

        assert result is None
