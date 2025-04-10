from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.services.auth_service import auth_service # For get_current_user dependency
from app.services.user_service import UserService

router = APIRouter()

# Dependency to get the current active user
# You might want to add more role-based access control here later
async def get_current_active_user(
    current_user: UserResponse = Depends(auth_service.get_current_user)
) -> UserResponse:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get current logged-in user's profile."""
    print(f"[ENDPOINT_STUB] Getting profile for user: {current_user.email}")
    # The dependency already fetches and validates the user
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_users_me(
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Update current logged-in user's profile."""
    user_service = UserService(db)
    # In a real app, prevent users from changing their role or ID via this endpoint
    # Also handle email uniqueness update carefully
    updated_user = await user_service.update_user(user_id=current_user.id, user_in=user_in)
    if not updated_user:
         # Should not happen if get_current_active_user worked, but for safety
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    print(f"[ENDPOINT_STUB] Updated profile for user: {current_user.email}")
    return UserResponse.model_validate(updated_user)

# Example of an admin-only endpoint (requires further authorization logic)
@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    # current_user: UserResponse = Depends(get_current_active_user) # Add role check here
):
    """Retrieve a list of users (example, might require admin role)."""
    # Add authorization check: e.g., if current_user.role != 'admin': raise HTTPException(...)
    print(f"[ENDPOINT_STUB] Getting user list (skip={skip}, limit={limit})")
    user_service = UserService(db)
    users = await user_service.get_users(skip=skip, limit=limit)
    # Convert list of DB models to list of Pydantic models
    return [UserResponse.model_validate(user) for user in users]
