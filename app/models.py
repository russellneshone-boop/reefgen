# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    tokens = Column(Integer, default=10)

    scans = relationship("ReefScan", back_populates="user")

class Reef(Base):
    __tablename__ = "reefs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)

    scans = relationship("ReefScan", back_populates="reef")

class ReefScan(Base):
    __tablename__ = "reef_scans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    reef_id = Column(Integer, ForeignKey("reefs.id"))
    image_path = Column(String)
    date_taken = Column(DateTime(timezone=True), server_default=func.now())
    diagnosis = Column(String, nullable=True)

    user = relationship("User", back_populates="scans")
    reef = relationship("Reef", back_populates="scans")
