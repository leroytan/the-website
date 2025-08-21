from unittest.mock import patch

import pytest
from api.services.content_filter_service import ContentFilterService, PIIDetection


class TestPIIDetection:
    """Test cases for PIIDetection class"""

    @pytest.mark.unit
    def test_pii_detection_creation(self):
        """Test creating a PIIDetection instance"""
        detection = PIIDetection(
            has_pii=True,
            detected_types=["EMAIL_ADDRESS", "PHONE_NUMBER"],
            confidence=0.95,
            filtered_message="Filtered content",
            reasoning="Detected sensitive information",
            provider="manual_filter",
        )

        assert detection.has_pii is True
        assert detection.detected_types == ["EMAIL_ADDRESS", "PHONE_NUMBER"]
        assert detection.confidence == 0.95
        assert detection.filtered_message == "Filtered content"
        assert detection.reasoning == "Detected sensitive information"
        assert detection.provider == "manual_filter"


class TestContentFilterService:
    """Test cases for ContentFilterService class"""

    @pytest.mark.unit
    def test_singleton_pattern(self):
        """Test that ContentFilterService follows singleton pattern"""
        service1 = ContentFilterService()
        service2 = ContentFilterService()
        assert service1 is service2

    @pytest.mark.unit
    def test_manual_filter_email_detection(self):
        """Test manual filter detects email addresses"""
        service = ContentFilterService()

        # Test with email in message
        result = service._manual_filter("Contact me at test@example.com")
        assert result["filtered"] is True
        assert result["reason"] == "EMAIL_ADDRESS"

    @pytest.mark.unit
    def test_manual_filter_phone_number_detection(self):
        """Test manual filter detects phone numbers"""
        service = ContentFilterService()

        # Test with Singapore phone number
        result = service._manual_filter("Call me at +6591234567")
        assert result["filtered"] is True
        assert result["reason"] == "PHONE_NUMBER"

        # Test with 8-digit number
        result = service._manual_filter("My number is 91234567")
        assert result["filtered"] is True
        assert result["reason"] == "PHONE_NUMBER"

    @pytest.mark.unit
    def test_manual_filter_unit_number_detection(self):
        """Test manual filter detects unit numbers"""
        service = ContentFilterService()

        # Test with unit number format
        result = service._manual_filter("I live at #12-34")
        assert result["filtered"] is True
        assert result["reason"] == "UNIT_NUMBER"

        result = service._manual_filter("Unit#56-78")
        assert result["filtered"] is True
        assert result["reason"] == "UNIT_NUMBER"

    @pytest.mark.unit
    def test_manual_filter_postal_code_detection(self):
        """Test manual filter detects postal codes"""
        service = ContentFilterService()

        # Test with 6-digit postal code
        result = service._manual_filter("Postal code 123456")
        assert result["filtered"] is True
        assert result["reason"] == "POSTAL_CODE"

        # Test with Singapore postal code context
        result = service._manual_filter("Singapore 654321")
        assert result["filtered"] is True
        assert result["reason"] == "POSTAL_CODE"

    @pytest.mark.unit
    def test_manual_filter_address_detection(self):
        """Test manual filter detects addresses"""
        service = ContentFilterService()

        # Test with address keywords and numbers
        result = service._manual_filter("123 Main Road")
        assert result["filtered"] is True
        assert result["reason"] == "ADDRESS"

        result = service._manual_filter("Block 456 Street")
        assert result["filtered"] is True
        assert result["reason"] == "ADDRESS"

    @pytest.mark.unit
    def test_manual_filter_nric_detection(self):
        """Test manual filter detects NRIC"""
        service = ContentFilterService()

        # Test with NRIC format
        result = service._manual_filter("My NRIC is S1234567A")
        assert result["filtered"] is True
        assert result["reason"] == "SG_NRIC"

        result = service._manual_filter("NRIC: T9876543B")
        assert result["filtered"] is True
        assert result["reason"] == "SG_NRIC"

    @pytest.mark.unit
    def test_manual_filter_no_pii(self):
        """Test manual filter with no PII"""
        service = ContentFilterService()

        result = service._manual_filter("Hello, how are you?")
        assert result["filtered"] is False

    @pytest.mark.unit
    def test_manual_filter_normalizes_whitespace(self):
        """Test manual filter normalizes whitespace in message"""
        service = ContentFilterService()

        # Test with email and extra whitespace
        result = service._manual_filter("Contact me at test @ example . com")
        assert result["filtered"] is True
        assert result["reason"] == "EMAIL_ADDRESS"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_filter_message_manual_filter_triggered(self):
        """Test filter_message when manual filter is triggered"""
        service = ContentFilterService()

        result = await service.filter_message("Contact me at test@example.com")

        assert result["filtered"] is True
        assert "EMAIL_ADDRESS" in result["detected"]
        assert result["confidence"] == 1.0
        assert result["provider"] == "manual_filter"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_filter_message_short_message(self):
        """Test filter_message with short message (less than 10 characters)"""
        service = ContentFilterService()

        result = await service.filter_message("Hi")

        assert result["filtered"] is False
        assert result["confidence"] == 0.0
        assert result["provider"] == "manual_filter"

    @pytest.mark.unit
    @pytest.mark.asyncio
    @patch("api.services.content_filter_service.ContentFilterService._mistral_provider")
    @patch("api.services.content_filter_service.ContentFilterService._huggingface_provider")
    @patch("api.services.content_filter_service.ContentFilterService._groq_provider")
    @patch("api.services.content_filter_service.ContentFilterService._gemini_provider")
    @patch("random.shuffle")
    async def test_filter_message_llm_provider_success(self, mock_shuffle, mock_groq_provider, mock_gemini_provider, mock_huggingface_provider, mock_mistral_provider):
        """Test filter_message with successful LLM provider"""
        # Disable shuffle to keep providers in order
        mock_shuffle.return_value = None
        
        service = ContentFilterService()
        test_message = "This is a longer message that requires LLM processing"
        
        # Make groq provider succeed
        mock_groq_provider.return_value = {
            "filtered": False,
            "content": test_message,
            "detected": [],
            "confidence": 0.0,
            "reasoning": "No PII detected or confidence below threshold.",
            "provider": "llama-3.1-8b-instant",
        }
        
        # Make other providers fail
        mock_gemini_provider.side_effect = Exception("Provider error")
        mock_huggingface_provider.side_effect = Exception("Provider error")
        mock_mistral_provider.side_effect = Exception("Provider error")

        result = await service.filter_message(test_message)
        assert result["filtered"] is False
        assert result["detected"] == []
        assert result["confidence"] == 0.0
        assert result["reasoning"] == "No PII detected or confidence below threshold."
        assert result["provider"] in ["llama-3.1-8b-instant", "gemini-1.5-flash", "mistral-7b-instruct", "microsoft/DialoGPT-medium"]
        assert result["content"] == test_message

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_filter_message_fallback_providers(self):
        """Test filter_message with provider fallback"""
        # Create a fresh instance for testing
        service = ContentFilterService()
        
        # Create mock providers
        async def mock_groq_fail(*args, **kwargs):
            raise Exception("Provider error")
            
        async def mock_huggingface_fail(*args, **kwargs):
            raise Exception("Provider error")
            
        async def mock_mistral_fail(*args, **kwargs):
            raise Exception("Provider error")
            
        async def mock_gemini_success(*args, **kwargs):
            return {
                "filtered": False,
                "content": "This is a longer message that requires LLM processing",
                "detected": [],
                "confidence": 0.0,
                "reasoning": "No PII detected or confidence below threshold.",
                "provider": "gemini-1.5-flash",
            }
        
        # Replace the provider list with our mocks
        service.llm_providers = [
            mock_groq_fail,
            mock_gemini_success,
            mock_huggingface_fail,
            mock_mistral_fail,
        ]

        test_message = "This is a longer message that requires LLM processing"
        result = await service.filter_message(test_message)

        assert result["filtered"] is False
        assert result["detected"] == []
        assert result["confidence"] == 0.0
        assert result["reasoning"] == "No PII detected or confidence below threshold."
        assert "gemini-1.5-flash" in result["provider"]
        assert result["content"] == test_message

    @pytest.mark.asyncio
    async def test_filter_message_all_providers_fail(self):
        """Test filter_message when all LLM providers fail"""
        service = ContentFilterService()

        # Create mock providers that all fail
        async def mock_groq_fail(*args, **kwargs):
            raise Exception("LLaMA provider error")
            
        async def mock_gemini_fail(*args, **kwargs):
            raise Exception("Gemini provider error")
            
        async def mock_huggingface_fail(*args, **kwargs):
            raise Exception("Hugging Face provider error")
            
        async def mock_mistral_fail(*args, **kwargs):
            raise Exception("Mistral provider error")
        
        # Replace the provider list with our failing mocks
        service.llm_providers = [
            mock_groq_fail,
            mock_gemini_fail,
            mock_huggingface_fail,
            mock_mistral_fail,
        ]

        test_message = "This is a longer message that requires LLM processing"

        with pytest.raises(Exception) as exc_info:
            await service.filter_message(test_message)

        # Should raise an exception from one of the providers
        error_message = str(exc_info.value)
        assert any(error in error_message for error in [
            "LLaMA provider error",
            "Gemini provider error", 
            "Hugging Face provider error",
            "Mistral provider error"
        ])

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_filter_message_with_threshold(self):
        """Test filter_message with custom threshold"""
        service = ContentFilterService()

        result = await service.filter_message(
            "Contact me at test@example.com", threshold=0.5
        )

        assert result["filtered"] is True
        assert (
            result["content"] == "Message filtered due to potential PII: EMAIL_ADDRESS"
        )
        assert result["detected"] == ["EMAIL_ADDRESS"]
        assert result["confidence"] == 1.0
        assert result["reasoning"] == "Message flagged by manual filter."
        assert result["provider"] == "manual_filter"

    @pytest.mark.unit
    def test_manual_filter_edge_cases(self):
        """Test manual filter with edge cases"""
        service = ContentFilterService()

        # Test with None message
        with pytest.raises(AttributeError):
            service._manual_filter(None)

        # Test with empty string
        result = service._manual_filter("")
        assert result["filtered"] is False

        # Test with only whitespace
        result = service._manual_filter("   ")
        assert result["filtered"] is False
