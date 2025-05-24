from .models import Coffee
from .database import SessionLocal


def seed_default_coffees():
    defaults = [
        {"name": "Espresso", "description": "Brew under pressure."},
        {"name": "Latte", "description": "Add steamed milk to espresso."},
        {"name": "Cappuccino", "description": "Equal parts espresso, milk, foam."},
    ]
    db = SessionLocal()
    for item in defaults:
        exists = db.query(Coffee).filter_by(name=item["name"]).first()
        if not exists:
            db.add(Coffee(**item))
    db.commit()
    db.close()
