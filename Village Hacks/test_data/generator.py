"""
Synthetic test data generator for NotaryGuard.
Generates fake ID card images (PNG) + form1003 JSON files.
No real PII — all data is synthetic.

Usage: python test_data/generator.py
"""

from datetime import date, timedelta
from pathlib import Path
import json

from PIL import Image, ImageDraw, ImageFont
from faker import Faker

fake = Faker()

BASE_DIR = Path(__file__).parent

# ── helpers ──────────────────────────────────────────────────────────────────

def _font(size: int):
    """Return a PIL font. Falls back to default if truetype not available."""
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()


def draw_id_card(
    output_path: Path,
    state: str,
    full_name: str,
    dob_str: str,        # displayed on card as-is (may be wrong format for FAIL)
    expiry_str: str,     # YYYY-MM-DD
    address: str,
    id_number: str,
    width: int = 640,
    height: int = 400,
) -> None:
    """Draw a synthetic driver's license image and save as PNG."""
    img = Image.new("RGB", (width, height), color=(240, 240, 255))
    draw = ImageDraw.Draw(img)

    # Card border
    draw.rectangle([4, 4, width - 5, height - 5], outline=(0, 0, 128), width=3)

    # Header bar
    draw.rectangle([4, 4, width - 5, 50], fill=(0, 0, 128))

    title_font  = _font(20)
    label_font  = _font(14)
    value_font  = _font(16)

    # State + title
    draw.text((20, 12), f"{state} DRIVER LICENSE", fill=(255, 255, 255), font=title_font)

    # Photo placeholder
    draw.rectangle([20, 70, 170, 220], fill=(200, 200, 200), outline=(100, 100, 100))
    draw.text((55, 135), "PHOTO", fill=(80, 80, 80), font=label_font)

    # Fields (right side of photo)
    fields = [
        ("NAME",       full_name),
        ("DOB",        dob_str),
        ("EXP",        expiry_str),
        ("ADDRESS",    address),
        ("ID NO",      id_number),
        ("CLASS",      "D"),
        ("ISS",        state),
    ]
    y = 70
    for label, value in fields:
        draw.text((190, y),      label + ":",  fill=(80, 80, 80),  font=label_font)
        draw.text((270, y),      value,         fill=(10, 10, 80),  font=value_font)
        y += 26

    # Barcode placeholder
    draw.rectangle([20, 300, width - 20, 360], fill=(30, 30, 30))
    draw.text((width // 2 - 40, 320), "||||||||||||||||", fill=(255, 255, 255), font=label_font)

    img.save(output_path, "PNG")
    print(f"  [OK] Image saved: {output_path}")


def write_form1003(output_path: Path, data: dict) -> None:
    output_path.write_text(json.dumps(data, indent=2))
    print(f"  [OK] form1003 saved: {output_path}")


# ── test cases ────────────────────────────────────────────────────────────────

def generate_pass_case():
    print("Generating PASS case...")
    out = BASE_DIR / "pass_case"

    draw_id_card(
        output_path   = out / "id_image.png",
        state         = "CO",
        full_name     = "Jane Marie Doe",
        dob_str       = "04/12/1985",
        expiry_str    = "2028-06-15",
        address       = "1420 Elm St Denver CO 80203",
        id_number     = "D12345678",   # 9 chars — CO length
    )

    write_form1003(out / "form1003.json", {
        "borrower_first_name": "Jane",
        "borrower_last_name":  "Doe",
        "borrower_dob":        "1985-04-12",
        "borrower_address":    "1420 Elm St Denver CO 80203",
        "property_state":      "CO",
    })


def generate_fail_case():
    print("Generating FAIL case...")
    out = BASE_DIR / "fail_case"

    draw_id_card(
        output_path   = out / "id_image.png",
        state         = "TX",
        full_name     = "J. Doe",
        dob_str       = "04/12/85",        # wrong format — 2-digit year
        expiry_str    = "2021-03-01",       # expired > 5 years
        address       = "500 Oak Ave Austin TX 78701",
        id_number     = "TX123456",         # 8 chars — TX length
    )

    write_form1003(out / "form1003.json", {
        "borrower_first_name": "Janet",
        "borrower_last_name":  "Doe",
        "borrower_dob":        "1990-01-01",
        "borrower_address":    "500 Oak Ave Austin TX 78701",
        "property_state":      "TX",
    })


def generate_review_case():
    print("Generating REVIEW case (expiring in 12 days)...")
    out     = BASE_DIR / "review_case"
    expiry  = date.today() + timedelta(days=12)

    draw_id_card(
        output_path   = out / "id_image.png",
        state         = "CO",
        full_name     = "Jennifer Doe",
        dob_str       = "04/12/1985",
        expiry_str    = expiry.isoformat(),
        address       = "1420 Elm St Denver CO 80203",
        id_number     = "D98765432",   # 9 chars — CO length
    )

    write_form1003(out / "form1003.json", {
        "borrower_first_name": "Jen",
        "borrower_last_name":  "Doe",
        "borrower_dob":        "1985-04-12",
        "borrower_address":    "1420 Elm St Denver CO 80203",
        "property_state":      "CO",
    })


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("NotaryGuard — Synthetic Test Data Generator")
    print("=" * 45)
    generate_pass_case()
    generate_fail_case()
    generate_review_case()
    print("=" * 45)
    print("Done. 3 test cases generated.")
