import cv2
import numpy as np
from pathlib import Path


def clean_image(input_path: str, output_path: str) -> str:
    """
    Clean image to improve OCR accuracy
    """
    img = cv2.imread(str(input_path))

    if img is None:
        raise ValueError("Failed to load image")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise reduction
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive threshold
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # Morphological operations
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    output_path = Path(output_path)
    cv2.imwrite(str(output_path), cleaned)

    return str(output_path)
