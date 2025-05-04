from fastapi import APIRouter
from .assistants import router as assistants_router
from .vector_stores import router as vector_stores_router

api_router = APIRouter()
api_router.include_router(assistants_router) 
api_router.include_router(vector_stores_router)     