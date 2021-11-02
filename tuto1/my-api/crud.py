from sqlalchemy.orm import Session

from . import models, schemas


def get_new(db: Session, new_id: int):
    return db.query(models.New).filter(models.New.id == new_id).first()


