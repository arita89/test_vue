from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import coffees, recipes

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

app.include_router(coffees.router)
app.include_router(recipes.router)
