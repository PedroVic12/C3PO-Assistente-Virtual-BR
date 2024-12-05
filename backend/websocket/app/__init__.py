from fastapi import FastAPI
from app.routes.chat_routes import router as chat_router

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(chat_router)
    return app
