from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.listing import Users
from ..schemas.listing import UserCreate
from ..core.security import hash_password
from ..core.exception import UserAlreadyExistsError



class UserService:
    async def create_user(self, payload: UserCreate, session: AsyncSession):
        statement = select(Users).where((Users.email == payload.email) | (Users.username == payload.username))
        result = await session.execute(statement)
        existing = result.scalar_one_or_none()
        
        if existing:
            raise UserAlreadyExistsError()
        
        user = Users(username=payload.username, email=payload.email, hash_password=hash_password(payload.password)
)
        
        session.add(user)
        await session.commit()
        await session.refresh(user)
        
        return user