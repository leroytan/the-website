import pytest
from unittest.mock import patch, Mock, AsyncMock
from fastapi.testclient import TestClient
from api.router.payment import router
from api.router.models import PaymentRequest
from api.storage.models import User

class TestPaymentRouter:
    """Test cases for payment router endpoints"""

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    async def test_create_checkout_session_success(self):
        """Test successful checkout session creation"""
        with patch('api.logic.auth_logic.AuthLogic.create_assert_user_authorized') as mock_assert:
            with patch('api.logic.payment_logic.PaymentLogic.handle_payment_request') as mock_handle:
                mock_assert.return_value = True
                mock_handle.return_value = {"success": True, "session_id": "cs_test_123"}
                
                # Test the function directly instead of using TestClient
                from api.router.payment import create_checkout_session
                
                payment_request = PaymentRequest(
                    mode="payment",
                    success_url="https://example.com/success",
                    cancel_url="https://example.com/cancel",
                    assignment_request_id=1,
                    tutor_id=2
                )
                
                # Create a mock user
                mock_user = User(id=1, name="Test User", email="test@example.com")
                
                # Call the function directly
                result = await create_checkout_session(payment_request, mock_user)
                
                assert result == {"success": True, "session_id": "cs_test_123"}
                mock_assert.assert_called_once_with(mock_user.id)
                mock_handle.assert_called_once_with(payment_request, True)

    @pytest.mark.unit
    @pytest.mark.router
    def test_stripe_webhook_success(self):
        """Test successful Stripe webhook handling"""
        with patch('api.logic.payment_logic.PaymentLogic.handle_stripe_webhook') as mock_handle:
            mock_handle.return_value = {"success": True, "processed": True}
            
            client = TestClient(router)
            
            # Mock request body and headers
            with patch('fastapi.Request.body') as mock_body:
                with patch('fastapi.Request.headers') as mock_headers:
                    mock_body.return_value = b"test_payload"
                    mock_headers.get.return_value = "test_signature"
                    
                    response = client.post("/webhook/stripe")
                    
                    assert response.status_code == 200
                    assert response.json() == {"success": True, "processed": True}

    @pytest.mark.unit
    @pytest.mark.router
    def test_stripe_webhook_with_signature_header(self):
        """Test Stripe webhook with signature header"""
        with patch('api.logic.payment_logic.PaymentLogic.handle_stripe_webhook') as mock_handle:
            mock_handle.return_value = {"success": True, "processed": True}
            
            client = TestClient(router)
            
            # Mock request body and headers
            with patch('fastapi.Request.body') as mock_body:
                with patch('fastapi.Request.headers') as mock_headers:
                    mock_body.return_value = b"test_payload"
                    mock_headers.get.return_value = "whsec_test_signature"
                    
                    response = client.post("/webhook/stripe")
                    
                    assert response.status_code == 200
                    # Verify the print statement is covered by the webhook handling
                    mock_handle.assert_called_once_with(b"test_payload", "whsec_test_signature")

    @pytest.mark.unit
    @pytest.mark.router
    def test_stripe_webhook_without_signature_header(self):
        """Test Stripe webhook without signature header"""
        with patch('api.logic.payment_logic.PaymentLogic.handle_stripe_webhook') as mock_handle:
            mock_handle.return_value = {"success": True, "processed": True}
            
            client = TestClient(router)
            
            # Mock request body and headers
            with patch('fastapi.Request.body') as mock_body:
                with patch('fastapi.Request.headers') as mock_headers:
                    mock_body.return_value = b"test_payload"
                    mock_headers.get.return_value = None
                    
                    response = client.post("/webhook/stripe")
                    
                    assert response.status_code == 200
                    # Verify the print statement is covered by the webhook handling
                    mock_handle.assert_called_once_with(b"test_payload", None)
