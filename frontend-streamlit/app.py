import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
import streamlit as st
from PIL import Image
from backend.app.core.scanner import scan_document
from backend.app.core.cleaner import clean_image
from backend.app.core.ocr_engine import extract_text
from backend.app.core.parser import parse_items_and_prices
os.makedirs(DATA_DIR, exist_ok=True)

st.set_page_config(page_title="Receipt OCR Pipeline", layout="wide")

st.title("🧾 Receipt OCR Pipeline Debugger")

# uploaded_file = st.file_uploader(
#     "Upload a receipt image",
#     type=["png", "jpg", "jpeg"]
# )

# if uploaded_file:
#     os.makedirs("temp", exist_ok=True)

#     input_path = f"temp/{uploaded_file.name}"
#     scanned_path = f"temp/scanned_{uploaded_file.name}"
#     cleaned_path = f"temp/cleaned_{uploaded_file.name}"

#     with open(input_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     # -------- PIPELINE --------
#     scan_document(input_path, scanned_path)
#     clean_image(scanned_path, cleaned_path)
#     ocr_text = extract_text(cleaned_path)
#     parsed = parse_receipt(ocr_text)

#     # -------- DISPLAY --------
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.subheader("Original")
#         st.image(Image.open(input_path), use_column_width=True)

#     with col2:
#         st.subheader("Scanned")
#         st.image(Image.open(scanned_path), use_column_width=True)

#     with col3:
#         st.subheader("Cleaned")
#         st.image(Image.open(cleaned_path), use_column_width=True)

#     st.subheader("📄 OCR Text")
#     st.text_area("Extracted Text", ocr_text, height=200)

#     st.subheader("📊 Parsed Output")
#     st.json(parsed)


if st.button("Use sample receipt image"):
    input_path = os.path.join(DATA_DIR, "raw/sample_receipt.png")
    scanned_path = os.path.join(DATA_DIR, "scanned_receipt.jpg")
    cleaned_path = os.path.join(DATA_DIR, "cleaned_receipt.jpg")



if "input_path" in locals():

    scan_document(input_path, scanned_path)
    clean_image(scanned_path, cleaned_path)
    ocr_text = extract_text(cleaned_path)
    print(ocr_text)
    parsed = parse_items_and_prices(ocr_text)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Original")
        st.image(Image.open(input_path), use_column_width=True)

    with col2:
        st.subheader("Scanned")
        st.image(Image.open(scanned_path), use_column_width=True)

    with col3:
        st.subheader("Cleaned")
        st.image(Image.open(cleaned_path), use_column_width=True)

    st.subheader("📄 OCR Text")
    st.text_area("Extracted Text", ocr_text, height=200)

    st.subheader("📊 Parsed Output")
    st.json(parsed)