from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path
from typing import List
import exifread

from ..schemas import CoffeeCreate, CoffeeOut, ImageLocationUpdate, ImageLocationPatch
from ..models import CoffeeImage
from ..core import database

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
        db.add(CoffeeImage(filename=img.filename, coffee_id=None))
        uploaded.append(img.filename)

    db.commit()
    return {"uploaded": uploaded}


@router.post("/upload-with-meta")
async def upload_with_location(
    image: UploadFile = File(...),
    db: Session = Depends(database.get_db),
):
    file_path = UPLOAD_DIR / image.filename
    with open(file_path, "wb") as f:
        f.write(await image.read())

    gps = extract_gps(file_path)
    db.add(
        CoffeeImage(
            filename=image.filename,
            coffee_id=None,
            latitude=gps.get("latitude") if gps else None,
            longitude=gps.get("longitude") if gps else None,
        )
    )
    db.commit()

    return {
        "filename": image.filename,
        "location": gps,  # Might be None
    }


@router.post("/set-location")
def set_image_location(
    payload: ImageLocationUpdate,
    db: Session = Depends(database.get_db),
):
    img = db.query(CoffeeImage).filter_by(filename=payload.filename).first()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    img.latitude = payload.latitude
    img.longitude = payload.longitude
    db.commit()
    return {"status": "updated"}


@router.patch("/image/location")
def patch_image_location(
    patch: ImageLocationPatch,
    db: Session = Depends(database.get_db),
):
    img = db.query(CoffeeImage).filter_by(filename=patch.filename).first()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")

    if patch.latitude is not None:
        img.latitude = patch.latitude
    if patch.longitude is not None:
        img.longitude = patch.longitude

    db.commit()
    return {
        "filename": img.filename,
        "latitude": img.latitude,
        "longitude": img.longitude,
    }


@router.delete("/image/{filename}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(filename: str, db: Session = Depends(database.get_db)):
    img = db.query(CoffeeImage).filter_by(filename=filename).first()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found in database")

    db.delete(img)
    db.commit()

    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        file_path.unlink()
    return


# 🖼️ List all uploaded images (linked and unlinked)
@router.get("/", response_model=List[str])
def list_gallery_images():
    return [
        f"http://localhost:8000/gallery/image/{file.name}"
        for file in UPLOAD_DIR.iterdir()
        if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"]
    ]


@router.get("/image/{filename}", response_class=FileResponse)
def serve_image_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)


@router.get("/map")
def gallery_locations(db: Session = Depends(database.get_db)):
    images = db.query(CoffeeImage).filter(CoffeeImage.latitude.isnot(None)).all()
    return [
        {
            "id": img.id,
            "filename": img.filename,
            "latitude": img.latitude,
            "longitude": img.longitude,
            "url": f"http://localhost:8000/gallery/image/{img.filename}",
        }
        for img in images
    ]


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
