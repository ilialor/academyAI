from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Base user schema
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    full_name: Optional[str] = Field(None, description="User's full name")

# Schema for user creation (requires password)
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User's password (min 8 chars)")

# Schema for user update (all fields optional)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="User's email address")
    full_name: Optional[str] = Field(None, description="User's full name")
    password: Optional[str] = Field(None, min_length=8, description="New password (optional, min 8 chars)")
    is_active: Optional[bool] = Field(None, description="User account status")
    role: Optional[str] = Field(None, description="User role (e.g., student, teacher, admin)")

# Schema for user response (doesn't include password)
class UserResponse(UserBase):
    id: int = Field(..., description="Unique user identifier")
    is_active: bool = Field(..., description="User account status")
    role: str = Field(..., description="User role")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last profile update timestamp")

    class Config:
        from_attributes = True # ORM mode
