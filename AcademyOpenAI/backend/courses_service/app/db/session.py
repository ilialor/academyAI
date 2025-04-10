async def get_db():
    """Dependency function to get a (dummy) database session."""
    # In a real application, this would create and yield a database session
    # For now, it does nothing as CourseService uses in-memory storage
    yield None
