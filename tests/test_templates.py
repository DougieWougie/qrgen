"""Unit tests for content template functionality."""

import pytest
from unittest.mock import patch
from qrgen.cli import _apply_template


class TestTemplates:
    """Tests for content templates."""

    def test_wifi_template_with_data(self):
        """Test WiFi template with provided data."""
        result = _apply_template("wifi", "MyNetwork,password123,WPA")

        assert "WIFI:T:WPA" in result
        assert "S:MyNetwork" in result
        assert "P:password123" in result
        assert result.endswith(";;")

    def test_wifi_template_wep_encryption(self):
        """Test WiFi template with WEP encryption."""
        result = _apply_template("wifi", "TestNet,pass456,WEP")

        assert "WIFI:T:WEP" in result
        assert "S:TestNet" in result
        assert "P:pass456" in result

    def test_wifi_template_nopass(self):
        """Test WiFi template with no password."""
        result = _apply_template("wifi", "OpenNet,,nopass")

        assert "WIFI:T:nopass" in result
        assert "S:OpenNet" in result

    @patch("builtins.input")
    def test_wifi_template_interactive(self, mock_input):
        """Test WiFi template with interactive prompts."""
        mock_input.side_effect = ["HomeNetwork", "secure123", "WPA"]

        result = _apply_template("wifi", "wifi")

        assert "WIFI:T:WPA" in result
        assert "S:HomeNetwork" in result
        assert "P:secure123" in result

    @patch("builtins.input")
    def test_wifi_template_interactive_invalid_encryption(self, mock_input):
        """Test WiFi template defaults to WPA for invalid encryption."""
        mock_input.side_effect = ["TestNet", "pass", "INVALID"]

        result = _apply_template("wifi", "test")

        # Should default to WPA
        assert "WIFI:T:WPA" in result

    def test_vcard_template_full_data(self):
        """Test vCard template with all fields."""
        result = _apply_template(
            "vcard", "John Doe,+1234567890,john@example.com,Acme Corp"
        )

        assert "BEGIN:VCARD" in result
        assert "VERSION:3.0" in result
        assert "FN:John Doe" in result
        assert "TEL:+1234567890" in result
        assert "EMAIL:john@example.com" in result
        assert "ORG:Acme Corp" in result
        assert "END:VCARD" in result

    def test_vcard_template_minimal_data(self):
        """Test vCard template with minimal fields."""
        result = _apply_template("vcard", "Jane Smith,+9876543210")

        assert "BEGIN:VCARD" in result
        assert "FN:Jane Smith" in result
        assert "TEL:+9876543210" in result
        assert "END:VCARD" in result

    def test_vcard_template_no_organization(self):
        """Test vCard template without organization."""
        result = _apply_template("vcard", "Bob Jones,+1111111111,bob@example.com")

        assert "FN:Bob Jones" in result
        assert "TEL:+1111111111" in result
        assert "EMAIL:bob@example.com" in result
        # Should not have ORG field
        assert "ORG:" not in result or "ORG:\n" in result

    @patch("builtins.input")
    def test_vcard_template_interactive(self, mock_input):
        """Test vCard template with interactive prompts."""
        mock_input.side_effect = [
            "Alice Wonder",
            "+5555555555",
            "alice@example.com",
            "Tech Corp",
        ]

        result = _apply_template("vcard", "test")

        assert "FN:Alice Wonder" in result
        assert "TEL:+5555555555" in result
        assert "EMAIL:alice@example.com" in result
        assert "ORG:Tech Corp" in result

    def test_sms_template_with_message(self):
        """Test SMS template with phone and message."""
        result = _apply_template("sms", "1234567890,Hello there!")

        assert result == "SMSTO:1234567890:Hello there!"

    def test_sms_template_phone_only(self):
        """Test SMS template with phone number only."""
        result = _apply_template("sms", "9876543210")

        assert result == "SMSTO:9876543210:"

    def test_sms_template_with_commas_in_message(self):
        """Test SMS template preserves commas in message."""
        result = _apply_template("sms", "1234567890,Hello, how are you?")

        assert result == "SMSTO:1234567890:Hello, how are you?"

    def test_email_template_full(self):
        """Test email template with all fields."""
        result = _apply_template(
            "email", "contact@example.com,Subject Line,Email body text"
        )

        assert result == "mailto:contact@example.com?subject=Subject Line&body=Email body text"

    def test_email_template_address_only(self):
        """Test email template with address only."""
        result = _apply_template("email", "test@example.com")

        assert result == "mailto:test@example.com?subject=&body="

    def test_email_template_with_subject_no_body(self):
        """Test email template with subject but no body."""
        result = _apply_template("email", "info@example.com,Important")

        assert result == "mailto:info@example.com?subject=Important&body="

    def test_phone_template(self):
        """Test phone template."""
        result = _apply_template("phone", "+1234567890")

        assert result == "tel:+1234567890"

    def test_phone_template_no_plus(self):
        """Test phone template without plus sign."""
        result = _apply_template("phone", "9876543210")

        assert result == "tel:9876543210"

    def test_invalid_template_returns_original(self):
        """Test that invalid template returns original data."""
        result = _apply_template("invalid", "test data")

        assert result == "test data"

    def test_none_template_returns_original(self):
        """Test that None template returns original data."""
        result = _apply_template(None, "test data")

        assert result == "test data"
