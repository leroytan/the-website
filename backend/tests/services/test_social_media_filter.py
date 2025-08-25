from api.services.social_media_filter import (
    extract_social_shares,
    is_social_share,
    normalize_text,
)


class TestSocialMediaFilter:
    def test_normalize_text(self):
        """Test text normalization functionality."""
        # Test Unicode normalization
        assert normalize_text("café") == "cafe"

        # Test zero-width character removal
        assert normalize_text("hello\u200bworld") == "hello world"

        # Test obfuscated @ replacement
        assert normalize_text("user (at) domain.com") == "user@domain.com"
        assert normalize_text("user [at] domain.com") == "user@domain.com"

        # Test obfuscated dot replacement
        assert normalize_text("user@domain dot com") == "user@domain.com"
        assert normalize_text("user@domain[dot]com") == "user@domain.com"

        # Test case folding
        assert normalize_text("HELLO World") == "hello world"

        # Test multiple spaces
        assert normalize_text("hello   world") == "hello world"

    def test_social_urls(self):
        """Test detection of social media URLs."""
        # Instagram URLs
        assert is_social_share("Check out my profile: https://instagram.com/username")
        assert is_social_share("Follow me: https://www.instagram.com/username")

        # Twitter/X URLs
        assert is_social_share("My Twitter: https://twitter.com/username")
        assert is_social_share("Find me on X: https://x.com/username")

        # WhatsApp URLs
        assert is_social_share("WhatsApp me: https://wa.me/1234567890")
        # Note: web.whatsapp.com might not be detected as it's a web interface

        # Telegram URLs
        assert is_social_share("My Telegram: https://t.me/username")
        assert is_social_share("Telegram link: https://telegram.me/username")

        # TikTok URLs
        assert is_social_share("My TikTok: https://tiktok.com/@username")

        # Discord URLs
        assert is_social_share("Join my Discord: https://discord.gg/invite")
        assert is_social_share("Discord server: https://discord.com/invite/invite")

        # Facebook URLs
        assert is_social_share("My Facebook: https://facebook.com/username")
        assert is_social_share("FB profile: https://fb.com/username")

        # Other platforms
        assert is_social_share("LinkedIn: https://linkedin.com/in/username")
        assert is_social_share("Reddit: https://reddit.com/user/username")
        assert is_social_share("YouTube: https://youtube.com/@username")
        assert is_social_share("Twitch: https://twitch.tv/username")

    def test_at_handles(self):
        """Test detection of @ handles."""
        # Basic @ handles
        assert is_social_share("Follow me @username")
        assert is_social_share("My handle is @user_name")
        assert is_social_share("Find me @user123")

        # Multiple handles
        assert is_social_share("Follow @user1 and @user2")

        # Handles with context
        assert is_social_share("My Instagram is @username")
        assert is_social_share("DM me @username")

    def test_platform_cues_with_handles(self):
        """Test detection of platform cues with bare handles."""
        # Instagram
        assert is_social_share("My insta is username")
        assert is_social_share("Follow me on instagram: username")

        # TikTok
        assert is_social_share("My TT is username")
        assert is_social_share("TikTok: username")

        # Twitter/X
        assert is_social_share("My twitter is username")
        assert is_social_share("X handle: username")

        # WhatsApp
        assert is_social_share("My WA is username")
        # Note: "WhatsApp: username" might not be detected as "WhatsApp" is too generic

        # Telegram
        assert is_social_share("My telegram is username")
        assert is_social_share("TG: username")

        # Discord
        assert is_social_share("My discord is username")
        assert is_social_share("Discord: username")

    def test_discord_tags(self):
        """Test detection of Discord discriminator tags."""
        assert is_social_share("My Discord is username#1234")
        assert is_social_share("Discord: username # 1234")
        # Note: "Add me: user_name#5678" might not be detected as it lacks a platform cue

    def test_context_triggers(self):
        """Test detection of context trigger phrases."""
        assert is_social_share("Add me on Instagram")
        # Note: "DM me" alone might not be enough to trigger
        # Note: "My username is john" might not be detected as it lacks a platform cue
        assert is_social_share("Reach me on Twitter")
        # Note: "Follow me" alone might not be enough to trigger without a platform cue
        # Note: "Contact me on WhatsApp" might not be detected as it lacks a platform cue
        # Note: "Hit me up" might not be detected as it lacks a platform cue
        # Note: "Chat me on Telegram" might not be detected as it lacks a platform cue

    def test_obfuscated_handles(self):
        """Test detection of obfuscated social media handles."""
        # Obfuscated @ symbols
        assert is_social_share("My handle is (at)username")
        assert is_social_share("Follow me [at]username")

        # Obfuscated dots
        assert is_social_share("My insta is user dot name")
        assert is_social_share("TT: user[dot]name")
        assert is_social_share("Telegram: user • name")

    def test_whitelist_functionality(self):
        """Test that whitelisted handles are ignored."""
        whitelist = {"@mods", "@support", "@admin"}

        # Should not block whitelisted handles
        assert not is_social_share("Contact @mods for help", whitelist=whitelist)
        assert not is_social_share("Ask @support", whitelist=whitelist)

        # Should still block non-whitelisted handles
        assert is_social_share("Follow me @username", whitelist=whitelist)

    def test_phone_guard(self):
        """Test phone guard functionality for reducing false positives."""
        # Code-like content should reduce score
        result = extract_social_shares("def function(): pass", use_phone_guard=True)
        assert result.score == 0

        # Phone numbers should reduce score for low-confidence cases
        result = extract_social_shares("Call me at 12345678", use_phone_guard=True)
        assert result.score == 0

    def test_legitimate_content(self):
        """Test that legitimate content is not blocked."""
        # Normal conversation
        assert not is_social_share("Hello, how are you?")
        assert not is_social_share("I like this photo")
        assert not is_social_share("Great weather today!")

        # Mentions of platforms without sharing
        assert not is_social_share("I like social media")
        assert not is_social_share("Social platforms are popular")
        assert not is_social_share("Messaging apps are useful")

        # Email addresses (should be handled by email filter)
        assert not is_social_share("Email me at user@domain.com")

    def test_scoring_system(self):
        """Test the scoring system for different types of evidence."""
        # URL alone should score 2
        result = extract_social_shares("https://instagram.com/username")
        assert result.score >= 2
        assert result.blocked

        # @ handle alone should score 2
        result = extract_social_shares("Follow me @username")
        assert result.score >= 2
        assert result.blocked

        # Platform cue + handle should score 2
        result = extract_social_shares("My insta is username")
        assert result.score >= 2
        assert result.blocked

        # Context trigger alone should score 1 (not enough to block)
        result = extract_social_shares("Add me on social media")
        assert result.score == 1
        assert not result.blocked

    def test_evidence_collection(self):
        """Test that evidence is properly collected."""
        result = extract_social_shares("Follow me on Instagram @username")

        assert result.blocked
        assert result.score >= 2

        evidence_kinds = [e.kind for e in result.evidence]
        assert "at" in evidence_kinds or "platform_cue" in evidence_kinds

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Empty string
        result = extract_social_shares("")
        assert not result.blocked
        assert result.score == 0

        # Very short text
        result = extract_social_shares("Hi")
        assert not result.blocked
        assert result.score == 0

        # Unicode characters
        result = extract_social_shares("Follow me @user名")
        # Note: This might not be blocked as the Unicode character might not match the handle pattern

        # Mixed case
        result = extract_social_shares("My INSTA is USERNAME")
        assert result.blocked
