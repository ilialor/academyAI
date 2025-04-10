from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    # База данных - используем имена сервисов из Docker Compose
    POSTGRES_SERVER: str = os.getenv("POSTGRES_HOST", "postgres")  # Используем postgres вместо localhost
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "auth_db")
    SQLALCHEMY_DATABASE_URI: Optional[str] = os.getenv("DATABASE_URL")  # Поддержка переменной окружения из docker-compose

    @property
    def get_database_url(self) -> str:
        if self.SQLALCHEMY_DATABASE_URI:
            # Если есть DATABASE_URL, преобразуем его для использования asyncpg
            if self.SQLALCHEMY_DATABASE_URI.startswith('postgresql://'):
                return self.SQLALCHEMY_DATABASE_URI.replace('postgresql://', 'postgresql+asyncpg://', 1)
            return self.SQLALCHEMY_DATABASE_URI
        # Используем протокол postgresql+asyncpg для асинхронного драйвера
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    # JWT
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")  # В продакшене заменить на безопасный ключ
    ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Настройки приложения
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Auth Service"
    APP_NAME: str = "Auth Service"  # Добавляем APP_NAME как синоним для PROJECT_NAME
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"  # Добавляем атрибут DEBUG для логирования
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]  # В продакшене заменить на конкретные домены
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()