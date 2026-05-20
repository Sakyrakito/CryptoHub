from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.models.favorite import Favorite


async def get_favorites(db: AsyncSession, user_id: int) -> list[Favorite]:
    result = await db.execute(
        select(Favorite)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.added_at.desc())
    )
    return result.scalars().all()


async def add_favorite(
    db: AsyncSession,
    user_id: int,
    coin_id: str,
    coin_symbol: str,
    coin_name: str,
) -> Favorite:
    favorite = Favorite(
        user_id=user_id,
        coin_id=coin_id,
        coin_symbol=coin_symbol,
        coin_name=coin_name,
    )
    db.add(favorite)
    await db.flush()
    await db.refresh(favorite)
    return favorite


async def remove_favorite(db: AsyncSession, user_id: int, coin_id: str) -> bool:
    result = await db.execute(
        delete(Favorite)
        .where(Favorite.user_id == user_id, Favorite.coin_id == coin_id)
    )
    return result.rowcount > 0


async def is_favorite(db: AsyncSession, user_id: int, coin_id: str) -> bool:
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.coin_id == coin_id,
        )
    )
    return result.scalar_one_or_none() is not None