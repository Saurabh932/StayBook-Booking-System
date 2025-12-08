from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from ..config.config import config


""" Creating async database engine """
async_engine = create_async_engine(config.DATABSE_URL, 
                                   echo=True, future=True)


"""  Global sessionmaker need for background scripting  """
async_session_maker = sessionmaker(bind=async_engine,
                             expire_on_commit=False,
                             class_=AsyncSession)



""" Initalizing database and creating tables """
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        
    print("*** Table Created Successfully ***")
    
    
    
""" Creates dependency routes session for FastAPI """
async def get_session() -> AsyncSession:
    sessionlocal = sessionmaker(bind=async_engine,
                                class_=AsyncSession,
                                expire_on_commit=False)
    
    async with sessionlocal() as session:
        yield session