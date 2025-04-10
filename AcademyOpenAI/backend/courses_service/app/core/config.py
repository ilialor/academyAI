from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Basic application settings
    APP_NAME: str = "Courses Service"
    DEBUG: bool = False

    # Database settings (placeholders for now)
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db" # Example for SQLite

    # Add other configurations like secrets, API keys, etc.
    # EXAMPLE_API_KEY: str = "your_api_key_here"

    class Config:
        # If using a .env file, specify its name
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Create a single instance of the settings to be used throughout the application
settings = Settings()
