from typing import List, Optional
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
import uuid

# Dummy in-memory storage for courses
_courses_db = {}

class CourseService:
    def __init__(self, db_session=None): # db_session is unused for now
        pass

    async def get_courses(self, skip: int = 0, limit: int = 100) -> List[CourseResponse]:
        """Retrieve a list of courses with pagination."""
        courses_list = list(_courses_db.values())
        # Apply pagination
        return courses_list[skip : skip + limit]

    async def create_course(self, course_data: CourseCreate) -> CourseResponse:
        """Create a new course."""
        new_id = str(uuid.uuid4())
        new_course = CourseResponse(id=new_id, **course_data.model_dump())
        _courses_db[new_id] = new_course
        return new_course

    async def get_course(self, course_id: str) -> Optional[CourseResponse]:
        """Get a specific course by its ID."""
        return _courses_db.get(course_id)

    async def update_course(self, course_id: str, course_update: CourseUpdate) -> Optional[CourseResponse]:
        """Update an existing course."""
        if course_id not in _courses_db:
            return None
        
        existing_course = _courses_db[course_id]
        update_data = course_update.model_dump(exclude_unset=True) # Get only fields that were actually set

        # Update the existing course fields
        for field, value in update_data.items():
            setattr(existing_course, field, value)

        _courses_db[course_id] = existing_course # Update in the 'db'
        return existing_course

    async def delete_course(self, course_id: str) -> bool:
        """Delete a course by its ID."""
        if course_id in _courses_db:
            del _courses_db[course_id]
            return True
        return False
