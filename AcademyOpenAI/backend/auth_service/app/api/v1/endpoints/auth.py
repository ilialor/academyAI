from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import auth_service # Using the instance
from app.services.user_service import UserService

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    user_service = UserService(db)
    existing_user = await user_service.get_user_by_email(user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    # In a real app, add more validation (password complexity, etc.)
    new_user = await user_service.create_user(user_in)
    print(f"[ENDPOINT_STUB] User registered: {new_user.email}")
    return UserResponse.model_validate(new_user)

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return JWT tokens."""
    user = await auth_service.authenticate_user(
        email=form_data.username, # form data uses 'username' field for email
        password=form_data.password,
        db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Generate tokens
    tokens = auth_service.create_user_tokens(user_id=user.id)
    print(f"[ENDPOINT_STUB] User logged in: {user.email}")
    return tokens

# Add endpoints for token refresh if needed
# @router.post("/refresh", response_model=Token)
# async def refresh_access_token(...):
#     ...
