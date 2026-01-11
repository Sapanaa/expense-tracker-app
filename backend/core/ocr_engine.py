import cv2
import pytesseract
import numpy as np
import os


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image_path: str) -> str:
    """
    Extract raw text from a cleaned receipt image.

    Args:
        image_path (str): Absolute path to cleaned image

    Returns:
        str: OCR extracted text
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"OCR input image not found: {image_path}")

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"OpenCV failed to load image: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Upscale for better OCR
    gray = cv2.resize(
        gray, None,
        fx=2, fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # Light blur (avoid edge artifacts)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # OTSU threshold (balanced for text + numbers)
    thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    # Ensure black text on white background
    if np.mean(thresh) < 127:
        thresh = 255 - thresh

    # OCR config (balanced)
    config = r"--oem 3 --psm 6"

    text = pytesseract.image_to_string(
        thresh,
        config=config
    )

    return text.strip()
