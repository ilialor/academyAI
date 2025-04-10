# Mark v1 as a package
# This file will also aggregate routers from endpoints
from fastapi import APIRouter

# Import endpoint routers (will be created next)
from .endpoints.auth import router as auth_router
from .endpoints.users import router as users_router

api_v1_router = APIRouter()

# Include the routers
api_v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(users_router, prefix="/users", tags=["users"])
