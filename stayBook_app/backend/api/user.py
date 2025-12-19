from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from  ..db.session import get_session
from ..schemas.listing import UserCreate, UserRead
from ..services.user_serivce import UserService


user_router = APIRouter(prefix="/auth", tags=['auth'])
user_serivce = UserService()


@user_router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    return await user_serivce.create_user(payload, session)