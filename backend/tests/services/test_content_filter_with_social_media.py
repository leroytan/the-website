from api.services.content_filter_service import content_filter_service


class TestContentFilterWithSocialMedia:
    """Test that the content filter service properly handles social media content."""

    def test_social_media_urls_are_filtered(self):
        """Test that social media URLs are filtered by the manual filter."""
        # Test Instagram URLs
        result = content_filter_service._manual_filter(
            "Check out my profile: https://instagram.com/username"
        )
        assert result["filtered"] is True
        assert "SOCIAL_MEDIA_SHARE" in result["reason"]

        # Test Twitter/X URLs
        result = content_filter_service._manual_filter(
            "My Twitter: https://twitter.com/username"
        )
        assert result["filtered"] is True
        assert "SOCIAL_MEDIA_SHARE" in result["reason"]

        # Test WhatsApp URLs
        result = content_filter_service._manual_filter(
            "WhatsApp me: https://wa.me/1234567890"
        )
        assert result["filtered"] is True
        assert "SOCIAL_MEDIA_SHARE" in result["reason"]

    def test_social_media_handles_are_filtered(self):
        """Test that social media handles are filtered by the manual filter."""
        # Test @ handles
        result = content_filter_service._manual_filter("Follow me @username")
        assert result["filtered"] is True
        assert "SOCIAL_MEDIA_SHARE" in result["reason"]

        # Test platform cues with handles
        result = content_filter_service._manual_filter("My insta is username")
        assert result["filtered"] is True
        assert "SOCIAL_MEDIA_SHARE" in result["reason"]

    def test_legitimate_content_is_not_filtered(self):
        """Test that legitimate content is not filtered."""
        # Normal conversation
        result = content_filter_service._manual_filter("Hello, how are you?")
        assert result["filtered"] is False

        # Mentions of platforms without sharing
        result = content_filter_service._manual_filter("I like social media")
        assert result["filtered"] is False

        # Email addresses (should be handled by email filter)
        result = content_filter_service._manual_filter("Email me at user@domain.com")
        assert result["filtered"] is True
        assert "EMAIL_ADDRESS" in result["reason"]

    def test_obfuscated_social_media_is_filtered(self):
        """Test that obfuscated social media content is filtered."""
        # Obfuscated @ symbols
        result = content_filter_service._manual_filter("My handle is (at)username")
        assert result["filtered"] is True
        assert "SOCIAL_MEDIA_SHARE" in result["reason"]

        # Obfuscated dots
        result = content_filter_service._manual_filter("My insta is user dot name")
        assert result["filtered"] is True
        assert "SOCIAL_MEDIA_SHARE" in result["reason"]

    def test_discord_tags_are_filtered(self):
        """Test that Discord discriminator tags are filtered."""
        result = content_filter_service._manual_filter("My Discord is username#1234")
        assert result["filtered"] is True
        assert "SOCIAL_MEDIA_SHARE" in result["reason"]

    def test_context_triggers_with_platforms_are_filtered(self):
        """Test that context triggers with platform mentions are filtered."""
        result = content_filter_service._manual_filter("Add me on Instagram")
        assert result["filtered"] is True
        assert "SOCIAL_MEDIA_SHARE" in result["reason"]

        result = content_filter_service._manual_filter("Reach me on Twitter")
        assert result["filtered"] is True
        assert "SOCIAL_MEDIA_SHARE" in result["reason"]
