#!/usr/bin/env python3
"""Command-line interface for QR code generation."""

import argparse
import sys
import qrcode
from pathlib import Path


def create_qr_code(
    data, output_path=None, size=10, border=4, error_correction="M", terminal=False
):
    """
    Create a QR code from the given data.

    Args:
        data: The data to encode in the QR code
        output_path: Path to save the QR code image (PNG)
        size: Size of each box in the QR code (default: 10)
        border: Border size in boxes (default: 4)
        error_correction: Error correction level (L, M, Q, H)
        terminal: Display QR code in terminal using ASCII
    """
    # Map error correction string to qrcode constant
    error_levels = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }

    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_levels.get(
            error_correction, qrcode.constants.ERROR_CORRECT_M
        ),
        box_size=size,
        border=border,
    )

    # Add data and generate
    qr.add_data(data)
    qr.make(fit=True)

    # Display in terminal if requested
    if terminal:
        qr.print_ascii(invert=True)
        print()

    # Save to file if output path provided
    if output_path:
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)
        print(f"QR code saved to: {output_path}")
        return output_path

    return None


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Generate QR codes from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  qrgen "https://example.com"
  qrgen "Hello World" -o qr.png
  qrgen "https://github.com" --terminal
  qrgen "Contact: john@example.com" -o contact.png --size 15
        """,
    )

    parser.add_argument(
        "data", help="The data to encode in the QR code (text, URL, etc.)"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output file path (PNG format). Default: qr_code.png",
        default=None,
    )

    parser.add_argument(
        "-s",
        "--size",
        type=int,
        default=10,
        help="Size of each box in pixels (default: 10)",
    )

    parser.add_argument(
        "-b", "--border", type=int, default=4, help="Border size in boxes (default: 4)"
    )

    parser.add_argument(
        "-e",
        "--error-correction",
        choices=["L", "M", "Q", "H"],
        default="M",
        help="Error correction level: L(7%%), M(15%%), Q(25%%), H(30%%) (default: M)",
    )

    parser.add_argument(
        "-t",
        "--terminal",
        action="store_true",
        help="Display QR code in terminal using ASCII characters",
    )

    args = parser.parse_args()

    # Determine output path
    output_path = args.output
    if not args.terminal and output_path is None:
        output_path = "qr_code.png"

    # Ensure we're doing something (either saving or displaying)
    if not args.terminal and output_path is None:
        print("Error: Must specify --output or --terminal", file=sys.stderr)
        return 1

    try:
        create_qr_code(
            data=args.data,
            output_path=output_path,
            size=args.size,
            border=args.border,
            error_correction=args.error_correction,
            terminal=args.terminal,
        )
        return 0
    except Exception as e:
        print(f"Error generating QR code: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
