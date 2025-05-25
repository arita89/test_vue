from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..schemas import (
    CoffeeCreate,
    CoffeeOut,
    CoffeeImageOut,
    ImageLocationUpdate,
    ImageLocationPatch,
)
from ..models import Coffee, CoffeeImage
from ..core import database
from pathlib import Path
from typing import List

router = APIRouter(prefix="/recipes", tags=["Recipes"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/")
async def upload_recipe(
    name: str = Form(...),
    description: str = Form(...),
    images: List[UploadFile] = File(default=[]),
    db: Session = Depends(database.get_db),
):
    record = Coffee(name=name, description=description)
    db.add(record)
    db.flush()  # ← get record.id here

    for img in images:
        file_path = UPLOAD_DIR / img.filename
        with open(file_path, "wb") as f:
            f.write(await img.read())

        coffee_img = CoffeeImage(filename=img.filename, coffee_id=record.id)  # ✅ FIXED
        db.add(coffee_img)

    db.commit()
    db.refresh(record)
    return {
        "id": record.id,
        "name": record.name,
        "images": [
            img.filename for img in record.images
        ],  # ✅ Better than using raw 'images'
    }


@router.get("/{coffee_id}/images", response_model=List[str])
def get_images_for_coffee(coffee_id: int, db: Session = Depends(database.get_db)):
    coffee = db.query(Coffee).filter(Coffee.id == coffee_id).first()  # ✅ FIXED
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    return [img.filename for img in coffee.images]  # ✅ FIXED


@router.get("/image/{filename}", response_class=FileResponse)
def get_uploaded_image(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(
        file_path, media_type="image/jpeg", headers={"Content-Disposition": "inline"}
    )
