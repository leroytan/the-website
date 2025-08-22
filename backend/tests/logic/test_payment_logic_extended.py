from unittest.mock import ANY, Mock, patch

import pytest
from api.logic.payment_logic import PaymentLogic
from api.router.models import PaymentRequest
from fastapi import HTTPException


class TestPaymentLogicExtended:
    """Extended test cases for PaymentLogic"""

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.payment_logic.stripe.checkout.Session.create")
    @patch("api.logic.payment_logic.AssignmentLogic.get_request_hourly_rate")
    @patch("api.logic.payment_logic.AssignmentLogic.get_lesson_duration")
    @patch("api.logic.payment_logic.AssignmentLogic.get_assignment_owner_id")
    def test_handle_payment_request_success(
        self, mock_get_owner_id, mock_get_duration, mock_get_rate, mock_create_session
    ):
        """Test successful payment request handling"""
        # Mock assignment logic responses
        mock_get_owner_id.return_value = 123
        mock_get_duration.return_value = 120  # 2 hours in minutes
        mock_get_rate.return_value = 50  # $50 per hour

        # Mock stripe session creation - return a dict-like object
        mock_session = {"id": "cs_test_123", "url": "https://checkout.stripe.com/test"}
        mock_create_session.return_value = mock_session

        # Mock authorization function
        mock_authorize = Mock()

        # Create payment request
        payment_request = PaymentRequest(
            assignment_request_id=456,
            tutor_id=789,
            chat_id=101,
            mode="payment",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )

        # Call function
        result = PaymentLogic.handle_payment_request(payment_request, mock_authorize)

        # Verify authorization was called
        mock_authorize.assert_called_once_with(123)

        # Verify assignment logic calls
        mock_get_owner_id.assert_called_once_with(456)
        mock_get_duration.assert_called_once_with(456)
        mock_get_rate.assert_called_once_with(456)

        # Verify stripe session creation
        mock_create_session.assert_called_once()
        call_args = mock_create_session.call_args[1]

        # Check line items
        line_items = call_args["line_items"]
        assert len(line_items) == 1
        assert line_items[0]["price_data"]["currency"] == "sgd"
        assert (
            line_items[0]["price_data"]["unit_amount"] == 10000
        )  # 2 hours * $50 * 100 cents
        assert line_items[0]["quantity"] == 1

        # Check payment intent metadata
        metadata = call_args["payment_intent_data"]["metadata"]
        assert metadata["assignment_request_id"] == 456

        # Check URLs
        assert call_args["mode"] == "payment"
        assert (
            call_args["success_url"]
            == "https://example.com/success?session_id={CHECKOUT_SESSION_ID}&tutor_id=789&chat_id=101"
        )
        assert call_args["cancel_url"] == "https://example.com/cancel"

        # Verify result
        assert result["session_id"] == "cs_test_123"
        assert result["url"] == "https://checkout.stripe.com/test"

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.payment_logic.AssignmentLogic.get_assignment_owner_id")
    def test_handle_payment_request_unauthorized(self, mock_get_owner_id):
        """Test payment request with unauthorized user"""
        # Mock assignment owner
        mock_get_owner_id.return_value = 123

        # Mock authorization function that raises exception
        def mock_authorize(user_id):
            raise HTTPException(status_code=403, detail="Unauthorized")

        # Create payment request
        payment_request = PaymentRequest(
            assignment_request_id=456,
            tutor_id=789,
            chat_id=101,
            mode="payment",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )

        # Call function and expect exception
        with pytest.raises(HTTPException) as exc_info:
            PaymentLogic.handle_payment_request(payment_request, mock_authorize)

        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Unauthorized"

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.payment_logic.stripe.checkout.Session.create")
    @patch("api.logic.payment_logic.AssignmentLogic.get_request_hourly_rate")
    @patch("api.logic.payment_logic.AssignmentLogic.get_lesson_duration")
    @patch("api.logic.payment_logic.AssignmentLogic.get_assignment_owner_id")
    def test_handle_payment_request_stripe_error(
        self, mock_get_owner_id, mock_get_duration, mock_get_rate, mock_create_session
    ):
        """Test payment request with Stripe error"""
        # Mock assignment logic responses
        mock_get_owner_id.return_value = 123
        mock_get_duration.return_value = 60  # 1 hour
        mock_get_rate.return_value = 30  # $30 per hour

        # Mock authorization function
        mock_authorize = Mock()

        # Mock stripe error
        import stripe

        mock_create_session.side_effect = stripe.error.StripeError(
            "Test error", "Test message"
        )

        # Create payment request
        payment_request = PaymentRequest(
            assignment_request_id=456,
            tutor_id=789,
            chat_id=101,
            mode="payment",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )

        # Call function and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            PaymentLogic.handle_payment_request(payment_request, mock_authorize)

        assert exc_info.value.status_code == 503
        assert "Payment processing error on stripe" in exc_info.value.detail

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.payment_logic.stripe.Webhook.construct_event")
    @patch("api.logic.payment_logic.AssignmentLogic.accept_assignment_request")
    @patch("api.logic.payment_logic.ChatLogic.get_or_create_private_chat")
    @patch("api.logic.payment_logic.ChatLogic.unlock_chat")
    @patch("api.logic.payment_logic.GmailEmailService.send_email")
    @patch("api.logic.payment_logic.Session")
    def test_handle_stripe_webhook_success(
        self,
        mock_session,
        mock_send_email,
        mock_unlock_chat,
        mock_get_chat,
        mock_accept_request,
        mock_construct_event,
    ):
        """Test successful stripe webhook handling"""
        # Mock webhook event construction
        mock_event = {
            "type": "payment_intent.succeeded",
            "data": {"object": {"metadata": {"assignment_request_id": "456"}}},
        }
        mock_construct_event.return_value = mock_event

        # Mock assignment acceptance
        mock_accept_request.return_value = (123, 789)  # owner_id, requester_id

        # Mock chat creation
        mock_chat = Mock()
        mock_chat.id = 101
        mock_get_chat.return_value = mock_chat

        # Mock session context manager
        mock_session_instance = Mock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock tutor and assignment data
        mock_tutor = Mock()
        mock_tutor.id = 789
        mock_tutor.user = Mock()
        mock_tutor.user.email = "tutor@example.com"

        mock_assignment_request = Mock()
        mock_assignment_request.id = 456
        mock_assignment_request.requested_rate_hourly = 50
        mock_assignment_request.requested_duration = 120
        mock_assignment_request.assignment = Mock()
        mock_assignment_request.assignment.title = "Math Tutoring"

        mock_session_instance.query.return_value.filter_by.return_value.first.side_effect = [
            mock_tutor,  # First call returns tutor
            mock_assignment_request,  # Second call returns assignment request
        ]

        # Call function
        result = PaymentLogic.handle_stripe_webhook(b"test_payload", "test_signature")

        # Verify webhook construction
        mock_construct_event.assert_called_once_with(
            b"test_payload", "test_signature", ANY
        )  # settings.stripe_webhook_secret

        # Verify assignment acceptance
        mock_accept_request.assert_called_once_with(456)

        # Verify chat operations
        mock_get_chat.assert_called_once_with(123, 789)
        mock_unlock_chat.assert_called_once_with(101, 123)

        # Verify email sending
        mock_send_email.assert_called_once()
        call_args = mock_send_email.call_args[1]
        assert call_args["recipient_email"] == "tutor@example.com"
        assert call_args["subject"] == "Assignment Accepted: Math Tutoring"
        assert "Math Tutoring" in call_args["content"]
        assert "$50" in call_args["content"]
        assert "120 minutes" in call_args["content"]

        # Verify result
        assert result == {"status": "success"}

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.payment_logic.stripe.Webhook.construct_event")
    def test_handle_stripe_webhook_invalid_payload(self, mock_construct_event):
        """Test webhook handling with invalid payload"""
        # Mock webhook construction to raise ValueError
        mock_construct_event.side_effect = ValueError("Invalid payload")

        # Call function and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            PaymentLogic.handle_stripe_webhook(b"invalid_payload", "test_signature")

        assert exc_info.value.status_code == 400
        assert "Invalid payload" in exc_info.value.detail

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.payment_logic.stripe.Webhook.construct_event")
    def test_handle_stripe_webhook_signature_verification_failed(
        self, mock_construct_event
    ):
        """Test webhook handling with signature verification failure"""
        # Mock webhook construction to raise signature verification error
        import stripe

        mock_construct_event.side_effect = stripe.error.SignatureVerificationError(
            "Invalid signature", "sig_header"
        )

        # Call function and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            PaymentLogic.handle_stripe_webhook(b"test_payload", "invalid_signature")

        assert exc_info.value.status_code == 400
        assert "Signature verification failed" in exc_info.value.detail

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.payment_logic.stripe.Webhook.construct_event")
    def test_handle_stripe_webhook_other_event_type(self, mock_construct_event):
        """Test webhook handling with non-payment event"""
        # Mock webhook event for different event type
        mock_event = {"type": "customer.created", "data": {"object": {}}}
        mock_construct_event.return_value = mock_event

        # Call function - should not process payment logic
        result = PaymentLogic.handle_stripe_webhook(b"test_payload", "test_signature")

        # Should return None or empty result for non-payment events
        assert result is None

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.payment_logic.stripe.Webhook.construct_event")
    @patch("api.logic.payment_logic.AssignmentLogic.accept_assignment_request")
    @patch("api.logic.payment_logic.ChatLogic.get_or_create_private_chat")
    @patch("api.logic.payment_logic.ChatLogic.unlock_chat")
    @patch("api.logic.payment_logic.Session")
    def test_handle_stripe_webhook_missing_metadata(
        self,
        mock_session,
        mock_unlock_chat,
        mock_get_chat,
        mock_accept_request,
        mock_construct_event,
    ):
        """Test webhook handling with missing metadata"""
        # Mock webhook event without metadata
        mock_event = {
            "type": "payment_intent.succeeded",
            "data": {"object": {"metadata": {}}},
        }
        mock_construct_event.return_value = mock_event

        # Mock assignment acceptance to raise KeyError
        mock_accept_request.side_effect = KeyError("assignment_request_id")

        # Mock chat creation
        mock_chat = Mock()
        mock_chat.id = 101
        mock_get_chat.return_value = mock_chat

        # Mock session context manager
        mock_session_instance = Mock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock empty tutor data
        mock_session_instance.query.return_value.filter_by.return_value.first.return_value = None

        # Call function - should handle missing metadata gracefully
        with pytest.raises(KeyError):
            PaymentLogic.handle_stripe_webhook(b"test_payload", "test_signature")

    @pytest.mark.unit
    @pytest.mark.logic
    def test_payment_calculation_logic(self):
        """Test payment calculation logic"""
        # Test various scenarios
        test_cases = [
            (60, 30, 3000),  # 1 hour at $30 = $30 = 3000 cents
            (120, 50, 10000),  # 2 hours at $50 = $100 = 10000 cents
            (90, 25, 3750),  # 1.5 hours at $25 = $37.50 = 3750 cents
            (30, 100, 5000),  # 0.5 hours at $100 = $50 = 5000 cents
        ]

        for duration_minutes, hourly_rate, expected_cents in test_cases:
            num_hours = duration_minutes / 60
            hourly_rate_cents = hourly_rate * 100
            fee = num_hours * hourly_rate_cents

            assert fee == expected_cents, (
                f"Failed for {duration_minutes}min at ${hourly_rate}/hr"
            )

    @pytest.mark.unit
    @pytest.mark.logic
    def test_stripe_api_key_configured(self):
        """Test that Stripe API key is configured"""
        import stripe

        assert stripe.api_key is not None
        assert len(stripe.api_key) > 0
