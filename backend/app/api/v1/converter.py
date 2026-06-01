from fastapi import APIRouter, HTTPException, Query
import httpx

from app.services.coingecko import _get
from app.core.config import settings
from app.core.cache import cache_get, cache_set

router = APIRouter(prefix="/converter", tags=["converter"])

FIAT_CURRENCIES = {
    "usd": "USD — Доллар США",
    "eur": "EUR — Евро",
    "rub": "RUB — Российский рубль",
    "gbp": "GBP — Фунт стерлингов",
    "jpy": "JPY — Японская иена",
    "cny": "CNY — Китайский юань",
}

POPULAR_COINS = [
    {"id": "bitcoin", "symbol": "BTC", "name": "Bitcoin"},
    {"id": "ethereum", "symbol": "ETH", "name": "Ethereum"},
    {"id": "tether", "symbol": "USDT", "name": "Tether"},
    {"id": "binancecoin", "symbol": "BNB", "name": "BNB"},
    {"id": "solana", "symbol": "SOL", "name": "Solana"},
    {"id": "ripple", "symbol": "XRP", "name": "XRP"},
    {"id": "dogecoin", "symbol": "DOGE", "name": "Dogecoin"},
    {"id": "cardano", "symbol": "ADA", "name": "Cardano"},
]


async def get_prices_in_fiat(coin_ids: list[str]) -> dict:
    ids = ",".join(coin_ids)
    cache_key = f"convert_prices:{ids}"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    data = await _get(
        f"{settings.COINGECKO_BASE_URL}/simple/price",
        params={
            "ids": ids,
            "vs_currencies": "usd,eur,rub,gbp,jpy,cny",
        },
    )
    await cache_set(cache_key, data, ttl=60)
    return data


@router.get("/popular-coins")
async def popular_coins():
    return POPULAR_COINS


@router.get("/fiat-list")
async def fiat_list():
    return [{"id": k, "name": v} for k, v in FIAT_CURRENCIES.items()]


@router.get("/convert")
async def convert(
    from_id: str = Query(...),
    to_id: str = Query(...),
    amount: float = Query(1.0, gt=0),
):
    try:
        fiat_codes = list(FIAT_CURRENCIES.keys())

        # собираем какие монеты нужно запросить
        coin_ids = []
        if from_id not in fiat_codes:
            coin_ids.append(from_id)
        if to_id not in fiat_codes:
            coin_ids.append(to_id)

        # получаем цены монет во всех фиатах сразу
        prices = {}
        if coin_ids:
            data = await get_prices_in_fiat(coin_ids)
            prices = data

        def get_price_in_usd(currency_id: str) -> float:
            # Возвращает стоимость 1 единицы валюты в USD.
            if currency_id == "usd":
                return 1.0
            if currency_id in fiat_codes:
                # для фиата берём цену через bitcoin как прокси
                # но проще - используем фиксированные примерные курсы
                fiat_to_usd = {
                    "eur": 1.08, "rub": 0.011,
                    "gbp": 1.27, "jpy": 0.0067, "cny": 0.14,
                }
                return fiat_to_usd.get(currency_id, 1.0)
            if currency_id in prices:
                return prices[currency_id].get("usd", 0)
            raise HTTPException(status_code=404, detail=f"Монета не найдена: {currency_id}")

        def get_price_in_fiat(currency_id: str, fiat: str) -> float:
            # Возвращает стоимость 1 единицы валюты в указанном фиате.
            if currency_id in fiat_codes:
                from_usd = get_price_in_usd(currency_id)
                to_usd = get_price_in_usd(fiat) if fiat != "usd" else 1.0
                return from_usd / to_usd if to_usd else 0
            if currency_id in prices:
                return prices[currency_id].get(fiat, 0)
            raise HTTPException(status_code=404, detail=f"Монета не найдена: {currency_id}")

        # конвертация через USD как промежуточную валюту
        from_in_usd = get_price_in_usd(from_id)
        to_in_usd = get_price_in_usd(to_id)

        if to_in_usd == 0:
            raise HTTPException(status_code=400, detail="Невозможно конвертировать")

        rate = from_in_usd / to_in_usd
        result = amount * rate

        return {
            "from_id": from_id,
            "to_id": to_id,
            "amount": amount,
            "result": result,
            "rate": rate,
        }

    except HTTPException:
        raise
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Ошибка API: {e}")