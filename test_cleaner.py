import os
import cv2

from backend.app.core.scanner import scan_document
from backend.app.core.cleaner import clean_image
# ---------- CONFIG ----------
from backend.app.core.parser import parse_items_and_prices
from backend.app.core.ocr_engine import extract_text
IMAGE_PATH = "data/raw/sample_receipt.png"   # change if needed
OUTPUT_DIR = "data/test_outputs"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "scanned_test.png")
# ----------------------------

def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Input image:", IMAGE_PATH)
    print("Output image will be saved to:", OUTPUT_PATH)

    # Run scanner
    scanned_path = scan_document(IMAGE_PATH, OUTPUT_PATH)

    # Verify result
    if not os.path.exists(scanned_path):
        print("❌ Scanner did not save output")
        return

    scanned_img = cv2.imread(scanned_path)
    if scanned_img is None:
        print("❌ Saved file exists but OpenCV cannot read it")
        return

    print("✅ Scanner test successful!")
    print("Saved scanned image at:", scanned_path)
    print("Scanned image shape:", scanned_img.shape)

    # Clean image
    cleaned_path = os.path.join(OUTPUT_DIR, "cleaned_test.png")
    clean_image(scanned_path, cleaned_path)

    # Verify result
    if not os.path.exists(cleaned_path):
        print("❌ Cleaner did not save output")
        return

    cleaned_img = cv2.imread(cleaned_path)
    if cleaned_img is None:
        print("❌ Saved file exists but OpenCV cannot read it")
        return

    print("✅ Cleaner test successful!")
    print("Saved cleaned image at:", cleaned_path)
    print("Cleaned image shape:", cleaned_img.shape)

    #ocr engine
    ocr_text = extract_text(cleaned_path)
    print(ocr_text)

    parsed = parse_items_and_prices(ocr_text)
    print(parsed)

if __name__ == "__main__":
    main()
