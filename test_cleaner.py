from backend.core.pipeline import process_bill
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

image_path = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "sample_receipt.png"
)

print("Image path:", image_path)
print("Exists:", os.path.exists(image_path))

result = process_bill(image_path)
print(result)
