from backend.database import Base, engine
from backend.seed import seed_default_coffees

# Create tables
Base.metadata.create_all(bind=engine)

# Seed with initial data
seed_default_coffees()
