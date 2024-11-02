#!/bin/bash


# Запускаем FastAPI сервер
echo "Запускаем FastAPI сервер..."
gunicorn server.src.app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 &

# Запускаем Telegram бота
echo "Запускаем Telegram бота..."
python -u bot/src/main.py


wait
