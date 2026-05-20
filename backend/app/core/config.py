from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "changeme"
    DEBUG: bool = True
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    COINGECKO_API_KEY: str = ""
    COINGECKO_BASE_URL: str = "https://api.coingecko.com/api/v3"

    CACHE_TTL_SECONDS: int = 60  # кэш на 60 секунд

    class Config:
        env_file = ".env"


settings = Settings()