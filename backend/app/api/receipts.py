from fastapi import APIRouter, UploadFile, File, HTTPException
import os, shutil, uuid

from backend.app.core.pipeline import process_bill

router = APIRouter()

@router.post("/process-receipt")
async def process_receipt(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    os.makedirs("temp", exist_ok=True)
    temp_path = os.path.join("temp", f"{uuid.uuid4()}{ext}")

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = process_bill(temp_path)
        return result
    finally:
        # cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
