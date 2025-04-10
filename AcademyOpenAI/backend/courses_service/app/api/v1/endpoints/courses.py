from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.services.course_service import CourseService
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[CourseResponse])
async def get_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db = Depends(get_db)
):
    """Get all courses with pagination"""
    course_service = CourseService(db)
    courses = await course_service.get_courses(skip=skip, limit=limit)
    return courses

@router.post("/", response_model=CourseResponse, status_code=201)
async def create_course(
    course: CourseCreate,
    db = Depends(get_db)
):
    """Create a new course"""
    course_service = CourseService(db)
    return await course_service.create_course(course)

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: str,
    db = Depends(get_db)
):
    """Get a specific course by ID"""
    course_service = CourseService(db)
    course = await course_service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: str,
    course_update: CourseUpdate,
    db = Depends(get_db)
):
    """Update a course"""
    course_service = CourseService(db)
    updated_course = await course_service.update_course(course_id, course_update)
    if not updated_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return updated_course

@router.delete("/{course_id}", status_code=204)
async def delete_course(
    course_id: str,
    db = Depends(get_db)
):
    """Delete a course"""
    course_service = CourseService(db)
    deleted = await course_service.delete_course(course_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Course not found")
    return None