from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --- USER SCHEMAS ---

# Base fields shared across User schemas
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None

# Schema used for user registration (includes password)
class UserCreate(UserBase):
    password: str

# Schema used for user responses (excluding password)
class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True

# Internal schema used in authentication (includes hashed password)
class User(UserOut):
    hashed_password: str

# Token schema for JWT token payload
class TokenData(BaseModel):
    username: Optional[str] = None


# --- REEF SCHEMAS ---

# Shared fields for reefs
class ReefBase(BaseModel):
    reef_name: str
    location: Optional[str] = None  # Extend with more fields as needed

# Used when creating a new reef entry
class ReefCreate(ReefBase):
    pass  # Add more fields as necessary

# Returned to clients (includes ID)
class ReefOut(ReefBase):
    id: int

    class Config:
        from_attributes = True


# --- REEF SCAN OUTPUT ---

class ReefScanOut(BaseModel):
    id: int
    timestamp: datetime
    image_url: str
    reef_name: str

    class Config:
        from_attributes = True
class Token(BaseModel):
    access_token: str
    token_type: str






