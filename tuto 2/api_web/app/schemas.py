from typing import List, Optional, Dict, Any, Type
from datetime import datetime, date
from pydantic import BaseModel, Field


class Cat(BaseModel):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True
        allow_mutation = True



class New(BaseModel):
    id: int
    title: str
    date: date
    url: str
    mo: str

    class Config:
        orm_mode = True
        allow_mutation = True