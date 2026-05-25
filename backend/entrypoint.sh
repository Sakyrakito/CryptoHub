#!/bin/bash
echo "Применяем миграции..."
alembic upgrade head
echo "Запускаем сервер..."
uvicorn app.main:app --host 0.0.0.0 --port 8000