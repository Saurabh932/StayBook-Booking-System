import uuid
from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import get_session
from ..models.listing import Users
from ..schemas.listing import ListingCreated, ReadListing, CreateListing, UpdateListing
from ..core.dependencies import get_current_user
from ..services.services import ListingService


list_service = ListingService()
list_router = APIRouter(prefix="/listings", tags=["listings"])


# -----------------------------
# View all listings (WITH reviews)
# -----------------------------
@list_router.get("/", response_model=List[ReadListing])
async def home(session: AsyncSession = Depends(get_session)):
    return await list_service.view(session)


# -----------------------------
# Create listing (NO reviews)
# -----------------------------
@list_router.post("/", response_model=ListingCreated, status_code=status.HTTP_201_CREATED,)
async def create_listing(payload: CreateListing, session: AsyncSession = Depends(get_session), current_user: Users = Depends(get_current_user)):
    return await list_service.create(payload, current_user, session)


# -----------------------------
# Get single listing (WITH reviews)
# -----------------------------
@list_router.get("/{list_id}", response_model=ReadListing, status_code=status.HTTP_200_OK,)
async def search_listing(list_id: uuid.UUID, session: AsyncSession = Depends(get_session),):
    return await list_service.get_listing(list_id, session)


    
    
# -----------------------------
# Searchin a Listing using keywords
# -----------------------------
@list_router.get("/search", response_model=list[ReadListing])
async def search_listings(q: str = Query(..., min_length=2), session: AsyncSession = Depends(get_session)):
    return await list_service.search_listings(q, session)


# -----------------------------
# Update listing (NO reviews)
# -----------------------------
@list_router.patch("/{list_id}", response_model=ListingCreated, status_code=status.HTTP_200_OK,)
async def update_listing(list_id: uuid.UUID, payload: UpdateListing, session: AsyncSession = Depends(get_session), current_user: Users = Depends(get_current_user)):
    return await list_service.update(list_id, payload, current_user, session)


# -----------------------------
# Delete listing
# -----------------------------
@list_router.delete("/{list_id}",status_code=status.HTTP_200_OK,)
async def delete_listing(list_id: uuid.UUID, session: AsyncSession = Depends(get_session), current_user: Users = Depends(get_current_user)):
    await list_service.delete(list_id, current_user, session)
    return {"message": "Listing deleted"}
