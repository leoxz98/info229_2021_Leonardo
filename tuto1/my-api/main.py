from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/news/{news_id}", response_model=schemas.New)
def read_new(news_id: int, db: Session = Depends(get_db)):
    db_new = crud.get_new(db, user_id=news_id)
    if db_new is None:
        raise HTTPException(status_code=404, detail="New not found")
    return db_new
