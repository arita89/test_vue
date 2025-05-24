from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base


class Coffee(Base):
    __tablename__ = "coffees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    location = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    images = relationship("CoffeeImage", back_populates="coffee")


class CoffeeImage(Base):
    __tablename__ = "coffee_images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    coffee_id = Column(Integer, ForeignKey("coffees.id"), nullable=True)
    coffee = relationship("Coffee", back_populates="images")
