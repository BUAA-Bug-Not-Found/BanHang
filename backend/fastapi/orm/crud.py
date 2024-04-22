from sqlalchemy.orm import Session
from orm import models,schemas

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username,password = user.password, email = user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_checkcode_record(db: Session, record: schemas.EmailCheck):
    if tmp := db.query(models.CheckCode).filter(models.CheckCode.email == record.email).first():
        db.delete(tmp)
    db_check_rec = models.CheckCode(email = record.email, checkcode = record.checkcode)
    db.add(db_check_rec)
    db.commit()
    db.refresh(db_check_rec)
    return db_check_rec