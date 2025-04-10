from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security import get_password_hash # Will be created later
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Fetch a user by email from the database."""
        # In a real app, implement DB query
        # result = await self.db.execute(select(User).where(User.email == email))
        # return result.scalars().first()
        logger.debug(f"[STUB] Attempting to get user by email: {email}")
        if email == "existing@example.com": # Dummy check
             # Return a dummy User object matching the model structure
             return User(id=1, email=email, hashed_password="fakepass", is_active=True, role="student")
        return None

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Fetch a user by ID from the database."""
        # In a real app, implement DB query
        # result = await self.db.execute(select(User).where(User.id == user_id))
        # return result.scalars().first()
        logger.debug(f"[STUB] Attempting to get user by ID: {user_id}")
        if user_id == 1: # Dummy check
            return User(id=1, email="existing@example.com", hashed_password="fakepass", is_active=True, role="student")
        return None

    async def create_user(self, user_in: UserCreate) -> User:
        """Create a new user in the database."""
        # In a real app, hash password and save to DB
        hashed_password = get_password_hash(user_in.password)
        # db_user = User(email=user_in.email, hashed_password=hashed_password, full_name=user_in.full_name)
        # self.db.add(db_user)
        # await self.db.commit()
        # await self.db.refresh(db_user)
        # return db_user
        logger.info(f"[STUB] Creating user: {user_in.email}")
        # Return a dummy User object representing the created user
        # Use a different ID to avoid collision with get_user_by_id stub
        return User(id=99, email=user_in.email, hashed_password=hashed_password, full_name=user_in.full_name, is_active=True, role="student")

    async def update_user(self, user_id: int, user_in: UserUpdate) -> Optional[User]:
        """Update an existing user."""
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return None
        
        logger.info(f"[STUB] Updating user: {user_id}")
        # In a real app, update fields selectively and save
        # update_data = user_in.model_dump(exclude_unset=True)
        # if "password" in update_data and update_data["password"]:
        #     db_user.hashed_password = get_password_hash(update_data["password"])
        #     del update_data["password"]
        # for key, value in update_data.items():
        #     setattr(db_user, key, value)
        # await self.db.commit()
        # await self.db.refresh(db_user)

        # Apply updates to the dummy object for the stub
        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
             db_user.hashed_password = get_password_hash(update_data.pop("password"))
        for key, value in update_data.items():
            setattr(db_user, key, value)

        return db_user

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Retrieve a list of users (for admin purposes, perhaps)."""
        # In a real app, implement DB query with pagination
        # result = await self.db.execute(select(User).offset(skip).limit(limit))
        # return result.scalars().all()
        logger.debug(f"[STUB] Getting users (skip={skip}, limit={limit})")
        # Return a dummy list
        dummy_users = [
            User(id=1, email="existing@example.com", hashed_password="fakepass", is_active=True, role="student"),
            User(id=2, email="another@example.com", hashed_password="fakepass2", is_active=True, role="teacher")
        ]
        return dummy_users[skip : skip + limit]
