import uuid
from typing import List
from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from ..db.session import get_session
from ..models.listing import Listing
from ..schemas.listing import ReadListing, CreateListing, UpdateListing
from ..services.services import ListingService


list_service = ListingService()


list_router = APIRouter(prefix="/listings", tags=["listings"])
templates = Jinja2Templates(directory="frontend/pages")


"""
    Home Page - View all
"""
@list_router.get("/", response_model=List[ReadListing])
async def home(session:AsyncSession = Depends(get_session)):
    listing = await list_service.view(session)
    return listing
    # return templates.TemplateResponse("index.html", {"listing": listing, "request":request})
    


"""
    Creating a Listiing 
"""
@list_router.post("/", response_model=ReadListing, status_code=status.HTTP_200_OK)
async def create_listing(pay_load: CreateListing, session: AsyncSession = Depends(get_session)):
    new_listing = await list_service.create(pay_load, session)
    return new_listing



"""
    Searching a Listing
"""
@list_router.get("/{list_id}", response_model=ReadListing, status_code=status.HTTP_200_OK)
async def search_listing(list_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    listing = await list_service.get_listing(list_id, session)
    return listing



"""
    Updating a Listing
"""
@list_router.patch("/{list_id}", response_model=ReadListing, status_code=status.HTTP_200_OK)
async def update_listing(list_id: uuid.UUID, payload: UpdateListing, session: AsyncSession = Depends(get_session)):
    update_listing = await list_service.update(list_id, payload, session)
    return update_listing


"""
    Deleting a Listing
"""
@list_router.delete("/{list_id}", status_code=status.HTTP_200_OK)
async def delete_listing(list_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    await list_service.delete(list_id, session)
    return {"message": f"Student deleted"}