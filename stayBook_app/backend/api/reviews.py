import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.dependencies import get_current_user
from ..models.listing import Users

from ..db.session import get_session
from ..schemas.listing import ReadReview, CreateReview
from ..services.services import ListingService

review_router = APIRouter(
    prefix="/listings/{list_id}/reviews",
    tags=["reviews"]
)

list_service = ListingService()


"""
Create a Review
"""
@review_router.post("", response_model=ReadReview, status_code=status.HTTP_201_CREATED)
async def create_review(list_id: uuid.UUID, payload: CreateReview, current_user: Users = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await list_service.create_review(list_id, payload, current_user, session)


"""
Delete a Review
"""
@review_router.delete("/{review_id}", status_code=status.HTTP_200_OK)
async def delete_review(list_id: uuid.UUID, review_id: uuid.UUID, current_user: Users = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    await list_service.del_review(list_id, review_id, current_user, session)
    return {"message": "Review deleted successfully"}
