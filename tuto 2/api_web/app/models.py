from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Date
from sqlalchemy.orm import relationship

from .database import Base #Se importa el objeto Base desde el archivo database.py

class New(Base): 

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, index=True)
    date = Column(Date())
    url = Column(String(100))
    mo = Column(String(100))

    category = relationship("Cat", back_populates="owner")

class Cat(Base):

    __tablename__ = "has_category"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    owner_id = Column(Integer, ForeignKey("news.id"))

    owner = relationship("New", back_populates="category")
    