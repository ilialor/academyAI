@echo off
REM Скрипт для запуска сервисов AcademyOpenAI локально через Docker Compose в Windows

REM Переход в директорию с docker-compose.yml
cd /d "%~dp0\..\infra\docker" || exit /b

REM Проверка наличия .env файла
if not exist .env (
    echo Файл .env не найден. Создаю из примера...
    copy .env.example .env
    echo Создан файл .env из примера. Пожалуйста, отредактируйте его с вашими настройками.
    exit /b 1
)

REM Обработка аргументов командной строки
if "%1"=="--all" goto all
if "%1"=="-a" goto all
if "%1"=="--auth" goto auth
if "%1"=="-u" goto auth
if "%1"=="--courses" goto courses
if "%1"=="-c" goto courses
if "%1"=="--worker" goto worker
if "%1"=="-w" goto worker
if "%1"=="--down" goto down
if "%1"=="-d" goto down
if "%1"=="--help" goto help
if "%1"=="-h" goto help
goto help

:all
echo Запуск всех сервисов...
docker-compose --profile all up -d
goto end

:auth
echo Запуск сервиса аутентификации...
docker-compose --profile auth up -d
goto end

:courses
echo Запуск сервиса курсов...
docker-compose --profile courses up -d
goto end

:worker
echo Запуск pipeline worker...
docker-compose --profile worker up -d
goto end

:down
echo Остановка всех контейнеров...
docker-compose down
goto end

:help
echo Использование: %0 [опции]
echo.
echo Опции:
echo   -a, --all       Запустить все сервисы
echo   -u, --auth      Запустить только сервис аутентификации и его зависимости
echo   -c, --courses   Запустить только сервис курсов и его зависимости
echo   -w, --worker    Запустить только pipeline worker и его зависимости
echo   -d, --down      Остановить все контейнеры
echo   -h, --help      Показать эту справку
echo.
echo Примеры:
echo   %0 --all        # Запустить все сервисы
echo   %0 --auth       # Запустить только сервис аутентификации
echo   %0 --down       # Остановить все контейнеры
goto end

:end
echo Готово!