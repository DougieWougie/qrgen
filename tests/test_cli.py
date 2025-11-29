"""Unit tests for CLI functionality."""

import pytest
import sys
from unittest.mock import patch, MagicMock
from qrgen.cli import main


class TestCLI:
    """Tests for the command-line interface."""

    def test_cli_with_output_file(self, tmp_path):
        """Test CLI with output file argument."""
        output_file = tmp_path / "cli_test.png"
        test_args = ["qrgen", "Test data", "-o", str(output_file)]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_with_terminal_flag(self):
        """Test CLI with terminal output flag."""
        test_args = ["qrgen", "Test data", "--terminal"]

        with patch.object(sys, "argv", test_args):
            with patch("qrcode.QRCode.print_ascii"):
                exit_code = main()

        assert exit_code == 0

    def test_cli_default_output(self, tmp_path, monkeypatch):
        """Test CLI with default output filename."""
        # Change to tmp directory to avoid cluttering project
        monkeypatch.chdir(tmp_path)
        test_args = ["qrgen", "Test data"]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert (tmp_path / "qr_code.png").exists()

    def test_cli_custom_size(self, tmp_path):
        """Test CLI with custom size."""
        output_file = tmp_path / "size_test.png"
        test_args = ["qrgen", "Test", "-o", str(output_file), "--size", "15"]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_custom_border(self, tmp_path):
        """Test CLI with custom border."""
        output_file = tmp_path / "border_test.png"
        test_args = ["qrgen", "Test", "-o", str(output_file), "--border", "8"]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    @pytest.mark.parametrize("error_level", ["L", "M", "Q", "H"])
    def test_cli_error_correction_levels(self, tmp_path, error_level):
        """Test CLI with different error correction levels."""
        output_file = tmp_path / f"error_{error_level}.png"
        test_args = [
            "qrgen",
            "Test",
            "-o",
            str(output_file),
            "--error-correction",
            error_level,
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_all_options(self, tmp_path):
        """Test CLI with all options combined."""
        output_file = tmp_path / "all_options.png"
        test_args = [
            "qrgen",
            "https://example.com",
            "-o",
            str(output_file),
            "--size",
            "12",
            "--border",
            "5",
            "--error-correction",
            "H",
            "--terminal",
        ]

        with patch.object(sys, "argv", test_args):
            with patch("qrcode.QRCode.print_ascii"):
                exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_url_data(self, tmp_path):
        """Test CLI with URL data."""
        output_file = tmp_path / "url.png"
        test_args = ["qrgen", "https://github.com", "-o", str(output_file)]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_long_text(self, tmp_path):
        """Test CLI with long text."""
        long_text = "Lorem ipsum " * 100
        output_file = tmp_path / "long.png"
        test_args = ["qrgen", long_text, "-o", str(output_file)]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_special_characters(self, tmp_path):
        """Test CLI with special characters."""
        special_text = "Hello! @#$%^&*()"
        output_file = tmp_path / "special.png"
        test_args = ["qrgen", special_text, "-o", str(output_file)]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_help(self):
        """Test CLI help flag."""
        test_args = ["qrgen", "--help"]

        with patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()

        # Help should exit with code 0
        assert exc_info.value.code == 0

    def test_cli_no_arguments(self):
        """Test CLI with no arguments (should fail)."""
        test_args = ["qrgen"]

        with patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()

        # Should exit with error code
        assert exc_info.value.code != 0

    def test_cli_short_flags(self, tmp_path):
        """Test CLI with short flag versions."""
        output_file = tmp_path / "short_flags.png"
        test_args = [
            "qrgen",
            "Test",
            "-o",
            str(output_file),
            "-s",
            "12",
            "-b",
            "5",
            "-e",
            "Q",
            "-t",
        ]

        with patch.object(sys, "argv", test_args):
            with patch("qrcode.QRCode.print_ascii"):
                exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    @patch("qrgen.cli.create_qr_code")
    def test_cli_handles_exceptions(self, mock_create_qr):
        """Test that CLI handles exceptions gracefully."""
        mock_create_qr.side_effect = Exception("Test error")
        test_args = ["qrgen", "Test", "--terminal"]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 1


class TestCLIVisualCustomization:
    """Tests for CLI visual customization options."""

    def test_cli_custom_fill_color(self, tmp_path):
        """Test CLI with custom fill color."""
        output_file = tmp_path / "blue.png"
        test_args = [
            "qrgen",
            "Test",
            "-o",
            str(output_file),
            "--fill-color",
            "blue",
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_custom_back_color(self, tmp_path):
        """Test CLI with custom background color."""
        output_file = tmp_path / "yellow_bg.png"
        test_args = [
            "qrgen",
            "Test",
            "-o",
            str(output_file),
            "--back-color",
            "yellow",
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_both_colors(self, tmp_path):
        """Test CLI with both custom colors."""
        output_file = tmp_path / "colored.png"
        test_args = [
            "qrgen",
            "Test",
            "-o",
            str(output_file),
            "--fill-color",
            "red",
            "--back-color",
            "white",
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_hex_colors(self, tmp_path):
        """Test CLI with hex color codes."""
        output_file = tmp_path / "hex.png"
        test_args = [
            "qrgen",
            "Test",
            "-o",
            str(output_file),
            "--fill-color",
            "#FF5733",
            "--back-color",
            "#C70039",
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_with_logo(self, tmp_path):
        """Test CLI with logo embedding."""
        from PIL import Image

        logo_file = tmp_path / "logo.png"
        logo_img = Image.new("RGB", (100, 100), color="blue")
        logo_img.save(logo_file)

        output_file = tmp_path / "with_logo.png"
        test_args = [
            "qrgen",
            "Test",
            "-o",
            str(output_file),
            "--logo",
            str(logo_file),
            "--error-correction",
            "H",
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()


class TestCLITemplates:
    """Tests for CLI template options."""

    def test_cli_wifi_template(self, tmp_path):
        """Test CLI with WiFi template."""
        output_file = tmp_path / "wifi.png"
        test_args = [
            "qrgen",
            "MyNetwork,password123,WPA",
            "-o",
            str(output_file),
            "--template",
            "wifi",
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_vcard_template(self, tmp_path):
        """Test CLI with vCard template."""
        output_file = tmp_path / "vcard.png"
        test_args = [
            "qrgen",
            "John Doe,+1234567890,john@example.com,Acme",
            "-o",
            str(output_file),
            "--template",
            "vcard",
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_sms_template(self, tmp_path):
        """Test CLI with SMS template."""
        output_file = tmp_path / "sms.png"
        test_args = [
            "qrgen",
            "1234567890,Hello!",
            "-o",
            str(output_file),
            "--template",
            "sms",
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_email_template(self, tmp_path):
        """Test CLI with email template."""
        output_file = tmp_path / "email.png"
        test_args = [
            "qrgen",
            "test@example.com,Subject,Body",
            "-o",
            str(output_file),
            "--template",
            "email",
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_phone_template(self, tmp_path):
        """Test CLI with phone template."""
        output_file = tmp_path / "phone.png"
        test_args = [
            "qrgen",
            "1234567890",
            "-o",
            str(output_file),
            "--template",
            "phone",
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()


class TestCLIAdvancedTypes:
    """Tests for CLI advanced QR code types."""

    def test_cli_micro_qr(self, tmp_path):
        """Test CLI with Micro QR code type."""
        output_file = tmp_path / "micro.png"
        test_args = ["qrgen", "Small", "-o", str(output_file), "--type", "micro"]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_standard_qr_explicit(self, tmp_path):
        """Test CLI with explicit standard type."""
        output_file = tmp_path / "standard.png"
        test_args = ["qrgen", "Data", "-o", str(output_file), "--type", "standard"]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_micro_qr_with_colors(self, tmp_path):
        """Test CLI Micro QR with custom colors."""
        output_file = tmp_path / "colored_micro.png"
        test_args = [
            "qrgen",
            "Test",
            "-o",
            str(output_file),
            "--type",
            "micro",
            "--fill-color",
            "blue",
            "--back-color",
            "yellow",
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

    def test_cli_combined_features(self, tmp_path):
        """Test CLI with multiple new features combined."""
        from PIL import Image

        logo_file = tmp_path / "logo.png"
        logo_img = Image.new("RGB", (50, 50), color="green")
        logo_img.save(logo_file)

        output_file = tmp_path / "combined.png"
        test_args = [
            "qrgen",
            "MyNetwork,pass123,WPA",
            "-o",
            str(output_file),
            "--template",
            "wifi",
            "--fill-color",
            "darkblue",
            "--back-color",
            "lightblue",
            "--size",
            "15",
            "--error-correction",
            "H",
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()
