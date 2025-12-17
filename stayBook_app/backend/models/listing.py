from typing import List
import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, ForeignKey


class Listing(SQLModel , table=True):
    __tablename__="listing"
    uid : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(...)
    description: str = Field(...)
    image: str = Field(...)
    price: int = Field(...)
    location: str = Field(...)
    country: str = Field(...)
    reviews: List["Reviews"] = Relationship(back_populates="listing", sa_relationship_kwargs={"cascade":"all, delete"})
    
    
class Reviews(SQLModel, table=True):
    __tablename__="reviews"
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    listing_uid: uuid.UUID = Field(sa_column=Column(ForeignKey("listing.uid", ondelete="CASCADE"), nullable=False))
    comment: str = Field(..., min_length=3, max_length=100)
    rating: int = Field(..., ge=1, le=5)
    created_at: datetime = Field(default_factory=datetime.now, sa_column=Column(DateTime(timezone=True)))
    listing: Listing = Relationship(back_populates="reviews")