from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from handlers import router


def create_app():
    application = FastAPI()
    application.include_router(router)
    return application


app = create_app()
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")
