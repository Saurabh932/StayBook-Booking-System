import uuid
from sqlmodel import SQLModel, Field
from sqlalchemy import Column


class Listing(SQLModel , table=True):
    __tablename__="listing"
    uid : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(...)
    description: str = Field(...)
    image: str = Field(...)
    price: str = Field(...)
    location: str = Field(...)
    country: str = Field(...)