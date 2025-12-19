from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
import uuid


# -----------------------------
# Shared base (no relationships)
# -----------------------------
class ListingBase(BaseModel):
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    price: int
    location: Optional[str] = None
    country: Optional[str] = None


# -----------------------------
# Create (request only)
# -----------------------------
class CreateListing(ListingBase):
    pass


# -----------------------------
# Update (partial update)
# -----------------------------
class UpdateListing(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    price: Optional[int] = None
    location: Optional[str] = None
    country: Optional[str] = None


# -----------------------------
# Reviews
# -----------------------------
class CreateReview(BaseModel):
    comment: str = Field(..., min_length=3, max_length=100)
    rating: int = Field(..., ge=1, le=5)


class ReadReview(CreateReview):
    uid: uuid.UUID
    listing_uid: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


# -----------------------------
# POST response (NO relationships)
# -----------------------------
class ListingCreated(ListingBase):
    uid: uuid.UUID

    class Config:
        from_attributes = True


# -----------------------------
# GET response (WITH relationships)
# -----------------------------
class ReadListing(ListingCreated):
    reviews: List[ReadReview] = []

    class Config:
        from_attributes = True



# -----------------------------
# User
# -----------------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr
    

class UserCreate(UserBase):
    password: str = Field(min_length=4)
    
    
class UserRead(UserBase):
    uid: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True