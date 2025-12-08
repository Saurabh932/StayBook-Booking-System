import uuid

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import get_session
from ..models.listing import Listing
from ..schemas.listing import ReadListing, CreateListing, UpateListing

class ListingService:
    
    
    """
        Viewing all Listings
    """
    async def view(self, session : AsyncSession):
        statement = select(Listing)
        listing = await session.execute(statement)
        return listing.scalars().all()
    
    
    """
        Creating a Listing
    """
    async def create(self, payload: CreateListing, session: AsyncSession):
        statement = select(Listing).where(Listing.title == payload.title)
        result = await session.execute(statement)
        existing  = result.scalar_one_or_none()
        
        if existing:
            return {"error":"Lisitng of this title already exists"}
        
        new_listing = Listing(title=payload.title,
                              description=payload.description,
                              image=payload.image,
                              price=payload.price,
                              location=payload.location,
                              country=payload.country)

        session.add(new_listing)
        await session.commit()
        await session.refresh(new_listing)
        return new_listing
        
    
    """
        Searching a Listing
    """
    async def get_listing(self, list_uid: uuid.UUID, session: AsyncSession):
        statement = select(Listing).where(Listing.uid == list_uid)
        result = await session.execute(statement)
        listing = result.scalars().first()
        
        if not listing:
            return {"error":"Listing not present"}
        
        return listing
    
    
    """
        Updating a Listing
    """    
    async def update(self, list_uid: uuid.UUID, payload:UpateListing, session: AsyncSession):
        statement = select(Listing).where(Listing.uid == list_uid)
        result = await session.execute(statement)
        listing = result.scalar_one_or_none()
        
        if not listing:
            return {"error":"Listing does not exist"}
        
        for field, value in payload.model_dump(exclude_unset=True).items():
            if field=="image" and value is not None:
                setattr(listing, field, str(value))
            else:
                setattr(listing, field, value)
            
        session.add(listing)
        await session.commit()
        await session.refresh(listing)
        
        return listing
    
    
    """
        Delete a listing
    """
    async def delete(self, list_uid: uuid.UUID, session: AsyncSession):
        statement = select(Listing).where(Listing.uid == list_uid)
        result = await session.execute(statement)
        listing = result.scalar_one_or_none()
        
        if not listing:
            return {"error":"Listing not exist"}
        
        await session.delete(listing)
        await session.commit()
        return {"message":"Delete successfull"}