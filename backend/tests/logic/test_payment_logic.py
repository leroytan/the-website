from unittest.mock import Mock, patch

import pytest
from api.logic.payment_logic import PaymentLogic
from api.router.models import PaymentRequest
from fastapi import HTTPException


class TestPaymentLogic:
    """Test cases for PaymentLogic class"""

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.payment_logic.stripe")
    @patch("api.logic.payment_logic.AssignmentLogic")
    def test_handle_payment_request_success(self, mock_assignment_logic, mock_stripe):
        """Test successful payment request handling"""
        # Mock assignment logic responses
        mock_assignment_logic.get_assignment_owner_id.return_value = 1
        mock_assignment_logic.get_lesson_duration.return_value = 60  # 60 minutes
        mock_assignment_logic.get_request_hourly_rate.return_value = 50  # $50/hour

        # Mock stripe checkout session
        mock_checkout_session = {
            "id": "cs_test_123",
            "url": "https://checkout.stripe.com/test",
        }
        mock_stripe.checkout.Session.create.return_value = mock_checkout_session

        # Mock assert function
        mock_assert_func = Mock()

        # Create payment request
        payment_request = PaymentRequest(
            mode="payment",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            assignment_request_id=1,
            tutor_id=2,
            chat_id=None,
        )

        # Test the method
        result = PaymentLogic.handle_payment_request(payment_request, mock_assert_func)

        assert result["session_id"] == "cs_test_123"
        assert result["url"] == "https://checkout.stripe.com/test"
        mock_assert_func.assert_called_once_with(1)
        mock_stripe.checkout.Session.create.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.payment_logic.stripe")
    @patch("api.logic.payment_logic.AssignmentLogic")
    def test_handle_payment_request_stripe_error(
        self, mock_assignment_logic, mock_stripe
    ):
        """Test payment request handling with Stripe error"""
        # Mock assignment logic responses
        mock_assignment_logic.get_assignment_owner_id.return_value = 1
        mock_assignment_logic.get_lesson_duration.return_value = 60
        mock_assignment_logic.get_request_hourly_rate.return_value = 50

        # Mock stripe error
        mock_stripe_error = Exception("Stripe error")
        mock_stripe_error.user_message = "Stripe error message"
        mock_stripe.error.StripeError = Exception
        mock_stripe.checkout.Session.create.side_effect = mock_stripe_error

        # Mock assert function
        mock_assert_func = Mock()

        # Create payment request
        payment_request = PaymentRequest(
            mode="payment",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            assignment_request_id=1,
            tutor_id=2,
            chat_id=None,
        )

        # Test the method
        with pytest.raises(HTTPException) as exc_info:
            PaymentLogic.handle_payment_request(payment_request, mock_assert_func)

        assert exc_info.value.status_code == 503
        assert "Payment processing error" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.payment_logic.stripe")
    @patch("api.logic.payment_logic.AssignmentLogic")
    @patch("api.logic.payment_logic.ChatLogic")
    @patch("api.logic.payment_logic.StorageService")
    @patch("api.logic.payment_logic.GmailEmailService")
    def test_handle_stripe_webhook_success(
        self,
        mock_email_service,
        mock_storage_service,
        mock_chat_logic,
        mock_assignment_logic,
        mock_stripe,
    ):
        """Test successful Stripe webhook handling"""
        # Mock webhook event
        mock_event = {
            "type": "payment_intent.succeeded",
            "data": {"object": {"metadata": {"assignment_request_id": "123"}}},
        }

        # Mock stripe webhook construction
        mock_stripe.Webhook.construct_event.return_value = mock_event

        # Mock assignment logic
        mock_assignment_logic.accept_assignment_request.return_value = (
            1,
            2,
        )  # owner_id, requester_id

        # Mock chat logic
        mock_chat_preview = Mock()
        mock_chat_preview.id = 1
        mock_chat_logic.get_or_create_private_chat.return_value = mock_chat_preview

        # Mock storage service
        mock_storage_service.engine = Mock()

        # Mock session and database objects
        mock_session = Mock()
        mock_tutor = Mock()
        mock_tutor.user.email = "tutor@example.com"
        mock_assignment_request = Mock()
        mock_assignment = Mock()
        mock_assignment.title = "Test Assignment"
        mock_assignment_request.assignment = mock_assignment
        mock_assignment_request.requested_rate_hourly = 50
        mock_assignment_request.requested_duration = 60

        # Mock session context manager
        with patch("api.logic.payment_logic.Session") as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session.query.return_value.filter_by.return_value.first.side_effect = [
                mock_tutor,
                mock_assignment_request,
            ]

            # Test the method
            result = PaymentLogic.handle_stripe_webhook(
                b"test_payload", "test_signature"
            )

            assert result["status"] == "success"
            mock_stripe.Webhook.construct_event.assert_called_once()
            mock_assignment_logic.accept_assignment_request.assert_called_once_with(123)
            mock_chat_logic.get_or_create_private_chat.assert_called_once_with(1, 2)
            mock_chat_logic.unlock_chat.assert_called_once_with(1, 1)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.payment_logic.stripe")
    def test_handle_stripe_webhook_invalid_payload(self, mock_stripe):
        """Test Stripe webhook handling with invalid payload"""
        # Mock stripe webhook construction to raise ValueError
        mock_stripe.Webhook.construct_event.side_effect = ValueError("Invalid payload")

        # Test the method
        with pytest.raises(HTTPException) as exc_info:
            PaymentLogic.handle_stripe_webhook(b"invalid_payload", "test_signature")

        assert exc_info.value.status_code == 400
        assert "Invalid payload" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.payment_logic.stripe")
    def test_handle_stripe_webhook_signature_verification_failed(self, mock_stripe):
        """Test Stripe webhook handling with signature verification failure"""
        # Mock stripe webhook construction to raise signature verification error
        mock_stripe.error.SignatureVerificationError = Exception
        mock_stripe.Webhook.construct_event.side_effect = Exception(
            "Signature verification failed"
        )

        # Test the method
        with pytest.raises(HTTPException) as exc_info:
            PaymentLogic.handle_stripe_webhook(b"test_payload", "invalid_signature")

        assert exc_info.value.status_code == 400
        assert "Signature verification failed" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.payment_logic.stripe")
    def test_handle_stripe_webhook_other_event_type(self, mock_stripe):
        """Test Stripe webhook handling with non-payment event"""
        # Mock webhook event with different type
        mock_event = {"type": "customer.created", "data": {"object": {}}}

        # Mock stripe webhook construction
        mock_stripe.Webhook.construct_event.return_value = mock_event

        # Test the method
        result = PaymentLogic.handle_stripe_webhook(b"test_payload", "test_signature")

        # Should return success even for non-payment events
        assert (
            result is None
        )  # The method doesn't return anything for non-payment events
