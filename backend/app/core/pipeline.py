import os
import uuid

# Save scanned image
import cv2
from backend.app.core.scanner import scan_document
from backend.app.core.cleaner import clean_image
from backend.app.core.ocr_engine import extract_text
from backend.app.core.parser import parse_items_and_prices

def process_bill(image_path: str) -> dict:
    """
    Full receipt processing pipeline.

    Args:
        image_path (str): Absolute path to input receipt image

    Returns:
        dict: {
            items: List[str],
            prices: List[float],
            total: float,
            raw_text: str
        }
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")

    # Create temp working directory
    base_dir = os.path.dirname(os.path.abspath(image_path))
    temp_dir = os.path.join(base_dir, "pipeline_temp")
    os.makedirs(temp_dir, exist_ok=True)

    uid = str(uuid.uuid4())

    scanned_path = os.path.join(temp_dir, f"scanned_{uid}.jpg")
    cleaned_path = os.path.join(temp_dir, f"cleaned_{uid}.jpg")

    # 1️⃣ Scan document
    scanned_path = scan_document(image_path, scanned_path)
    if not os.path.exists(scanned_path):
        raise RuntimeError("Scanner failed to produce output image")

    # 2️⃣ Clean image (reads + writes paths)
    clean_image(scanned_path, cleaned_path)

    if not os.path.exists(cleaned_path):
        raise RuntimeError("Cleaner failed to produce output image")

    # 3️⃣ OCR
    raw_text = extract_text(cleaned_path)

    # 4️⃣ Parse text
    parsed  = parse_items_and_prices(raw_text)

    return {
        "items": parsed["items"],
        "prices": parsed["prices"],
        "calculated_total": parsed["calculated_total"],
        "detected_total": parsed["detected_total"],
        "raw_text": raw_text
    }
