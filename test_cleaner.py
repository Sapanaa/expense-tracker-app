from backend.core.cleaner import clean_image
from backend.core.scanner import scan_document

input_image = "data/raw/sample_receipt.png"
output_image = "data/processed/cleaned_receipt.png"
output_scanned_image = "data/processed/scanned_receipt.png"

clean_image(input_image, output_image)

print(f"Cleaned image saved at: {output_image}")

scan_document(input_image, output_scanned_image)

print(f"Scanned image saved at: {output_scanned_image}")