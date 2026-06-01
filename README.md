# CryptoHub — Агрегатор криптовалют

Веб-приложение для мониторинга криптовалютного рынка в режиме реального времени.
Агрегирует данные о курсах монет, отображает графики, показывает актуальные данные
и позволяет настраивать персональные уведомления по цене.

## Функциональность

- **Котировки в реальном времени** — топ монет по капитализации с актуальными ценами
- **Страница монеты** — детальная информация, график цены за 1д/7д/30д/3м
- **Поиск** — поиск монеты по названию или тикеру
- **Избранное** — персональный список отслеживаемых монет
- **Уведомления** — алерт когда монета достигает заданной цены
- **Портфель** — учёт активов с подсчётом общей стоимости в реальном времени
- **Конвертер** — перевод между криптовалютами и фиатом (USD, EUR, RUB и др.)

## Стек технологий

| Слой | Технология |
|---|---|
| Backend | Python 3.12, FastAPI |
| База данных | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 (async) |
| Миграции | Alembic |
| Кэш / брокер | Redis 7 |
| Фоновые задачи | Celery + Celery Beat |
| Крипто API | CoinGecko API |
| Frontend | React 18, Vite |
| HTTP клиент | Axios |
| Состояние | Zustand, React Query |
| Графики | Recharts |
| Контейнеризация | Docker, Docker Compose |

## Требования

- Docker Desktop
- Git

## Быстрый старт

### 1. Клонируй репозиторий

```bash
git clone https://github.com/Sakyrakito/cryptohub.git
cd cryptohub
```

### 2. Создай файл окружения

```bash
cp backend/.env.example backend/.env
```

Открой `backend/.env` и заполни:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@postgres:5432/cryptohub
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key-here
COINGECKO_API_KEY=your-api-key  # получить на coingecko.com/api
```

### 3. Запусти проект

```bash
docker-compose up --build
```

### 4. Открой в браузере

| Сервис | Адрес |
|---|---|
| Фронтенд | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |

## Структура проекта

```
cryptohub/
├── backend/
│   ├── app/
│   │   ├── api/v1/        # роуты
│   │   ├── core/          # конфиг, БД, безопасность
│   │   ├── models/        # SQLAlchemy модели
│   │   ├── schemas/       # Pydantic схемы
│   │   ├── services/      # бизнес-логика
│   │   ├── tasks/         # Celery задачи
│   │   └── main.py
│   ├── migrations/        # Alembic миграции
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/           # axios + запросы
│   │   ├── components/    # UI компоненты
│   │   ├── pages/         # страницы
│   │   └── store/         # Zustand
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

## API эндпоинты

### Авторизация
| Метод | Эндпоинт | Описание |
|---|---|---|
| POST | /api/v1/auth/register | Регистрация |
| POST | /api/v1/auth/login | Вход |
| GET | /api/v1/auth/me | Текущий пользователь |

### Монеты
| Метод | Эндпоинт | Описание |
|---|---|---|
| GET | /api/v1/coins/top | Топ монет |
| GET | /api/v1/coins/search?q= | Поиск |
| GET | /api/v1/coins/{id} | Детали монеты |
| GET | /api/v1/coins/{id}/chart | График цены |

### Избранное
| Метод | Эндпоинт | Описание |
|---|---|---|
| GET | /api/v1/favorites | Список избранных |
| POST | /api/v1/favorites | Добавить |
| DELETE | /api/v1/favorites/{id} | Удалить |

### Уведомления
| Метод | Эндпоинт | Описание |
|---|---|---|
| GET | /api/v1/alerts | Список алертов |
| POST | /api/v1/alerts | Создать алерт |
| DELETE | /api/v1/alerts/{id} | Удалить |
| GET | /api/v1/alerts/history | История срабатываний |

### Портфель
| Метод | Эндпоинт | Описание |
|---|---|---|
| GET | /api/v1/portfolio | Портфель пользователя |
| POST | /api/v1/portfolio/assets | Добавить монету |
| DELETE | /api/v1/portfolio/assets/{id} | Удалить монету |

### Конвертер
| Метод | Эндпоинт | Описание |
|---|---|---|
| GET | /api/v1/converter/convert | Конвертировать |
| GET | /api/v1/converter/popular-coins | Популярные монеты |
| GET | /api/v1/converter/fiat-list | Список фиат валют |

## Архитектура

```
React Frontend (5173)
        ↓ HTTP
FastAPI Backend (8000)
    ↓           ↓
PostgreSQL    Redis
(данные)   (кэш + очередь)
                ↓
          Celery Worker
                ↓
          CoinGecko API
```

## Автор

Синкевич Владимир — [GitHub](https://github.com/Sakyrakito)