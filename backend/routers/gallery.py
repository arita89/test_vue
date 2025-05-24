from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path
from typing import List
import exifread
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


@router.post("/upload-with-meta")
async def upload_with_location(
    image: UploadFile = File(...), db: Session = Depends(database.get_db)
):
    file_path = UPLOAD_DIR / image.filename
    with open(file_path, "wb") as f:
        f.write(await image.read())

    gps = extract_gps(file_path)

    db.add(models.CoffeeImage(filename=image.filename, coffee_id=None))
    db.commit()

    return {
        "filename": image.filename,
        "location": gps,  # Could be None if no GPS found
    }


@router.post("/set-location")
def set_image_location(data: dict, db: Session = Depends(database.get_db)):
    img = db.query(models.CoffeeImage).filter_by(filename=data["filename"]).first()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    img.latitude = data["latitude"]
    img.longitude = data["longitude"]
    db.commit()
    return {"status": "updated"}


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


def extract_gps(filepath: Path):
    with open(filepath, "rb") as f:
        tags = exifread.process_file(f, stop_tag="GPS GPSLongitude")

    try:
        lat = tags["GPS GPSLatitude"]
        lon = tags["GPS GPSLongitude"]
        lat_ref = tags["GPS GPSLatitudeRef"].values
        lon_ref = tags["GPS GPSLongitudeRef"].values

        def to_decimal(coord, ref):
            d, m, s = [x.num / x.den for x in coord.values]
            decimal = d + m / 60 + s / 3600
            return -decimal if ref in ["S", "W"] else decimal

        return {
            "latitude": to_decimal(lat, lat_ref),
            "longitude": to_decimal(lon, lon_ref),
        }
    except KeyError:
        return None
