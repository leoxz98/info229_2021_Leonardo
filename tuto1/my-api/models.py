from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base #Se importa el objeto Base desde el archivo database.py

class New(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key = True, index=True)
    tittle = Column(String)
    date = Column(String)
    url = Column(String)
    media_outlet = Column(String)

    category = relationship("has_category",back_populates="reference")

class H_C(Base):
    __tablename__ = "has_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    reference_id = Column(Integer, ForeignKey("news.id"))
    reference = relationship("New",back_populates="has_category")






