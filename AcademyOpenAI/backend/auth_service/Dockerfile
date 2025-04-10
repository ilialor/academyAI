FROM python:3.12-slim

WORKDIR /app

# Установка зависимостей для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install --no-cache-dir poetry==1.7.1

# Копирование только файлов зависимостей для кэширования слоев
COPY pyproject.toml ./

# Настройка Poetry для создания виртуального окружения в контейнере
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --only main

# Копирование остальных файлов проекта
COPY . .

# Установка проекта
RUN poetry install --no-interaction --no-ansi --only main

# Порт для FastAPI
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]