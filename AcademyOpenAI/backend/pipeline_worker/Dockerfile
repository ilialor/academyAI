FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей для сборки и обработки медиа
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    ffmpeg \
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

# Запуск воркера
CMD ["python", "-m", "app.main"]