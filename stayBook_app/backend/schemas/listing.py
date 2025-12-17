from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid


class LisitngModel(BaseModel):
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    price: int
    location: str = None
    country: str = None
    

class CreateListing(BaseModel):
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    price: int
    location: str = None
    country: str = None
    
    
class UpdateListing(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    price: Optional[int] = None
    location: str = None
    country: str = None
        
        
class CreateReview(BaseModel):
    comment: str = Field(..., min_length=3, max_length=100)
    rating: int = Field(..., ge=1, le=5)
    
    
class ReadReview(CreateReview):
    uid: uuid.UUID
    listing_uid: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ReadListing(LisitngModel):
    uid: uuid.UUID
    reviews: List[ReadReview] = []

    class Config:
        from_attributes = True
