"""Configuration settings for the pipeline worker service."""

import os
from typing import Optional, Dict, Any, List
from pydantic import BaseSettings, Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuration settings for the pipeline worker service."""
    
    APP_NAME: str = "Pipeline Worker"
    DEBUG: bool = False

    # Celery/Message Broker settings
    CELERY_BROKER_URL: str = "redis://localhost:6379/0" # Example using Redis
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    # External Service API Keys (load from env)
    GOOGLE_API_KEY: str = "YOUR_GOOGLE_API_KEY"
    # ASSEMBLYAI_API_KEY: str = "YOUR_ASSEMBLYAI_KEY"
    # DEEPL_API_KEY: str = "YOUR_DEEPL_KEY"

    # Course Service API URL (to update status/results)
    COURSES_SERVICE_URL: str = "http://courses-service/api/v1" # Internal service name

    # MongoDB connection for courses data
    MONGODB_URL: str = "mongodb://localhost:27017/"
    MONGODB_DB_NAME: str = "academy_courses"

    # API Keys
    GOOGLE_AI_API_KEY: Optional[str] = Field(None, env="GOOGLE_AI_API_KEY")
    
    # Service URLs
    AUTH_SERVICE_URL: str = Field("http://auth-service:8000", env="AUTH_SERVICE_URL")
    
    # Message Queue Settings
    RABBITMQ_HOST: str = Field("rabbitmq", env="RABBITMQ_HOST")
    RABBITMQ_PORT: int = Field(5672, env="RABBITMQ_PORT")
    RABBITMQ_USER: str = Field("guest", env="RABBITMQ_USER")
    RABBITMQ_PASSWORD: str = Field("guest", env="RABBITMQ_PASSWORD")
    RABBITMQ_VHOST: str = Field("/", env="RABBITMQ_VHOST")
    
    # Queue Names
    VIDEO_PROCESSING_QUEUE: str = Field("video_processing", env="VIDEO_PROCESSING_QUEUE")
    TEXT_PROCESSING_QUEUE: str = Field("text_processing", env="TEXT_PROCESSING_QUEUE")
    
    # Processing Settings
    DEFAULT_TARGET_LANGUAGE: str = Field("ru", env="DEFAULT_TARGET_LANGUAGE")
    MAX_VIDEO_SIZE_MB: int = Field(500, env="MAX_VIDEO_SIZE_MB")
    
    # Storage Settings
    STORAGE_TYPE: str = Field("local", env="STORAGE_TYPE")  # 'local', 's3', etc.
    LOCAL_STORAGE_PATH: str = Field("/app/data", env="LOCAL_STORAGE_PATH")
    S3_BUCKET_NAME: Optional[str] = Field(None, env="S3_BUCKET_NAME")
    S3_REGION: Optional[str] = Field(None, env="S3_REGION")
    
    # LLM Settings
    LLM_MODEL: str = Field("gemini-2.5-pro", env="LLM_MODEL")
    LLM_TEMPERATURE: float = Field(0.2, env="LLM_TEMPERATURE")
    LLM_MAX_OUTPUT_TOKENS: int = Field(8192, env="LLM_MAX_OUTPUT_TOKENS")
    
    # Logging Settings
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

# Create global settings instance
settings = Settings()