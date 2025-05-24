from .models import Coffee
from .database import SessionLocal


def seed_default_coffees():
    defaults = [
        {
            "name": "Espresso",
            "description": "Brew under pressure.",
            "location": "Rome, Italy",
            "latitude": 41.9028,
            "longitude": 12.4964,
        },
        {
            "name": "Latte",
            "description": "Add steamed milk to espresso.",
            "location": "Milan, Italy",
            "latitude": 45.4642,
            "longitude": 9.19,
        },
        {
            "name": "Cappuccino",
            "description": "Equal parts espresso, milk, foam.",
            "location": "Vienna, Austria",
            "latitude": 48.2082,
            "longitude": 16.3738,
        },
        {
            "name": "Mocha Latte",
            "description": "Chocolate + espresso + steamed milk.",
            "location": "Quito, Ecuador",
            "latitude": -0.1807,
            "longitude": -78.4678,
        },
    ]

    db = SessionLocal()
    for item in defaults:
        exists = db.query(Coffee).filter_by(name=item["name"]).first()
        if not exists:
            db.add(Coffee(**item))
    db.commit()
    db.close()
