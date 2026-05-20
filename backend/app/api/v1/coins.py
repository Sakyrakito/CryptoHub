from fastapi import APIRouter, HTTPException, Query, status
import httpx

from app.services.coingecko import (
    get_top_coins,
    get_coin_detail,
    get_coin_chart,
    search_coins,
)

router = APIRouter(prefix="/coins", tags=["coins"])


@router.get("/top")
async def top_coins(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=250),
):
    try:
        return await get_top_coins(page=page, per_page=per_page)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Ошибка CoinGecko API: {e}")


@router.get("/search")
async def search(q: str = Query(..., min_length=1)):
    try:
        return await search_coins(q)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Ошибка CoinGecko API: {e}")


@router.get("/{coin_id}")
async def coin_detail(coin_id: str):
    try:
        return await get_coin_detail(coin_id)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Монета не найдена")
        raise HTTPException(status_code=502, detail=f"Ошибка CoinGecko API: {e}")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Ошибка CoinGecko API: {e}")


@router.get("/{coin_id}/chart")
async def coin_chart(
    coin_id: str,
    days: int = Query(7, ge=1, le=365),
):
    try:
        return await get_coin_chart(coin_id, days=days)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Монета не найдена")
        raise HTTPException(status_code=502, detail=f"Ошибка CoinGecko API: {e}")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Ошибка CoinGecko API: {e}")