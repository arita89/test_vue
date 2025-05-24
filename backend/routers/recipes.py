from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from .. import models, database
import os
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
    coffee = models.Coffee(name=name, description=description)
    db.add(coffee)
    db.flush()  # get coffee.id

    for img in images:
        file_path = UPLOAD_DIR / img.filename
        with open(file_path, "wb") as f:
            f.write(await img.read())

        coffee_img = models.CoffeeImage(filename=img.filename, coffee_id=coffee.id)
        db.add(coffee_img)

    db.commit()
    db.refresh(coffee)
    return {
        "id": coffee.id,
        "name": coffee.name,
        "images": [img.filename for img in coffee.images],
    }


@router.get("/{coffee_id}/images", response_model=List[str])
def get_images_for_coffee(coffee_id: int, db: Session = Depends(database.get_db)):
    coffee = db.query(models.Coffee).filter(models.Coffee.id == coffee_id).first()
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    return [img.filename for img in coffee.images]


@router.get("/image/{filename}", response_class=FileResponse)
def get_uploaded_image(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(
        file_path, media_type="image/jpeg", headers={"Content-Disposition": "inline"}
    )
