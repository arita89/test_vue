from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..schemas import CoffeeCreate, CoffeeOut
from ..models import Coffee
from ..core import database

router = APIRouter(prefix="/coffees", tags=["Coffees"])


@router.post("/", response_model=CoffeeOut)
def add_coffee(payload: CoffeeCreate, db: Session = Depends(database.get_db)):
    try:
        new = Coffee(**payload.dict())
        db.add(new)
        db.flush()
        db.refresh(new)
        return new
    except SQLAlchemyError:
        raise HTTPException(
            status_code=400, detail="Could not create coffee (possibly duplicate name)."
        )


@router.get("/", response_model=list[CoffeeOut])
def list_coffees(db: Session = Depends(database.get_db)):
    return db.query(Coffee).all()


@router.delete("/{coffee_id}")
def delete_coffee(coffee_id: int, db: Session = Depends(database.get_db)):
    record = db.query(Coffee).get(coffee_id)
    if not record:
        raise HTTPException(status_code=404, detail="Coffee not found")
    try:
        db.delete(record)
        db.commit()
        return {"detail": "Deleted"}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting coffee")


# Optional static brew instructions fallback
brew_instructions = {
    "Espresso": "Brew under pressure.",
    "Latte": "Add steamed milk to espresso.",
    "Cappuccino": "Use equal parts espresso, milk, and foam.",
}


@router.get("/brew/{coffee_id}")
def brew_coffee(coffee_id: int, db: Session = Depends(database.get_db)):
    coffee = db.query(Coffee).filter(Coffee.id == coffee_id).first()
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    # Try static instructions first, fallback to description
    instructions = brew_instructions.get(coffee.name, coffee.description)
    return {"name": coffee.name, "instructions": instructions}


@router.get("/map")
def coffee_locations(db: Session = Depends(database.get_db)):
    coffees = (
        db.query(Coffee)
        .filter(Coffee.latitude.isnot(None), Coffee.longitude.isnot(None))
        .all()
    )
    return [
        {
            "id": c.id,
            "name": c.name,
            "location": c.location,
            "latitude": c.latitude,
            "longitude": c.longitude,
        }
        for c in coffees
    ]
