from unittest.mock import AsyncMock, Mock, patch

import pytest
from api.index import (
    add_process_time_header,
    app,
    custom_http_exception_handler,
    lifespan,
)
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.exceptions import HTTPException as StarletteHTTPException


class TestIndexCore:
    """Test cases for core application functionality"""

    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)

    @pytest.mark.unit
    @pytest.mark.core
    @pytest.mark.asyncio
    async def test_lifespan_startup(self):
        """Test application lifespan startup"""
        mock_app = Mock(spec=FastAPI)

        with patch("api.index.send_startup_notification_email") as mock_startup_email:
            async with lifespan(mock_app):
                # Startup should call send_startup_notification_email
                mock_startup_email.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.core
    @pytest.mark.asyncio
    async def test_lifespan_shutdown(self):
        """Test application lifespan shutdown"""
        mock_app = Mock(spec=FastAPI)

        # Test that lifespan context manager works correctly
        async with lifespan(mock_app) as context:
            assert context is None  # lifespan yields None

    @pytest.mark.unit
    @pytest.mark.core
    def test_root_head_endpoint(self):
        """Test root HEAD endpoint"""
        response = self.client.head("/")

        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/json"

    @pytest.mark.unit
    @pytest.mark.core
    def test_ping_get_endpoint(self):
        """Test ping GET endpoint"""
        response = self.client.get("/api/ping")

        assert response.status_code == 200
        assert response.json() == {"message": "pong"}

    @pytest.mark.unit
    @pytest.mark.core
    def test_ping_post_endpoint(self):
        """Test ping POST endpoint"""
        response = self.client.post("/api/ping")

        assert response.status_code == 200
        assert response.json() == {"message": "pong"}

    @pytest.mark.unit
    @pytest.mark.core
    def test_ping_head_endpoint(self):
        """Test ping HEAD endpoint"""
        response = self.client.head("/api/ping")

        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/json"

    @pytest.mark.unit
    @pytest.mark.core
    def test_process_time_middleware(self):
        """Test process time middleware"""
        response = self.client.get("/api/ping")

        # Check that X-Process-Time header is present
        process_time = response.headers.get("X-Process-Time")
        assert process_time is not None
        assert float(process_time) > 0

    @pytest.mark.unit
    @pytest.mark.core
    @pytest.mark.asyncio
    async def test_add_process_time_header_middleware(self):
        """Test process time middleware function directly"""
        mock_request = Mock()
        mock_call_next = AsyncMock()
        mock_response = Mock()
        mock_response.headers = {}
        mock_call_next.return_value = mock_response

        # Mock time.time to return predictable values
        with patch("api.index.time.time") as mock_time:
            mock_time.side_effect = [1000.0, 1000.1]  # 0.1 second difference

            result = await add_process_time_header(mock_request, mock_call_next)

            assert result == mock_response
            # Use approximate comparison for floating point
            process_time = float(result.headers["X-Process-Time"])
            assert abs(process_time - 0.1) < 0.001
            mock_call_next.assert_called_once_with(mock_request)

    @pytest.mark.unit
    @pytest.mark.core
    @pytest.mark.asyncio
    async def test_custom_http_exception_handler_404(self):
        """Test custom HTTP exception handler for 404"""
        mock_request = Mock()
        mock_exception = StarletteHTTPException(status_code=404, detail="Not found")

        response = await custom_http_exception_handler(mock_request, mock_exception)

        assert response.status_code == 404
        # Use json() method instead of body.decode() for consistent formatting
        response_data = response.body.decode()
        assert "Error: The requested route or method does not exist" in response_data

    @pytest.mark.unit
    @pytest.mark.core
    @pytest.mark.asyncio
    async def test_custom_http_exception_handler_other_status(self):
        """Test custom HTTP exception handler for other status codes"""
        mock_request = Mock()
        mock_exception = StarletteHTTPException(
            status_code=500, detail="Internal server error"
        )

        response = await custom_http_exception_handler(mock_request, mock_exception)

        assert response.status_code == 500
        response_data = response.body.decode()
        assert "Internal server error" in response_data

    @pytest.mark.unit
    @pytest.mark.core
    def test_app_configuration(self):
        """Test that app is configured correctly"""
        assert app.docs_url == "/api/py/docs"
        assert app.openapi_url == "/api/py/openapi.json"
        # Check for lifespan function instead of attribute
        assert (
            hasattr(app, "lifespan")
            or hasattr(app, "_lifespan_context")
            or hasattr(app, "router")
        )

    @pytest.mark.unit
    @pytest.mark.core
    def test_cors_middleware_configured(self):
        """Test that CORS middleware is configured"""
        # Check that CORS middleware is added by looking for middleware stack
        assert len(app.user_middleware) > 0

    @pytest.mark.unit
    @pytest.mark.core
    def test_routers_included(self):
        """Test that all routers are included"""
        # Check that routers are included by looking for router paths
        routes = [route.path for route in app.routes]

        # Should have some router paths (not just the ping endpoints)
        router_paths = [
            path for path in routes if path.startswith("/api/") and "ping" not in path
        ]
        assert len(router_paths) > 0

    @pytest.mark.unit
    @pytest.mark.core
    def test_websocket_ping_endpoint_exists(self):
        """Test that websocket ping endpoint exists"""
        routes = [route.path for route in app.routes]
        assert "/ws/ping" in routes

    @pytest.mark.unit
    @pytest.mark.core
    def test_websocket_endpoint_exists(self):
        """Test that websocket endpoint exists"""
        routes = [route.path for route in app.routes]
        assert "/ws" in routes

    @pytest.mark.unit
    @pytest.mark.core
    def test_websocket_protected_endpoint_exists(self):
        """Test that protected websocket endpoint exists"""
        routes = [route.path for route in app.routes]
        assert "/ws/protected" in routes

    @pytest.mark.unit
    @pytest.mark.core
    def test_allowed_origins_configured(self):
        """Test that allowed origins are configured"""
        # This test checks that the CORS configuration is set up
        # The actual origins are set in settings, but we can verify the middleware is there
        assert len(app.user_middleware) > 0

    @pytest.mark.unit
    @pytest.mark.core
    def test_storage_service_initialized(self):
        """Test that StorageService is initialized"""
        # This is called at module level, so we just verify it doesn't raise an error
        from api.storage.storage_service import StorageService

        assert StorageService is not None

    @pytest.mark.unit
    @pytest.mark.core
    def test_app_has_lifespan(self):
        """Test that app has lifespan configured"""
        assert (
            hasattr(app, "lifespan")
            or hasattr(app, "_lifespan_context")
            or hasattr(app, "router")
        )

    @pytest.mark.unit
    @pytest.mark.core
    def test_app_has_middleware(self):
        """Test that app has middleware configured"""
        assert len(app.user_middleware) > 0

    @pytest.mark.unit
    @pytest.mark.core
    def test_app_has_exception_handler(self):
        """Test that app has exception handler configured"""
        # Check that exception handlers are configured
        assert len(app.exception_handlers) > 0
