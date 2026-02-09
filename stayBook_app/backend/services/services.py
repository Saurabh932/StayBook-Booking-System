from operator import or_
import uuid

from pydantic import ValidationError
from sqlmodel import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import get_session

from ..models.listing import Listing, Reviews, Users
from ..schemas.listing import ReadListing, CreateListing, UpdateListing, ReadReview, CreateReview
from ..core.exception import ListingNotFoundError, ReviewsNotFoundError, ForbiddenError

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
    async def create(self, payload: CreateListing, user: Users, session: AsyncSession):
        statement = select(Listing).where(Listing.title == payload.title)
        result = await session.execute(statement)
        existing  = result.scalar_one_or_none()
        
        if existing:
            raise ValidationError()

        new_listing = Listing(**payload.model_dump(), owner_id = user.uid)

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
        Searching a Listing with keyword
    """
    async def search_listings(self, query: str, session: AsyncSession):
        pattern = f"%{query.lower()}%"

        statement = (select(Listing).where(or_(func.lower(Listing.title).like(pattern),
                    func.lower(Listing.description).like(pattern))).limit(20))

        result = await session.execute(statement)
        return result.scalars().all()

        
    
    """
        Updating a Listing
    """    
    async def update(self, list_uid: uuid.UUID, payload:UpdateListing, user:Users, session: AsyncSession):
        statement = select(Listing).where(Listing.uid == list_uid)
        result = await session.execute(statement)
        listing = result.scalar_one_or_none()
        
        if not listing:
            raise ListingNotFoundError()
        
        if listing.owner_id != user.uid:
            raise ForbiddenError("You do not own this listing.")
        
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
    async def delete(self, list_uid: uuid.UUID, user: Users, session: AsyncSession):
        statement = select(Listing).where(Listing.uid == list_uid)
        result = await session.execute(statement)
        listing = result.scalar_one_or_none()
        
        if not listing:
            raise ListingNotFoundError()
        if listing.owner_id != user.uid:
            raise ForbiddenError("You do not own this listing")
        
        await session.delete(listing)
        await session.commit()
        return {"message":"Delete successfull"}
    
    
    """        ------------------------------------------------------------------------------------------------------
    """
    
    
    """
        Reviews Creation
    """
    async def create_review(self, list_uid: uuid.UUID, payload: CreateReview, current_user: Users, session: AsyncSession):
        listing = await session.get(Listing, list_uid)
        
        if not listing:
            raise ListingNotFoundError()
        

        listing_reviews = Reviews(listing_uid=list_uid, user_id=current_user.uid, comment=payload.comment, rating=payload.rating)
        
        session.add(listing_reviews)
        await session.commit()
        await session.refresh(listing_reviews)
        
        return listing_reviews


    """
        Review Deletion
    """
    async def del_review(self, list_uid: uuid.UUID, review_uid: uuid.UUID, current_user: Users, session: AsyncSession):
        listing = await session.get(Listing, list_uid)

        if not listing:
            raise ListingNotFoundError()

        statement = select(Reviews).where(Reviews.uid == review_uid, Reviews.listing_uid == list_uid)
        result = await session.execute(statement)
        review = result.scalar_one_or_none()

        if not review:
            raise ReviewsNotFoundError()
        
        if review.user_id != current_user.uid:
            raise ForbiddenError("You do not own this review.")

        await session.delete(review)
        await session.commit()
