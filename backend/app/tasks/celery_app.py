from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "cryptohub",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.price_checker"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
    # расписание задач
    beat_schedule={
        "check-prices-every-minute": {
            "task": "app.tasks.price_checker.check_prices",
            "schedule": 60.0,  # каждые 60 секунд
        },
    },
)