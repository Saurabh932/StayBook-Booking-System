from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from ..db.session import init_db
from ..api.listings import list_router


BASE_DIR = Path(__file__).resolve().parent.parent.parent

FRONTEND_DIR = BASE_DIR / "frontend"
PAGES_DIR = FRONTEND_DIR / "pages"
ASSETS_DIR = FRONTEND_DIR / "assets"
TEMPLATES_DIR = FRONTEND_DIR / "templates" 

print("BASE_DIR:", BASE_DIR)
print("PAGES_DIR:", PAGES_DIR)
print("ASSETS_DIR:", ASSETS_DIR)



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("<< Starting StayBook Application >>")
    await init_db()
    print("DB INIT: start")
    yield
    print("DB INIT: end")
    print(" xx Shutting down StayBook Application")


app = FastAPI(title="StayBook Application", lifespan=lifespan)

app.include_router(list_router)

# Serve static assets first
app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

app.mount("/templates", StaticFiles(directory=str(TEMPLATES_DIR)), name="templates")

# Then serve pages fallback
app.mount("/", StaticFiles(directory=str(PAGES_DIR), html=True), name="pages")
