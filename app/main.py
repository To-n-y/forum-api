from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.handlers import router
from scripts.create_db import main as create_db


def create_app():
    create_db()
    application = FastAPI()
    application.include_router(router)
    return application


app = create_app()
app.include_router(router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
