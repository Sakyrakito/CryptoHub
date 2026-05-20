# backend/app/schemas/coin.py
from pydantic import BaseModel
from typing import Any


class CoinMarket(BaseModel):
    id: str
    symbol: str
    name: str
    image: str
    current_price: float | None
    market_cap: float | None
    market_cap_rank: int | None
    price_change_percentage_24h: float | None
    price_change_percentage_7d_in_currency: float | None
    total_volume: float | None

    model_config = {"from_attributes": True}


class CoinDetail(BaseModel):
    id: str
    symbol: str
    name: str
    description: dict
    image: dict
    market_cap_rank: int | None
    market_data: dict
    links: dict

    model_config = {"from_attributes": True}


class CoinChart(BaseModel):
    prices: list[list[float]]
    market_caps: list[list[float]]
    total_volumes: list[list[float]]


class CoinSearchResult(BaseModel):
    id: str
    symbol: str
    name: str
    thumb: str
    market_cap_rank: int | None