from typing import List
from fastapi_pagination import Page, add_pagination, paginate
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import crud, models, schemas
from .database import SessionLocal, engine
from typing import Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#buscar en db por fecha: SELECT * FROM table WHERE date_column >= '2014-01-01' AND date_column <= '2015-01-01';
#tas = db.query(models.Task).filter(created_at__range=[today, end_day]).all()
# INSERT INTO news(id,title,date,url,mo) values(2,"leo test 2","2021-10-15","leo.cl.com","adasdsa");
# INSERT INTO has_category(id,title,owner_id) values(1,"sport",1);


# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/news/{new_id}", response_model=schemas.New)
def read_New(new_id: int, db: Session = Depends(get_db)):
    x = crud.get_new(db, new_id=new_id)
    if x is None:
        raise HTTPException(status_code=404, detail="noticia no encontrada bro...")
    return x

@app.get("/news/",response_model = Page[schemas.New])
def get_news(from_:str = "2021-01-01", to_: str = "2021-12-30", db: Session = Depends(get_db)):
    n = crud.by_date(db, from_=from_, to_=to_)
    return paginate(n)

add_pagination(app)
