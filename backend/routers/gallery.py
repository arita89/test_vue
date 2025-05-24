from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path
from typing import List
from .. import models, database

router = APIRouter(prefix="/gallery", tags=["Gallery"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# 📤 Upload images to gallery (not linked to a coffee)
@router.post("/upload")
async def upload_gallery_images(
    images: List[UploadFile] = File(...),
    db: Session = Depends(database.get_db),
):
    uploaded = []
    for img in images:
        file_path = UPLOAD_DIR / img.filename
        with open(file_path, "wb") as f:
            f.write(await img.read())
        db.add(models.CoffeeImage(filename=img.filename, coffee_id=None))
        uploaded.append(img.filename)

    db.commit()
    return {"uploaded": uploaded}


# 🖼️ List all uploaded images (linked and unlinked)
@router.get("/", response_model=List[str])
def list_gallery_images():
    return [
        f"http://localhost:8000/gallery/image/{file.name}"
        for file in UPLOAD_DIR.iterdir()
        if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]
    ]


# 📥 Serve image file
@router.get("/image/{filename}", response_class=FileResponse)
def serve_image_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)
