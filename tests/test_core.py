"""Unit tests for core QR code generation functionality."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from qrgen.cli import create_qr_code


class TestCreateQRCode:
    """Tests for the create_qr_code function."""

    def test_create_qr_code_saves_file(self, tmp_path):
        """Test that QR code is saved to file."""
        output_file = tmp_path / "test_qr.png"
        result = create_qr_code("Test data", output_path=str(output_file))

        assert result == str(output_file)
        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_create_qr_code_with_url(self, tmp_path):
        """Test QR code generation with URL."""
        output_file = tmp_path / "url_qr.png"
        result = create_qr_code("https://example.com", output_path=str(output_file))

        assert result == str(output_file)
        assert output_file.exists()

    def test_create_qr_code_custom_size(self, tmp_path):
        """Test QR code with custom size."""
        output_file = tmp_path / "large_qr.png"
        result = create_qr_code(
            "Test data",
            output_path=str(output_file),
            size=20
        )

        assert output_file.exists()
        # Larger size should produce larger file (generally)
        assert output_file.stat().st_size > 0

    def test_create_qr_code_custom_border(self, tmp_path):
        """Test QR code with custom border."""
        output_file = tmp_path / "border_qr.png"
        result = create_qr_code(
            "Test data",
            output_path=str(output_file),
            border=10
        )

        assert output_file.exists()

    @pytest.mark.parametrize("error_level", ['L', 'M', 'Q', 'H'])
    def test_create_qr_code_error_correction_levels(self, tmp_path, error_level):
        """Test all error correction levels."""
        output_file = tmp_path / f"qr_{error_level}.png"
        result = create_qr_code(
            "Test data",
            output_path=str(output_file),
            error_correction=error_level
        )

        assert output_file.exists()

    def test_create_qr_code_invalid_error_correction(self, tmp_path):
        """Test that invalid error correction defaults to M."""
        output_file = tmp_path / "default_qr.png"
        result = create_qr_code(
            "Test data",
            output_path=str(output_file),
            error_correction='INVALID'
        )

        # Should not raise error, should default to M
        assert output_file.exists()

    def test_create_qr_code_no_output_path(self):
        """Test QR code generation without output path."""
        result = create_qr_code("Test data", output_path=None, terminal=False)

        assert result is None

    @patch('builtins.print')
    def test_create_qr_code_terminal_output(self, mock_print, tmp_path):
        """Test terminal output mode."""
        with patch('qrcode.QRCode.print_ascii') as mock_ascii:
            result = create_qr_code("Test data", terminal=True)

            # Verify print_ascii was called
            mock_ascii.assert_called_once_with(invert=True)
            # Verify print was called for newline
            assert mock_print.called

    @patch('builtins.print')
    def test_create_qr_code_terminal_and_file(self, mock_print, tmp_path):
        """Test both terminal output and file saving."""
        output_file = tmp_path / "both_qr.png"

        with patch('qrcode.QRCode.print_ascii') as mock_ascii:
            result = create_qr_code(
                "Test data",
                output_path=str(output_file),
                terminal=True
            )

            # Verify both file and terminal output
            assert output_file.exists()
            mock_ascii.assert_called_once()

    def test_create_qr_code_empty_string(self, tmp_path):
        """Test QR code generation with empty string."""
        output_file = tmp_path / "empty_qr.png"
        result = create_qr_code("", output_path=str(output_file))

        # QR code library should handle empty string
        assert output_file.exists()

    def test_create_qr_code_long_text(self, tmp_path):
        """Test QR code generation with long text."""
        long_text = "A" * 1000
        output_file = tmp_path / "long_qr.png"
        result = create_qr_code(long_text, output_path=str(output_file))

        assert output_file.exists()

    def test_create_qr_code_special_characters(self, tmp_path):
        """Test QR code with special characters."""
        special_text = "Hello! @#$%^&*() 你好 🎉"
        output_file = tmp_path / "special_qr.png"
        result = create_qr_code(special_text, output_path=str(output_file))

        assert output_file.exists()
