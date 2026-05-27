from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.models.portfolio import Portfolio, PortfolioAsset
from app.services.coingecko import get_coin_price
from app.schemas.portfolio import AssetResponse, PortfolioResponse


async def get_or_create_portfolio(db: AsyncSession, user_id: int) -> Portfolio:
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == user_id)
    )
    portfolio = result.scalar_one_or_none()
    if not portfolio:
        portfolio = Portfolio(user_id=user_id)
        db.add(portfolio)
        await db.flush()
        await db.refresh(portfolio)
    return portfolio


async def get_portfolio(db: AsyncSession, user_id: int) -> PortfolioResponse:
    portfolio = await get_or_create_portfolio(db, user_id)

    result = await db.execute(
        select(PortfolioAsset).where(PortfolioAsset.portfolio_id == portfolio.id)
    )
    assets = result.scalars().all()

    if not assets:
        return PortfolioResponse(assets=[], total_value=0)

    coin_ids = [a.coin_id for a in assets]
    try:
        prices_data = await get_coin_price(coin_ids)
    except Exception:
        prices_data = {}

    asset_list = []
    total_value = 0.0

    for asset in assets:
        coin_data = prices_data.get(asset.coin_id, {})
        current_price = coin_data.get("usd")
        change_24h = coin_data.get("usd_24h_change")
        amount = float(asset.amount)
        total = current_price * amount if current_price else None

        if total:
            total_value += total

        asset_list.append(AssetResponse(
            id=asset.id,
            coin_id=asset.coin_id,
            coin_symbol=asset.coin_symbol,
            coin_name=asset.coin_name,
            amount=amount,
            current_price=current_price,
            total_value=total,
            change_24h=change_24h,
        ))

    return PortfolioResponse(assets=asset_list, total_value=total_value)


async def add_or_update_asset(
    db: AsyncSession,
    portfolio_id: int,
    coin_id: str,
    coin_symbol: str,
    coin_name: str,
    amount: float,
) -> PortfolioAsset:
    result = await db.execute(
        select(PortfolioAsset).where(
            PortfolioAsset.portfolio_id == portfolio_id,
            PortfolioAsset.coin_id == coin_id,
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        existing.amount = Decimal(str(amount))
        await db.flush()
        await db.refresh(existing)
        return existing

    asset = PortfolioAsset(
        portfolio_id=portfolio_id,
        coin_id=coin_id,
        coin_symbol=coin_symbol,
        coin_name=coin_name,
        amount=Decimal(str(amount)),
    )
    db.add(asset)
    await db.flush()
    await db.refresh(asset)
    return asset


async def delete_asset(
    db: AsyncSession,
    portfolio_id: int,
    coin_id: str,
) -> bool:
    result = await db.execute(
        delete(PortfolioAsset).where(
            PortfolioAsset.portfolio_id == portfolio_id,
            PortfolioAsset.coin_id == coin_id,
        )
    )
    return result.rowcount > 0