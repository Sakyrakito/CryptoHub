import json
from typing import Any
import redis.asyncio as aioredis
from app.core.config import settings

_redis: aioredis.Redis | None = None

async def get_redis() -> aioredis.Redis:
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis


async def cache_get(key: str) -> Any | None:
    r = await get_redis()
    value = await r.get(key)
    if value:
        return json.loads(value)
    return None


async def cache_set(key: str, value: Any, ttl: int = settings.CACHE_TTL_SECONDS) -> None:
    r = await get_redis()
    await r.set(key, json.dumps(value), ex=ttl)