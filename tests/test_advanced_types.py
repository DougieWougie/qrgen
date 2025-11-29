"""Unit tests for advanced QR code types (Micro QR, etc.)."""

import pytest
from unittest.mock import patch, MagicMock
from qrgen.cli import create_qr_code, _create_micro_qr


class TestMicroQRCodes:
    """Tests for Micro QR code generation."""

    def test_create_micro_qr_code(self, tmp_path):
        """Test basic Micro QR code creation."""
        output_file = tmp_path / "micro_qr.png"
        result = create_qr_code(
            "Hello", output_path=str(output_file), qr_type="micro"
        )

        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_create_micro_qr_code_short_text(self, tmp_path):
        """Test Micro QR code with very short text."""
        output_file = tmp_path / "micro_short.png"
        result = create_qr_code("Hi", output_path=str(output_file), qr_type="micro")

        assert output_file.exists()

    def test_create_micro_qr_code_with_size(self, tmp_path):
        """Test Micro QR code with custom size."""
        output_file = tmp_path / "micro_sized.png"
        result = create_qr_code(
            "Test", output_path=str(output_file), qr_type="micro", size=15
        )

        assert output_file.exists()

    def test_create_micro_qr_code_with_border(self, tmp_path):
        """Test Micro QR code with custom border."""
        output_file = tmp_path / "micro_border.png"
        result = create_qr_code(
            "Test", output_path=str(output_file), qr_type="micro", border=2
        )

        assert output_file.exists()

    @pytest.mark.parametrize("error_level", ["L", "M", "Q", "H"])
    def test_create_micro_qr_error_correction_levels(self, tmp_path, error_level):
        """Test Micro QR code with different error correction levels."""
        output_file = tmp_path / f"micro_{error_level}.png"
        result = create_qr_code(
            "Test",
            output_path=str(output_file),
            qr_type="micro",
            error_correction=error_level,
        )

        assert output_file.exists()

    def test_create_micro_qr_with_colors(self, tmp_path):
        """Test Micro QR code with custom colors."""
        output_file = tmp_path / "micro_colored.png"
        result = create_qr_code(
            "Color",
            output_path=str(output_file),
            qr_type="micro",
            fill_color="blue",
            back_color="yellow",
        )

        assert output_file.exists()

    @patch("builtins.print")
    def test_create_micro_qr_terminal_output(self, mock_print, tmp_path):
        """Test Micro QR code with terminal output."""
        with patch("segno.QRCode.terminal") as mock_terminal:
            result = create_qr_code("Test", qr_type="micro", terminal=True)

            # Verify terminal was called
            mock_terminal.assert_called_once()

    def test_create_micro_qr_terminal_and_file(self, tmp_path):
        """Test Micro QR code with both terminal and file output."""
        output_file = tmp_path / "micro_both.png"

        with patch("segno.QRCode.terminal"):
            result = create_qr_code(
                "Test", output_path=str(output_file), qr_type="micro", terminal=True
            )

        assert output_file.exists()

    def test_create_standard_qr_type(self, tmp_path):
        """Test explicitly specifying standard QR type."""
        output_file = tmp_path / "standard_qr.png"
        result = create_qr_code(
            "Standard", output_path=str(output_file), qr_type="standard"
        )

        assert output_file.exists()

    def test_create_qr_default_type(self, tmp_path):
        """Test QR code creation defaults to standard type."""
        output_file = tmp_path / "default_qr.png"
        result = create_qr_code("Default", output_path=str(output_file))

        assert output_file.exists()

    def test_micro_qr_direct_function(self, tmp_path):
        """Test _create_micro_qr function directly."""
        output_file = tmp_path / "direct_micro.png"
        result = _create_micro_qr(
            data="Direct",
            output_path=str(output_file),
            size=10,
            border=4,
            error_correction="M",
            terminal=False,
            fill_color="black",
            back_color="white",
        )

        assert output_file.exists()
        assert result == str(output_file)

    def test_micro_qr_no_output_path(self):
        """Test Micro QR code without output path."""
        result = _create_micro_qr(
            data="Test",
            output_path=None,
            size=10,
            border=4,
            error_correction="M",
            terminal=False,
            fill_color="black",
            back_color="white",
        )

        assert result is None

    def test_micro_qr_numbers_only(self, tmp_path):
        """Test Micro QR code with numeric data."""
        output_file = tmp_path / "micro_numbers.png"
        result = create_qr_code(
            "123456", output_path=str(output_file), qr_type="micro"
        )

        assert output_file.exists()

    def test_micro_qr_alphanumeric(self, tmp_path):
        """Test Micro QR code with alphanumeric data."""
        output_file = tmp_path / "micro_alnum.png"
        result = create_qr_code(
            "ABC123", output_path=str(output_file), qr_type="micro"
        )

        assert output_file.exists()
