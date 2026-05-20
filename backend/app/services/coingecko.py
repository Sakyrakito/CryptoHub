import httpx
from app.core.config import settings
from app.core.cache import cache_get, cache_set


def _get_headers() -> dict:
    headers = {"accept": "application/json"}
    if settings.COINGECKO_API_KEY:
        headers["x-cg-demo-api-key"] = settings.COINGECKO_API_KEY
    return headers


async def _get(url: str, params: dict = None) -> dict | list:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            url,
            params=params,
            headers=_get_headers(),
        )
        response.raise_for_status()
        return response.json()


async def get_top_coins(page: int = 1, per_page: int = 50) -> list:
    cache_key = f"top_coins:{page}:{per_page}"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    data = await _get(
        f"{settings.COINGECKO_BASE_URL}/coins/markets",
        params={
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page,
            "sparkline": False,
            "price_change_percentage": "24h,7d",
        },
    )
    await cache_set(cache_key, data)
    return data


async def get_coin_detail(coin_id: str) -> dict:
    cache_key = f"coin_detail:{coin_id}"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    data = await _get(
        f"{settings.COINGECKO_BASE_URL}/coins/{coin_id}",
        params={
            "localization": False,
            "tickers": False,
            "market_data": True,
            "community_data": False,
            "developer_data": False,
        },
    )
    await cache_set(cache_key, data, ttl=120)
    return data


async def get_coin_chart(coin_id: str, days: int = 7) -> dict:
    cache_key = f"coin_chart:{coin_id}:{days}"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    data = await _get(
        f"{settings.COINGECKO_BASE_URL}/coins/{coin_id}/market_chart",
        params={
            "vs_currency": "usd",
            "days": days,
        },
    )
    await cache_set(cache_key, data, ttl=300)
    return data


async def search_coins(query: str) -> list:
    cache_key = f"search:{query.lower()}"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    data = await _get(
        f"{settings.COINGECKO_BASE_URL}/search",
        params={"query": query},
    )
    coins = data.get("coins", [])[:20]
    await cache_set(cache_key, coins, ttl=300)
    return coins


async def get_coin_price(coin_ids: list[str]) -> dict:
    ids = ",".join(coin_ids)
    cache_key = f"prices:{ids}"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    data = await _get(
        f"{settings.COINGECKO_BASE_URL}/simple/price",
        params={
            "ids": ids,
            "vs_currencies": "usd",
            "include_24hr_change": True,
        },
    )
    await cache_set(cache_key, data, ttl=30)
    return data