from pydantic import BaseModel, Field

from typing import List, Optional


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


class ImageLocationUpdate(BaseModel):
    filename: str = Field(..., example="coffee.jpg")
    latitude: float = Field(..., example=41.9028)
    longitude: float = Field(..., example=12.4964)


class ImageLocationPatch(BaseModel):
    filename: str = Field(..., example="coffee.jpg")
    latitude: Optional[float] = Field(None, example=45.07)
    longitude: Optional[float] = Field(None, example=7.69)
