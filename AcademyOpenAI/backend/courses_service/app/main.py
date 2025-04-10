from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import courses
from app.core.config import settings

app = FastAPI(
    title="Courses Service",
    description="API для управления курсами",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(
    courses.router,
    prefix="/api/v1/courses",
    tags=["courses"]
)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)