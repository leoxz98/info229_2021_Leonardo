from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas


def get_new(db: Session, new_id: int):
    return db.query(models.New).filter(models.New.id == new_id).first()

def by_date(db: Session, from_: str = '2021-01-01', to_: str = '2021-12-30',limit: int = 100):
    return db.query(models.New).filter(and_(models.New.date >= from_, models.New.date < to_)).limit(limit).all()
    