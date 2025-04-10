from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import api_v1_router
from app.core.config import settings
from app.db.session import async_engine as engine, AsyncSessionFactory as SessionLocal
from app.models.user import Base  # Импортируем Base из models.user

# Создание таблиц в базе данных
# Заменяем синхронное создание таблиц на асинхронную операцию
# которую нужно запускать в отдельной функции при старте приложения
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    version="0.1.0",
    # Add other FastAPI config like description, docs_url etc. if needed
    # docs_url="/api/docs",
    # redoc_url="/api/redoc",
    # openapi_url="/api/v1/openapi.json"
)

# Настройка CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Для асинхронного создания таблиц добавляем обработчик startup
@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # Раскомментировать для сброса БД
        await conn.run_sync(Base.metadata.create_all)
    print("База данных инициализирована")

# Подключение роутеров
app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)