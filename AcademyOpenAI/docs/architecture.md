# Архитектура AcademyOpenAI

## Обзор архитектуры

AcademyOpenAI построен на современной микросервисной архитектуре, обеспечивающей масштабируемость, отказоустойчивость и гибкость. Система использует контейнеризацию для упрощения развертывания и управления компонентами.

## Системная архитектура (C4 модель)

### Уровень 1: Контекстная диаграмма системы

Основные участники и внешние системы:

- **Пользователи:** Студенты, Преподаватели, Администраторы
- **AcademyOpenAI Platform:** Основная система
- **Внешние сервисы:** Email Service, External STT API, External Translation API, External LLM API (Google AI)

### Уровень 2: Контейнерная диаграмма

```
+--------------------------------------------------------------------------------------------------+
|                                    AcademyOpenAI Platform                                        |
|                                                                                                  |
|  +----------------+    +----------------+    +----------------+    +----------------+            |
|  |                |    |                |    |                |    |                |            |
|  |  Frontend Web  |    | Frontend Mobile|    |  API Gateway   |    |  Auth Service  |            |
|  |    (React)     |    | (React Native) |    |     (Kong)     |    |   (FastAPI)    |            |
|  |                |    |                |    |                |    |                |            |
|  +-------+--------+    +-------+--------+    +-------+--------+    +-------+--------+            |
|          |                     |                     |                     |                     |
|          |                     |                     |                     |                     |
|          |                     |                     |                     |                     |
|  +-------v--------+    +------v---------+    +-----v----------+    +-----v----------+            |
|  |                |    |                |    |                |    |                |            |
|  | Courses Service|    | Pipeline Worker|    |   PostgreSQL   |    |    MongoDB     |            |
|  |   (FastAPI)    |    |  (Celery/FS)   |    |   Database     |    |   Database     |            |
|  |                |    |                |    |                |    |                |            |
|  +----------------+    +----------------+    +----------------+    +----------------+            |
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
```

### Уровень 3: Компонентная диаграмма

#### Auth Service Components
- API Endpoints (Router)
- Authentication Logic
- User Profile Logic
- Database Interface (SQLAlchemy Core/ORM + asyncpg)
- JWT Utilities

#### Courses Service Components
- API Endpoints (Router)
- Course Management Logic
- Pipeline Trigger Logic
- Database Interface (Motor)
- File Handling Logic

#### Pipeline Worker Components
- Task Consumer
- State Manager
- Video Processor (FFmpeg Interface)
- STT Client
- Translation Client
- Course Generation Client (LLM Interface)
- Result Handler (Updates MongoDB)

## Технологический стек

| Категория | Выбор | Обоснование |
|-----------|-------|-------------|
| **Frontend (Web)** | React (Vite) + TypeScript + TanStack Query | Зрелая экосистема, компонентный UI, производительность (Vite), типобезопасность (TS), эффективная выборка/кэширование данных (TanStack Query) |
| **Frontend (Mobile)** | React Native + TypeScript + TanStack Query | Повторное использование кода с веб-версией (логика, состояние), доступ к нативной производительности, сильное сообщество |
| **Backend Framework** | FastAPI (Python) | Высокая производительность (asyncio, Starlette, Pydantic), автоматическая документация (OpenAPI), встроенная валидация данных, внедрение зависимостей |
| **Package Mgmt** | UV / Poetry | Современное, быстрое, надежное управление зависимостями и упаковка для Python |
| **Linting/Format** | Ruff | Чрезвычайно быстрый линтер и форматтер для Python на основе Rust, единый инструмент, заменяющий Flake8, isort, Black и т.д. |
| **API Gateway** | Kong | Зрелый, богатый функциями, экосистема плагинов, обрабатывает маршрутизацию, безопасность, ограничение скорости, наблюдаемость |
| **Auth Database** | PostgreSQL (asyncpg) | Надежная, ACID-совместимая, зрелая реляционная база данных. asyncpg для высокопроизводительного асинхронного взаимодействия с Python |
| **Course Database** | MongoDB (Motor) | Гибкая схема, идеальная для развивающихся структур курсов и вложенных интерактивных элементов. Motor для асинхронного взаимодействия с Python |
| **Task Queue** | RabbitMQ (aio-pika) / Redis Streams | Разделяет длительные задачи конвейера, улучшает отзывчивость. RabbitMQ для надежности, Redis для простоты/скорости |
| **Video Processing** | FFmpeg | Стандарт де-факто для манипуляций с аудио/видео. Надежное извлечение аудио |
| **STT Service** | Whisper Large v3 / AssemblyAI / Google Speech-to-Text | Современная точность (Whisper), корпоративные функции (AssemblyAI), интеграция GCP (Google) |
| **Translation** | Google Translate API / DeepL API | Высококачественные API машинного перевода |
| **Course Gen LLM** | Gemini 2.5 Pro / GPT-4 / Claude 3 | Современная мультимодальная модель, большой контекст, потенциал для прямого структурированного вывода |
| **Containerization** | Docker | Стандарт для упаковки приложений и зависимостей |
| **Orchestration** | Kubernetes (K8s) | Отраслевой стандарт для развертывания, масштабирования и управления контейнеризированными приложениями |
| **CI/CD** | GitHub Actions / GitLab CI | Интегрировано с контролем исходного кода, автоматизированные рабочие процессы для тестирования и развертывания |
| **Monitoring** | Prometheus + Grafana + OpenTelemetry | Современный стек для сбора метрик, визуализации и распределенной трассировки |

## Основные процессы обработки

### Конвейер Video-to-Interactive Course

**Триггер:** `POST /courses/{course_id}/upload_video` запрос к Courses Service.

1. **Загрузка и начальная обработка (Courses Service):**
   - Получение видеофайла через multipart/form-data
   - Валидация типа и размера файла
   - Временное сохранение файла
   - Обновление статуса курса в MongoDB на `PROCESSING_VIDEO`
   - Публикация задачи в Message Broker

#### Вариант A: Прямая генерация (Gemini 2.5 Pro)

2. **Потребление задачи:** Worker получает `process_video_task`
3. **Вызов Gemini API:**
   - Чтение видеофайла из хранилища
   - Создание запроса для Gemini 2.5 Pro API (мультимодальный ввод)
   - Отправка запроса в Google AI API
4. **Обработка ответа:**
   - Получение JSON-ответа от Gemini
   - Валидация структуры полученного JSON
5. **Обновление курса:**
   - Обновление соответствующего документа Course в MongoDB структурированным контентом
   - Изменение статуса курса на `PROCESSED` или `NEEDS_REVIEW`
6. **Очистка:** Удаление временного видеофайла

#### Вариант B: Многоэтапная обработка

2. **Потребление задачи:** Worker получает `process_video_task`
3. **Извлечение аудио (FFmpeg):**
   - Выполнение команды FFmpeg для извлечения аудио из видео
4. **Speech-to-Text (STT):**
   - Отправка аудиофайла в выбранный STT API
   - Получение английской транскрипции
5. **Перевод:**
   - Отправка английской транскрипции в Translation API
   - Получение русского перевода
6. **Генерация структуры курса и интерактивности (LLM):**
   - Создание запроса для текстовой LLM
   - Отправка запроса в LLM API
7. **Обработка ответа:**
   - Получение и валидация JSON-ответа
8. **Обновление курса:**
   - Обновление документа Course в MongoDB
   - Изменение статуса курса на `PROCESSED` или `NEEDS_REVIEW`
9. **Очистка:** Удаление временных видео и аудио файлов

### Конвейер Text-to-Interactive Course

**Триггер:** `POST /courses/{course_id}/upload_text` запрос к Courses Service.

1. **Загрузка и начальная обработка (Courses Service):**
   - Получение текстового контента
   - Валидация размера ввода
   - Обновление статуса курса в MongoDB на `PROCESSING_TEXT`
   - Публикация задачи в Message Broker

2. **Потребление задачи:** Worker получает `process_text_task`
3. **(Условно) Перевод:**
   - Если входной текст определен как английский, отправка в Translation API
   - Получение русского перевода
4. **Генерация структуры курса и интерактивности (LLM):**
   - Создание запроса для LLM
   - Отправка запроса в LLM API
5. **Обработка ответа:**
   - Получение и валидация JSON-ответа
6. **Обновление курса:**
   - Обновление документа Course в MongoDB
   - Изменение статуса курса на `PROCESSED` или `NEEDS_REVIEW`

## Дизайн API

### API Gateway (Kong) Configuration
- Определения upstream-сервисов (Auth, Courses)
- Определения маршрутов (например, `/auth/*` -> Auth Service, `/courses/*` -> Courses Service)
- Конфигурация плагинов (Rate Limiting, CORS, JWT validation)
- Конфигурация HTTPS-терминации

### Auth & Profile Service API
- Ключевые эндпоинты:
  - `POST /auth/register`
  - `POST /auth/login`
  - `GET /users/me`
  - `PUT /users/me`
  - `GET /admin/users`

### Courses Service API
- Ключевые эндпоинты:
  - `POST /courses`
  - `GET /courses`
  - `GET /courses/{course_id}`
  - `PUT /courses/{course_id}`
  - `DELETE /courses/{course_id}`
  - `POST /courses/{course_id}/upload_video`
  - `POST /courses/{course_id}/upload_text`
  - `POST /courses/{course_id}/publish`
  - `GET /courses/{course_id}/status`

## Дизайн базы данных

### Реляционная база данных (PostgreSQL - Auth & Profile)
- Таблица `users`: `id`, `email`, `hashed_password`, `role`, `created_at`, `updated_at`
- Таблица `profiles`: `user_id`, `full_name`, `avatar_url`, и другие поля

### Документная база данных (MongoDB - Courses & Content)
- Коллекция `courses`:
  - Метаданные курса: `_id`, `title`, `description`, `creator_id`, `status`
  - Модули курса с интерактивными элементами
  - Временные метки: `created_at`, `updated_at`, `published_at`
- Коллекция `student_progress`:
  - Отслеживание прогресса студентов по курсам

## Архитектура развертывания

### Контейнеризация (Docker, Docker Compose)
- `Dockerfile` для каждого сервиса
- `docker-compose.yml` для локальной разработки и тестирования

### Оркестрация (Kubernetes)
- K8s манифесты: `Deployment`, `Service`, `Ingress`, `ConfigMap`/`Secret`, `PersistentVolumeClaim`
- Helm charts для управления развертыванием

### Стратегия окружений (Dev, Staging, Prod)
- Раздельные окружения (разные K8s namespaces или кластеры)
- Управление конфигурацией для настройки развертываний по окружениям

## CI/CD Pipeline

### Контроль исходного кода (Git - GitHub/GitLab)
- Стратегия ветвления (Gitflow, GitHub Flow)

### CI Server (GitHub Actions / GitLab CI)
- Определение рабочих процессов в `.github/workflows` или `.gitlab-ci.yml`

### Этапы Pipeline
1. **Триггер:** Push в ветку `main`/`develop` или Pull Request
2. **Lint & Format:** Запуск `ruff check .` и `ruff format --check .`
3. **Type Check:** Запуск `mypy .` или `pyright .`
4. **Test:** Запуск `pytest`
5. **Build:** Сборка Docker-образа
6. **Push:** Отправка Docker-образа в реестр контейнеров
7. **Deploy (Staging):** Автоматическое развертывание в staging-окружение
8. **Deploy (Production):** Ручной триггер или автоматическое развертывание после валидации staging

## Безопасность

- **Аутентификация:** Безопасная реализация JWT, надежное хеширование паролей
- **Авторизация:** Строгое применение RBAC на уровне API Gateway и сервисов
- **Валидация ввода:** Использование Pydantic в FastAPI для строгой валидации запросов
- **Безопасность API:** HTTPS везде, ограничение скорости, потенциально WAF
- **Сканирование зависимостей:** Использование инструментов для поиска уязвимостей в зависимостях
- **Управление секретами:** Использование K8s Secrets или HashiCorp Vault
- **Безопасность контейнеров:** Сканирование образов контейнеров на уязвимости
- **Безопасность данных:** Шифрование конфиденциальных данных в состоянии покоя и при передаче