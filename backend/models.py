from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Coffee(Base):
    __tablename__ = "coffees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    images = relationship("CoffeeImage", back_populates="coffee")


class CoffeeImage(Base):
    __tablename__ = "coffee_images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    coffee_id = Column(Integer, ForeignKey("coffees.id"))
    coffee = relationship("Coffee", back_populates="images")
