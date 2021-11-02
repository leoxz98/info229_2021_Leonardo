from typing import List, Optional

from pydantic import BaseModel

class NewSearch(BaseModel):
    id: int

class newBase(BaseModel):
    tittle: str

class New(newBase):
    id: int

    class Config:
        orm_mode = True
        
