from fastapi import APIRouter

from app.api.routes import classify, message, physician

api_router = APIRouter()
api_router.include_router(classify.router)
api_router.include_router(message.router)
api_router.include_router(physician.router)