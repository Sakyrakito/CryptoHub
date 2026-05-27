from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.portfolio import AssetAdd, AssetResponse, PortfolioResponse
from app.services.portfolio import (
    get_or_create_portfolio,
    get_portfolio,
    add_or_update_asset,
    delete_asset,
)

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("", response_model=PortfolioResponse)
async def get_my_portfolio(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_portfolio(db, current_user.id)


@router.post("/assets", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def add_asset(
    data: AssetAdd,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    portfolio = await get_or_create_portfolio(db, current_user.id)
    asset = await add_or_update_asset(
        db,
        portfolio_id=portfolio.id,
        coin_id=data.coin_id,
        coin_symbol=data.coin_symbol,
        coin_name=data.coin_name,
        amount=data.amount,
    )
    return AssetResponse(
        id=asset.id,
        coin_id=asset.coin_id,
        coin_symbol=asset.coin_symbol,
        coin_name=asset.coin_name,
        amount=float(asset.amount),
    )


@router.delete("/assets/{coin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_asset(
    coin_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    portfolio = await get_or_create_portfolio(db, current_user.id)
    removed = await delete_asset(db, portfolio.id, coin_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Монета не найдена в портфеле")