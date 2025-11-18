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
