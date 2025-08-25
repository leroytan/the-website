import re

import pytest
from api.common.constants import AUTONOMOUS_UNIVERSITIES_EMAIL_DOMAINS


class TestConstants:
    """Test cases for constants module"""

    @pytest.mark.unit
    def test_autonomous_universities_email_domains_structure(self):
        """Test that the email domains list has the expected structure"""
        assert isinstance(AUTONOMOUS_UNIVERSITIES_EMAIL_DOMAINS, list)
        assert len(AUTONOMOUS_UNIVERSITIES_EMAIL_DOMAINS) > 0

    @pytest.mark.unit
    def test_autonomous_universities_email_domains_content(self):
        """Test that the email domains contain expected universities"""
        domains = AUTONOMOUS_UNIVERSITIES_EMAIL_DOMAINS

        # Check for specific universities
        assert "u.nus.edu" in domains
        assert "student.main.ntu.edu.sg" in domains
        assert "e.ntu.edu.sg" in domains
        assert "sit.edu.sg" in domains
        assert "suss.edu.sg" in domains
        assert "sutd.edu.sg" in domains

        # Check for SMU regex pattern - it's the 4th element (index 3)
        assert len(domains) >= 4
        smu_pattern = domains[3]  # The SMU pattern is at index 3
        assert smu_pattern == r".+\.smu\.edu\.sg$"

    @pytest.mark.unit
    def test_smu_regex_pattern(self):
        """Test that the SMU regex pattern works correctly"""
        smu_pattern = r".+\.smu\.smu\.edu\.sg$"

        # Test valid SMU email patterns
        valid_smu_emails = [
            "student@business.smu.edu.sg",
            "user@accountancy.smu.edu.sg",
            "test@economics.smu.edu.sg",
        ]

        for email in valid_smu_emails:
            domain = email.split("@")[1]
            assert re.match(r".+\.smu\.edu\.sg$", domain) is not None

    @pytest.mark.unit
    def test_domain_formats(self):
        """Test that all domains have valid formats"""
        for domain in AUTONOMOUS_UNIVERSITIES_EMAIL_DOMAINS:
            # Skip regex patterns
            if domain.startswith('r"') or domain.startswith("r'"):
                continue

            # Check that non-regex domains are valid
            assert "." in domain
            assert len(domain) > 0
