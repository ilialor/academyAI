from pydantic import BaseModel, Field
from typing import Optional
import uuid

# Base model for common course attributes
class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Course title")
    description: Optional[str] = Field(None, max_length=500, description="Course description")

# Model for creating a new course (inherits from Base)
class CourseCreate(CourseBase):
    pass # No additional fields needed for creation in this basic version

# Model for updating an existing course (all fields optional)
class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Course title")
    description: Optional[str] = Field(None, max_length=500, description="Course description")

# Model for returning course data in responses (includes ID)
class CourseResponse(CourseBase):
    id: str = Field(..., description="Unique course identifier")

    class Config:
        from_attributes = True # Enable ORM mode for compatibility with database models
        # Example data for documentation generation (optional)
        json_schema_extra = {
            "example": {
                "id": str(uuid.uuid4()),
                "title": "Introduction to FastAPI",
                "description": "Learn the basics of building APIs with FastAPI."
            }
        }
