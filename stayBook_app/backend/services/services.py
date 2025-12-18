import uuid

from sqlmodel import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import get_session
from ..models.listing import Listing, Reviews
from ..schemas.listing import ReadListing, CreateListing, UpdateListing, ReadReview, CreateReview
from ..core.exception import ListingNotFoundError, ReviewsNotFoundError

class ListingService:
    
    
    """
        Viewing all Listings
    """
    async def view(self, session : AsyncSession):
        statement = select(Listing).options(selectinload(Listing.reviews))
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
        statement = select(Listing).where(Listing.uid == list_uid).options(selectinload(Listing.reviews))
        result = await session.execute(statement)
        listing = result.scalars().first()
        
        if not listing:
            raise ListingNotFoundError()
        
        return listing
    
    
    """
        Updating a Listing
    """    
    async def update(self, list_uid: uuid.UUID, payload:UpdateListing, session: AsyncSession):
        statement = select(Listing).where(Listing.uid == list_uid)
        result = await session.execute(statement)
        listing = result.scalar_one_or_none()
        
        if not listing:
            raise ListingNotFoundError()
        
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
            raise ListingNotFoundError()
        
        await session.delete(listing)
        await session.commit()
        return {"message":"Delete successfull"}
    
    
    """
        Reviews Creation
    """
    async def create_review(self, list_uid: uuid.UUID, payload: CreateReview, session: AsyncSession):
        listing = await session.get(Listing, list_uid)
        
        if not listing:
            raise ListingNotFoundError()
        

        listing_reviews = Reviews(listing_uid=list_uid, comment=payload.comment, rating=payload.rating)
        
        session.add(listing_reviews)
        await session.commit()
        await session.refresh(listing_reviews)
        
        return listing_reviews


    """
        Review Deletion
    """
    async def del_review(self, list_uid: uuid.UUID, review_uid: uuid.UUID, session: AsyncSession):
        listing = await session.get(Listing, list_uid)

        if not listing:
            raise ListingNotFoundError()

        statement = select(Reviews).where(Reviews.uid == review_uid, Reviews.listing_uid == list_uid)
        result = await session.execute(statement)
        review = result.scalar_one_or_none()

        if not review:
            raise ReviewsNotFoundError()

        await session.delete(review)
        await session.commit()
