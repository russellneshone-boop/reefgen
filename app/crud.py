# app/crud.py
from sqlalchemy.orm import Session
from app import models, schemas

# User CRUD
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"  # Replace with real hash
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Reef CRUD
def get_reef_by_name(db: Session, name: str):
    return db.query(models.Reef).filter(models.Reef.name == name).first()

def create_reef(db: Session, reef: schemas.ReefCreate):
    db_reef = models.Reef(name=reef.name, location=reef.location)
    db.add(db_reef)
    db.commit()
    db.refresh(db_reef)
    return db_reef

# ReefScan CRUD
def create_scan(db: Session, user_id: int, reef_id: int, image_path: str, date_taken, diagnosis: str):
    db_scan = models.ReefScan(
        user_id=user_id,
        reef_id=reef_id,
        image_path=image_path,
        date_taken=date_taken,
        diagnosis=diagnosis
    )
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan

def get_scans_by_reef(db: Session, reef_id: int):
    return db.query(models.ReefScan).filter(models.ReefScan.reef_id == reef_id).all()

# Token system
def award_tokens(db: Session, user: models.User, amount: int):
    user.tokens += amount
    db.commit()
    db.refresh(user)
    return user

def deduct_tokens(db: Session, user: models.User, amount: int):
    if user.tokens < amount:
        raise Exception("Not enough tokens")
    user.tokens -= amount
    db.commit()
    db.refresh(user)
    return user
