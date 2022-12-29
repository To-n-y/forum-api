from fastapi import FastAPI
from handlers import router


def create_app():
    application = FastAPI()
    application.include_router(router)
    return application


app = create_app()
