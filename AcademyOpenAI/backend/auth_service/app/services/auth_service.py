from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.services.user_service import UserService
from app.schemas.token import Token, TokenPayload
from app.schemas.user import UserResponse
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token # Will be created later
from app.db.session import get_db
from typing import Optional

# This defines the URL where clients send username/password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login") # Matches the login endpoint path

class AuthService:

    async def authenticate_user(self, email: str, password: str, db: AsyncSession) -> Optional[UserResponse]:
        """Authenticate a user based on email and password."""
        user_service = UserService(db)
        user = await user_service.get_user_by_email(email)
        if not user:
            print(f"[AUTH_STUB] Authentication failed: User not found - {email}")
            return None
        if not verify_password(password, user.hashed_password):
            print(f"[AUTH_STUB] Authentication failed: Invalid password for user - {email}")
            return None
        print(f"[AUTH_STUB] Authentication successful for user: {email}")
        return UserResponse.model_validate(user) # Convert DB model to Pydantic model

    def create_user_tokens(self, user_id: int) -> Token:
        """Generate access and refresh tokens for a user."""
        # In JWT, 'sub' (subject) usually contains the user identifier
        access_token = create_access_token(data={"sub": str(user_id)})
        refresh_token = create_refresh_token(data={"sub": str(user_id)})
        print(f"[AUTH_STUB] Tokens created for user ID: {user_id}")
        return Token(access_token=access_token, refresh_token=refresh_token)

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> UserResponse:
        """Dependency to get the current authenticated user from a token."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = decode_token(token)
            user_id: str = payload.get("sub")
            if user_id is None:
                print("[AUTH_STUB] Token validation failed: No user ID (sub) in payload")
                raise credentials_exception
            # token_data = TokenPayload(**payload) # Can add more validation here if needed
        except Exception as e: # Catches JWT errors or validation errors
            print(f"[AUTH_STUB] Token validation failed: {e}")
            raise credentials_exception
        
        user_service = UserService(db)
        user = await user_service.get_user_by_id(int(user_id)) # Assuming ID is stored as int in DB
        if user is None:
            print(f"[AUTH_STUB] Token validation failed: User ID {user_id} not found in DB")
            raise credentials_exception
        print(f"[AUTH_STUB] Current user identified: {user.email} (ID: {user.id})")
        return UserResponse.model_validate(user) # Convert to Pydantic response model

# Instance for dependency injection
auth_service = AuthService()
