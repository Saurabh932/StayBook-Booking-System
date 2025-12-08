from contextlib import asynccontextmanager
from fastapi import FastAPI
from ..db.session import init_db, get_session
from ..api.listings import list_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("<< Starting StayBook Application >>")
    await init_db()
    
    yield
    
    print(" xx Shutting down StayBook Application")


app = FastAPI(title="StayBook Application", lifespan=lifespan)

app.include_router(list_router)