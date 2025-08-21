from unittest.mock import MagicMock, patch

import pytest
from api.services.email_service import GmailEmailService


class TestEmailService:
    """Test cases for email service"""

    @pytest.mark.unit
    @pytest.mark.services
    @patch("api.services.email_service.GmailEmailService._get_gmail_service")
    @patch("api.services.email_service.GmailEmailService._get_credentials")
    def test_send_email_confirmation_email(self, mock_get_creds, mock_get_service):
        """Test sending email confirmation email"""
        # Mock the Gmail service
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.users().messages().send().execute.return_value = {
            "id": "123",
            "threadId": "456",
        }

        # Test sending confirmation email
        result = GmailEmailService.send_email_confirmation_email(
            recipient_email="test@example.com",
            confirmation_link="https://example.com/confirm?token=123",
            user_name="Test User",
        )

        assert result["success"] is True
        assert "message_id" in result
        assert "thread_id" in result

    @pytest.mark.unit
    @pytest.mark.services
    @patch("api.services.email_service.GmailEmailService._get_gmail_service")
    @patch("api.services.email_service.GmailEmailService._get_credentials")
    def test_send_password_reset_email(self, mock_get_creds, mock_get_service):
        """Test sending password reset email"""
        # Mock the Gmail service
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.users().messages().send().execute.return_value = {
            "id": "123",
            "threadId": "456",
        }

        # Test sending password reset email
        result = GmailEmailService.send_password_reset_email(
            recipient_email="test@example.com",
            reset_link="https://example.com/reset?token=123",
        )

        assert result["success"] is True
        assert "message_id" in result
        assert "thread_id" in result

    @pytest.mark.unit
    @pytest.mark.services
    def test_create_email_confirmation_link(self):
        """Test creating email confirmation link"""
        confirmation_token = "test_confirmation_token"
        confirmation_url = "https://example.com/confirm-email"

        link = GmailEmailService.create_email_confirmation_link(
            confirmation_token, confirmation_url
        )

        assert confirmation_token in link
        assert confirmation_url in link

    @pytest.mark.unit
    @pytest.mark.services
    def test_create_reset_link(self):
        """Test creating password reset link"""
        reset_token = "test_reset_token"
        reset_url = "https://example.com/reset-password"

        link = GmailEmailService.create_reset_link(reset_token, reset_url)

        assert reset_token in link
        assert reset_url in link

    @pytest.mark.unit
    @pytest.mark.services
    @patch("api.services.email_service.GmailEmailService._get_gmail_service")
    @patch("api.services.email_service.GmailEmailService._get_credentials")
    def test_send_unread_message_email(self, mock_get_creds, mock_get_service):
        """Test sending unread message notification email"""
        # Mock the Gmail service
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.users().messages().send().execute.return_value = {
            "id": "123",
            "threadId": "456",
        }

        # Test sending unread message email
        result = GmailEmailService.send_unread_message_email(
            recipient_email="test@example.com",
            sender_name="John Doe",
            message_preview="Hello!",
            chat_url="https://example.com/chat",
        )

        assert result["success"] is True
        assert "message_id" in result
        assert "thread_id" in result

    @pytest.mark.unit
    @pytest.mark.services
    @patch("api.services.email_service.GmailEmailService._read_template")
    @patch("api.services.email_service.GmailEmailService._get_gmail_service")
    @patch("api.services.email_service.GmailEmailService._get_credentials")
    def test_send_assignment_request_email(self, mock_get_creds, mock_get_service, mock_read_template):
        """Test sending assignment request email"""
        # Mock the Gmail service
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.users().messages().send().execute.return_value = {
            "id": "123",
            "threadId": "456",
        }

        # Mock the template
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Test email content</html>"
        mock_read_template.return_value = mock_template

        # Mock assignment data
        mock_assignment = MagicMock()
        mock_assignment.title = "Math Assignment"
        mock_assignment.price = 100
        mock_assignment.subject = "Mathematics"

        # Test sending assignment request email
        result = GmailEmailService.notify_new_assignment_request(
            recipient_email="test@gmail.com",
            assignment=mock_assignment,
            origin="https://example.com",
        )

        assert result["success"] is True
        assert "message_id" in result
        assert "thread_id" in result

    @pytest.mark.unit
    @pytest.mark.services
    def test_email_template_rendering(self):
        """Test email template rendering"""
        # Verify that template rendering methods exist
        assert hasattr(GmailEmailService, "_read_template")
        assert hasattr(GmailEmailService, "send_email_confirmation_email")
        assert hasattr(GmailEmailService, "send_password_reset_email")

    @pytest.mark.unit
    @pytest.mark.services
    @patch("api.services.email_service.GmailEmailService._get_gmail_service")
    @patch("api.services.email_service.GmailEmailService._get_credentials")
    def test_email_service_error_handling(self, mock_get_creds, mock_get_service):
        """Test email service error handling"""
        # Mock the Gmail service to raise an HttpError
        from googleapiclient.errors import HttpError
        mock_get_service.side_effect = HttpError(
            resp=MagicMock(status=400),
            content=b'{"error": {"message": "Email service error"}}'
        )

        # Test sending invalid email
        result = GmailEmailService.send_email_confirmation_email(
            recipient_email="invalid",
            confirmation_link="https://example.com/confirm?token=123",
            user_name="Test User",
        )

        assert result["success"] is False
        assert "error" in result

    @pytest.mark.unit
    @pytest.mark.services
    @patch("api.services.email_service.GmailEmailService._get_gmail_service")
    @patch("api.services.email_service.GmailEmailService._get_credentials")
    def test_email_validation(self, mock_get_creds, mock_get_service):
        """Test email validation in service methods"""
        # Mock the Gmail service to simulate an HttpError
        from googleapiclient.errors import HttpError
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.users().messages().send().execute.side_effect = HttpError(
            resp=MagicMock(status=400),
            content=b'{"error": {"message": "Invalid email"}}'
        )
        
        # Test with invalid email - should return error response, not raise exception
        result = GmailEmailService.send_email_confirmation_email(
            recipient_email="invalid-email",
            confirmation_link="https://example.com/confirm?token=123",
            user_name="Test User",
        )

        assert result["success"] is False
        assert "error" in result

    @pytest.mark.unit
    @pytest.mark.services
    def test_link_generation_security(self):
        """Test that generated links are secure"""
        confirmation_token = "test_confirmation_token"
        confirmation_url = "https://example.com/confirm-email"

        link = GmailEmailService.create_email_confirmation_link(
            confirmation_token, confirmation_url
        )

        # Test that the link uses HTTPS
        assert link.startswith("https://")

        # Test that the token is properly encoded in the URL
        assert confirmation_token in link
