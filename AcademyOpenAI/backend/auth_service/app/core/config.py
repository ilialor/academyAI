from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # База данных
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "auth_db"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @property
    def get_database_url(self) -> str:
        if self.SQLALCHEMY_DATABASE_URI:
            return self.SQLALCHEMY_DATABASE_URI
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    # JWT
    SECRET_KEY: str = "your-secret-key"  # В продакшене заменить на безопасный ключ
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Настройки приложения
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Auth Service"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()