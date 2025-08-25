from unittest.mock import patch

import pytest
from api.startup_email import send_startup_notification_email


class TestStartupEmail:
    """Test cases for startup email functionality"""

    @pytest.mark.unit
    @pytest.mark.services
    @patch("api.startup_email.GmailEmailService.send_email")
    @patch("api.startup_email.socket.gethostname")
    @patch("api.startup_email.datetime")
    @patch("api.startup_email.settings")
    def test_send_startup_notification_email_success(
        self, mock_settings, mock_datetime, mock_gethostname, mock_send_email
    ):
        """Test successful startup notification email"""
        # Mock settings
        mock_settings.gmail_startup_notification_email = "admin@example.com"

        # Mock hostname and datetime
        mock_gethostname.return_value = "test-server"
        mock_datetime.now.return_value.strftime.return_value = "2023-12-01 10:30:00"

        # Mock successful email sending
        mock_send_email.return_value = {
            "success": True,
            "message_id": "test_message_id_123",
        }

        # Call function
        result = send_startup_notification_email()

        # Verify result
        assert result["success"] is True
        assert result["message_id"] == "test_message_id_123"
        assert result["hostname"] == "test-server"
        assert result["startup_time"] == "2023-12-01 10:30:00"

        # Verify email was sent with correct parameters
        mock_send_email.assert_called_once()
        call_args = mock_send_email.call_args
        assert call_args.kwargs["recipient_email"] == "admin@example.com"
        assert call_args.kwargs["subject"] == "Backend Application Startup Notification"
        assert "test-server" in call_args.kwargs["content"]
        assert "2023-12-01 10:30:00" in call_args.kwargs["content"]

    @pytest.mark.unit
    @pytest.mark.services
    @patch("api.startup_email.settings")
    def test_send_startup_notification_email_no_config(self, mock_settings):
        """Test startup notification when no email is configured"""
        # Mock no email configured
        mock_settings.gmail_startup_notification_email = None

        # Call function
        result = send_startup_notification_email()

        # Verify result
        assert result["success"] is True
        assert result["message"] == "No email configured for startup notifications."

    @pytest.mark.unit
    @pytest.mark.services
    @patch("api.startup_email.settings")
    def test_send_startup_notification_email_empty_config(self, mock_settings):
        """Test startup notification when email config is empty string"""
        # Mock empty email configured
        mock_settings.gmail_startup_notification_email = ""

        # Call function
        result = send_startup_notification_email()

        # Verify result
        assert result["success"] is True
        assert result["message"] == "No email configured for startup notifications."

    @pytest.mark.unit
    @pytest.mark.services
    @patch("api.startup_email.GmailEmailService.send_email")
    @patch("api.startup_email.socket.gethostname")
    @patch("api.startup_email.datetime")
    @patch("api.startup_email.settings")
    def test_send_startup_notification_email_send_failure(
        self, mock_settings, mock_datetime, mock_gethostname, mock_send_email
    ):
        """Test startup notification when email sending fails"""
        # Mock settings
        mock_settings.gmail_startup_notification_email = "admin@example.com"

        # Mock hostname and datetime
        mock_gethostname.return_value = "test-server"
        mock_datetime.now.return_value.strftime.return_value = "2023-12-01 10:30:00"

        # Mock failed email sending
        mock_send_email.return_value = {
            "success": False,
            "error": "Failed to authenticate with Gmail",
        }

        # Call function
        result = send_startup_notification_email()

        # Verify result
        assert result["success"] is False
        assert result["error"] == "Failed to authenticate with Gmail"

    @pytest.mark.unit
    @pytest.mark.services
    @patch("api.startup_email.socket.gethostname")
    @patch("api.startup_email.settings")
    def test_send_startup_notification_email_exception(
        self, mock_settings, mock_gethostname
    ):
        """Test startup notification when an exception occurs"""
        # Mock settings
        mock_settings.gmail_startup_notification_email = "admin@example.com"

        # Mock exception in hostname retrieval
        mock_gethostname.side_effect = Exception("Network error")

        # Call function
        result = send_startup_notification_email()

        # Verify result
        assert result["success"] is False
        assert "Network error" in result["error"]

    @pytest.mark.unit
    @pytest.mark.services
    @patch("api.startup_email.GmailEmailService.send_email")
    @patch("api.startup_email.socket.gethostname")
    @patch("api.startup_email.datetime")
    @patch("api.startup_email.settings")
    def test_send_startup_notification_email_content_format(
        self, mock_settings, mock_datetime, mock_gethostname, mock_send_email
    ):
        """Test that startup notification email content is properly formatted"""
        # Mock settings
        mock_settings.gmail_startup_notification_email = "admin@example.com"

        # Mock hostname and datetime
        mock_gethostname.return_value = "production-server-01"
        mock_datetime.now.return_value.strftime.return_value = "2023-12-01 15:45:30"

        # Mock successful email sending
        mock_send_email.return_value = {
            "success": True,
            "message_id": "test_message_id_456",
        }

        # Call function
        result = send_startup_notification_email()

        # Verify email content format
        mock_send_email.assert_called_once()
        call_args = mock_send_email.call_args
        content = call_args.kwargs["content"]

        # Check content contains expected elements
        assert "Application Startup Notification" in content
        assert "Hostname: production-server-01" in content
        assert "Startup Time: 2023-12-01 15:45:30" in content
        assert "The backend application has successfully started." in content

        # Verify result contains expected data
        assert result["success"] is True
        assert result["hostname"] == "production-server-01"
        assert result["startup_time"] == "2023-12-01 15:45:30"

    @pytest.mark.unit
    @pytest.mark.services
    @patch("api.startup_email.GmailEmailService.send_email")
    @patch("api.startup_email.socket.gethostname")
    @patch("api.startup_email.datetime")
    @patch("api.startup_email.settings")
    def test_send_startup_notification_email_missing_message_id(
        self, mock_settings, mock_datetime, mock_gethostname, mock_send_email
    ):
        """Test startup notification when email service doesn't return message_id"""
        # Mock settings
        mock_settings.gmail_startup_notification_email = "admin@example.com"

        # Mock hostname and datetime
        mock_gethostname.return_value = "test-server"
        mock_datetime.now.return_value.strftime.return_value = "2023-12-01 10:30:00"

        # Mock successful email sending without message_id
        mock_send_email.return_value = {
            "success": True
            # No message_id in response
        }

        # Call function
        result = send_startup_notification_email()

        # Verify result handles missing message_id gracefully
        assert result["success"] is True
        assert result.get("message_id") is None  # Should be None, not cause error
        assert result["hostname"] == "test-server"
        assert result["startup_time"] == "2023-12-01 10:30:00"
