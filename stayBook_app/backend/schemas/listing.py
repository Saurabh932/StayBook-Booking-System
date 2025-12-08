from typing import Optional
import uuid
from pydantic import BaseModel, HttpUrl


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
    
    
class UpateListing(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    price: Optional[int] = None
    location: str = None
    country: str = None
    

class ReadListing(LisitngModel):
    uid : uuid.UUID
    
    class Config:
        from_attribute = True