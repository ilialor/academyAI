from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str = Field(..., description="JWT Access Token")
    refresh_token: str = Field(..., description="JWT Refresh Token")
    token_type: str = Field("bearer", description="Token type")

class TokenPayload(BaseModel):
    sub: str # Subject (usually user email or ID)
    # Add other claims like exp (expiration time) if needed for validation
    # exp: int | None = None
