from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from pathlib import Path

from ..db.session import init_db
from ..api.listings import list_router
from ..core.exception import StayBookError
from ..core.error_handler import staybook_exception_handler, generic_exception_handler, validation_exception_handler
from ..middleware.logging import logging_middleware
from ..middleware.not_found import not_found_middleware

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

# Middleware
app.middleware("http")(logging_middleware)
app.middleware("http")(not_found_middleware)


# Exception Handlers
app.add_exception_handler(StayBookError, staybook_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)



app.include_router(list_router)

# Serve static assets first
app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

app.mount("/templates", StaticFiles(directory=str(TEMPLATES_DIR)), name="templates")

# Then serve pages fallback
app.mount("/", StaticFiles(directory=str(PAGES_DIR), html=True), name="pages")
