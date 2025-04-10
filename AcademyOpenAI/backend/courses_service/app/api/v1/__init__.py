from fastapi import APIRouter
from app.api.v1.endpoints.courses import router as courses_router

api_v1_router = APIRouter()

# Include the courses router
api_v1_router.include_router(courses_router, prefix="/courses", tags=["courses"])

# Add other v1 routers here if needed

# Re-export for cleaner imports
courses = courses_router