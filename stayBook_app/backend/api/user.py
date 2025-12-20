from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.dependencies import get_current_user

from  ..db.session import get_session
from ..schemas.listing import UserCreate, UserRead, LoginRequest, TokenResponse
from ..services.user_serivce import UserService
from ..core.jwt import create_access_token


user_router = APIRouter(prefix="/auth", tags=['auth'])
user_serivce = UserService()


# -----------------------------
# Signup (JSON - frontend)
# -----------------------------
@user_router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    return await user_serivce.create_user(payload, session)


# -----------------------------
# Login (JSON - frontend)
# -----------------------------
@user_router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_session)):
    user = await user_serivce.auth_user(payload.email, payload.password, session)

    token = create_access_token({"sub": str(user.uid)})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "uid": str(user.uid),
            "email": user.email,
            "username": user.username,
        }
    }


# -----------------------------
# Current user (JWT protected)
# -----------------------------
@user_router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_me(current_user = Depends(get_current_user)):
    return current_user