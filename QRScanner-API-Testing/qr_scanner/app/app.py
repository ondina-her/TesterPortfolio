# Run with:
#   .\.venv\Scripts\activate.bat
#   uvicorn app.app:app --reload
# Then open http://127.0.0.1:8000/ in the browser.

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import models
from .database import engine
from .routers import pages

app = FastAPI()

# Serve everything under ./static at the URL prefix /static.
app.mount("/static", StaticFiles(directory="static", check_dir=False), name="static")

models.Base.metadata.create_all(bind=engine)

app.include_router(pages.router)