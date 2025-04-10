from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create async engine
async_engine = create_async_engine(
    settings.get_database_url,
    echo=settings.DEBUG if hasattr(settings, 'DEBUG') else False, # Log SQL queries if DEBUG exists and is True
    future=True
)

# Create async session maker
AsyncSessionFactory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncSession:
    """Dependency to get DB session."""
    async with AsyncSessionFactory() as session:
        try:
            yield session
            # No commit here, commit should be handled in the service layer
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
