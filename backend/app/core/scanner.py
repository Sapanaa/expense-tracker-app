import cv2
import numpy as np
from pathlib import Path
import imutils


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = int(max(widthA, widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = int(max(heightA, heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


def scan_document(input_path: str, output_path: str) -> str:
    """
    Receipt scanner using adaptive threshold + morphology.
    Selects the LARGEST contour (works well for real bills).
    """

    image = cv2.imread(str(input_path))
    if image is None:
        raise ValueError("Could not read input image")

    orig = image.copy()
    h, w = image.shape[:2]

    # Resize for processing
    target_height = 600
    ratio = h / target_height
    resized = cv2.resize(image, (int(w / ratio), target_height))

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # 🔹 Adaptive Threshold (YOUR WORKING METHOD)
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    # 🔹 Morphological Closing (connect receipt edges)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # 🔹 Find contours
    cnts = cv2.findContours(
        closed.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    cnts = imutils.grab_contours(cnts)

    # 🔁 Fallback if no contours
    if not cnts:
        output_path = Path(output_path)
        cv2.imwrite(str(output_path), orig)
        return str(output_path)

    # 🔹 Select LARGEST contour
    receipt_contour = max(cnts, key=cv2.contourArea)

    peri = cv2.arcLength(receipt_contour, True)
    approx = cv2.approxPolyDP(receipt_contour, 0.02 * peri, True)

    output_path = Path(output_path)

    # 🔁 Fallback if not rectangular
    if len(approx) != 4:
        cv2.imwrite(str(output_path), orig)
        return str(output_path)

    # 🔹 Perspective transform
    warped = four_point_transform(
        orig,
        approx.reshape(4, 2) * ratio
    )

    cv2.imwrite(str(output_path), warped)
    return str(output_path)
