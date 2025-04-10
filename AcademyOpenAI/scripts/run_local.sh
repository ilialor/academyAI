#!/bin/bash

# Скрипт для запуска сервисов AcademyOpenAI локально через Docker Compose

# Переход в директорию с docker-compose.yml
cd "$(dirname "$0")/../infra/docker" || exit

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "Файл .env не найден. Создаю из примера..."
    cp .env.example .env
    echo "Создан файл .env из примера. Пожалуйста, отредактируйте его с вашими настройками."
    exit 1
fi

# Функция для вывода справки
show_help() {
    echo "Использование: $0 [опции]"
    echo ""
    echo "Опции:"
    echo "  -a, --all       Запустить все сервисы"
    echo "  -u, --auth      Запустить только сервис аутентификации и его зависимости"
    echo "  -c, --courses   Запустить только сервис курсов и его зависимости"
    echo "  -w, --worker    Запустить только pipeline worker и его зависимости"
    echo "  -d, --down      Остановить все контейнеры"
    echo "  -h, --help      Показать эту справку"
    echo ""
    echo "Примеры:"
    echo "  $0 --all        # Запустить все сервисы"
    echo "  $0 --auth       # Запустить только сервис аутентификации"
    echo "  $0 --down       # Остановить все контейнеры"
}

# Обработка аргументов командной строки
case "$1" in
    -a|--all)
        echo "Запуск всех сервисов..."
        docker-compose --profile all up -d
        ;;
    -u|--auth)
        echo "Запуск сервиса аутентификации..."
        docker-compose --profile auth up -d
        ;;
    -c|--courses)
        echo "Запуск сервиса курсов..."
        docker-compose --profile courses up -d
        ;;
    -w|--worker)
        echo "Запуск pipeline worker..."
        docker-compose --profile worker up -d
        ;;
    -d|--down)
        echo "Остановка всех контейнеров..."
        docker-compose down
        ;;
    -h|--help)
        show_help
        ;;
    *)
        echo "Неизвестная опция: $1"
        show_help
        exit 1
        ;;
esac

echo "Готово!"