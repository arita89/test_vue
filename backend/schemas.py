from pydantic import BaseModel
from typing import List


class CoffeeCreate(BaseModel):
    name: str
    description: str


class CoffeeOut(CoffeeCreate):
    id: int

    class Config:
        orm_mode = True


class CoffeeImageOut(BaseModel):
    id: int
    filename: str

    class Config:
        orm_mode = True
