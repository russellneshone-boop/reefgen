# app/token_system.py
from sqlalchemy.orm import Session
from app import crud, models

def award_tokens(db: Session, user_id: int, amount: int = 10):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    return crud.award_tokens(db, user, amount)

def deduct_tokens(db: Session, user_id: int, amount: int = 1):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    return crud.deduct_tokens(db, user, amount)
