from pydantic import BaseModel
from typing import List


class CoffeeCreate(BaseModel):
    name: str
    description: str
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class CoffeeOut(CoffeeCreate):
    id: int

    class Config:
        orm_mode = True


class CoffeeImageOut(BaseModel):
    id: int
    filename: str

    class Config:
        orm_mode = True
