
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .. import models, schemas, database

router = APIRouter(prefix="/coffees", tags=["Coffees"])

@router.post("/", response_model=schemas.CoffeeOut)
def add_coffee(coffee: schemas.CoffeeCreate, db: Session = Depends(database.get_db)):
    try:
        new = models.Coffee(**coffee.dict())
        db.add(new)
        db.flush()
        db.refresh(new)
        return new
    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Could not create coffee (possibly duplicate name).")

@router.get("/", response_model=list[schemas.CoffeeOut])
def list_coffees(db: Session = Depends(database.get_db)):
    return db.query(models.Coffee).all()

@router.delete("/{coffee_id}")
def delete_coffee(coffee_id: int, db: Session = Depends(database.get_db)):
    coffee = db.query(models.Coffee).get(coffee_id)
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")
    try:
        db.delete(coffee)
        db.flush()
        return {"detail": "Deleted"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error deleting coffee")
