#!/usr/bin/env python3
"""Command-line interface for QR code generation."""

import argparse
import sys
import qrcode
import segno
from pathlib import Path
from PIL import Image, ImageDraw


def create_qr_code(
    data,
    output_path=None,
    size=10,
    border=4,
    error_correction="M",
    terminal=False,
    fill_color="black",
    back_color="white",
    logo_path=None,
    qr_type="standard",
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
        fill_color: Color of the QR code modules (default: black)
        back_color: Background color (default: white)
        logo_path: Path to logo image to embed in center
        qr_type: Type of QR code (standard, micro)
    """
    # Use segno for micro QR codes and advanced variants
    if qr_type == "micro":
        return _create_micro_qr(
            data,
            output_path,
            size,
            border,
            error_correction,
            terminal,
            fill_color,
            back_color,
        )

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
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        # Add logo if provided
        if logo_path:
            img = _embed_logo(img, logo_path)

        img.save(output_path)
        print(f"QR code saved to: {output_path}")
        return output_path

    return None


def _create_micro_qr(
    data, output_path, size, border, error_correction, terminal, fill_color, back_color
):
    """
    Create a Micro QR code using segno library.

    Args:
        data: The data to encode
        output_path: Path to save the QR code
        size: Scale factor
        border: Border size
        error_correction: Error correction level
        terminal: Display in terminal
        fill_color: Module color
        back_color: Background color

    Returns:
        Path to saved file or None
    """
    # Map error correction to segno format
    # Note: Micro QR codes don't support 'H' error correction
    # Map H to Q (the highest available for Micro QR)
    error_map = {"L": "L", "M": "M", "Q": "Q", "H": "Q"}
    error = error_map.get(error_correction, "M")

    # Create micro QR code
    qr = segno.make_micro(data, error=error)

    # Display in terminal if requested
    if terminal:
        qr.terminal()
        print()

    # Save to file if output path provided
    if output_path:
        qr.save(
            output_path,
            scale=size,
            border=border,
            dark=fill_color,
            light=back_color,
        )
        print(f"Micro QR code saved to: {output_path}")
        return output_path

    return None


def _embed_logo(qr_img, logo_path):
    """
    Embed a logo in the center of a QR code image.

    Args:
        qr_img: The QR code PIL Image
        logo_path: Path to the logo image file

    Returns:
        PIL Image with embedded logo
    """
    # Convert to RGB if needed
    if qr_img.mode != "RGB":
        qr_img = qr_img.convert("RGB")

    # Open and resize logo
    logo = Image.open(logo_path)

    # Calculate logo size (should be about 1/5 of QR code size)
    qr_width, qr_height = qr_img.size
    logo_size = min(qr_width, qr_height) // 5

    # Resize logo maintaining aspect ratio
    logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Create a white background for the logo area
    logo_bg_size = int(logo_size * 1.2)
    logo_bg = Image.new("RGB", (logo_bg_size, logo_bg_size), "white")

    # Paste logo onto white background
    logo_pos = ((logo_bg_size - logo.size[0]) // 2, (logo_bg_size - logo.size[1]) // 2)
    if logo.mode == "RGBA":
        logo_bg.paste(logo, logo_pos, logo)
    else:
        logo_bg.paste(logo, logo_pos)

    # Calculate position to center the logo
    logo_pos_on_qr = (
        (qr_width - logo_bg_size) // 2,
        (qr_height - logo_bg_size) // 2,
    )

    # Paste logo onto QR code
    qr_img.paste(logo_bg, logo_pos_on_qr)

    return qr_img


def _apply_template(template_type, data):
    """
    Apply a content template to format data for specific QR code types.

    Args:
        template_type: Type of template (wifi, vcard, sms, email, phone)
        data: Input data string

    Returns:
        Formatted string for the QR code
    """
    if template_type == "wifi":
        # Expected format: SSID,password,encryption
        # Or interactive prompt if not provided
        parts = data.split(",")
        if len(parts) == 3:
            ssid, password, encryption = parts
        else:
            print("WiFi QR Code Generator")
            ssid = input("Network SSID: ")
            password = input("Password: ")
            encryption = input("Encryption (WPA/WEP/nopass): ").upper()
            if encryption not in ["WPA", "WEP", "NOPASS"]:
                encryption = "WPA"

        return f"WIFI:T:{encryption};S:{ssid};P:{password};;"

    elif template_type == "vcard":
        # Expected format: name,phone,email,organization
        parts = data.split(",")
        if len(parts) >= 2:
            name = parts[0]
            phone = parts[1]
            email = parts[2] if len(parts) > 2 else ""
            org = parts[3] if len(parts) > 3 else ""
        else:
            print("vCard QR Code Generator")
            name = input("Full Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            org = input("Organization (optional): ")

        vcard = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\n"
        if phone:
            vcard += f"TEL:{phone}\n"
        if email:
            vcard += f"EMAIL:{email}\n"
        if org:
            vcard += f"ORG:{org}\n"
        vcard += "END:VCARD"
        return vcard

    elif template_type == "sms":
        # Expected format: phone_number,message
        parts = data.split(",", 1)
        if len(parts) == 2:
            phone, message = parts
        else:
            phone = data
            message = ""
        return f"SMSTO:{phone}:{message}"

    elif template_type == "email":
        # Expected format: email@address,subject,body
        parts = data.split(",", 2)
        if len(parts) >= 1:
            email = parts[0]
            subject = parts[1] if len(parts) > 1 else ""
            body = parts[2] if len(parts) > 2 else ""
        else:
            email = data
            subject = ""
            body = ""
        return f"mailto:{email}?subject={subject}&body={body}"

    elif template_type == "phone":
        # Simple phone number
        return f"tel:{data}"

    return data


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

    parser.add_argument(
        "--fill-color",
        default="black",
        help="Fill color for QR code modules (default: black). Accepts color names or hex codes",
    )

    parser.add_argument(
        "--back-color",
        default="white",
        help="Background color for QR code (default: white). Accepts color names or hex codes",
    )

    parser.add_argument(
        "--logo",
        help="Path to logo image to embed in center of QR code",
    )

    parser.add_argument(
        "--type",
        choices=["standard", "micro"],
        default="standard",
        help="Type of QR code to generate (default: standard)",
    )

    parser.add_argument(
        "--template",
        choices=["wifi", "vcard", "sms", "email", "phone"],
        help="Use a template for specific content types",
    )

    args = parser.parse_args()

    # Handle templates
    if args.template:
        data = _apply_template(args.template, args.data)
    else:
        data = args.data

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
            data=data,
            output_path=output_path,
            size=args.size,
            border=args.border,
            error_correction=args.error_correction,
            terminal=args.terminal,
            fill_color=args.fill_color,
            back_color=args.back_color,
            logo_path=args.logo,
            qr_type=args.type,
        )
        return 0
    except Exception as e:
        print(f"Error generating QR code: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
