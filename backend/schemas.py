
from pydantic import BaseModel

class CoffeeCreate(BaseModel):
    name: str
    description: str

class CoffeeOut(CoffeeCreate):
    id: int

    class Config:
        orm_mode = True
