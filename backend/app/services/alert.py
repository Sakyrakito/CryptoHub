from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from decimal import Decimal

from app.models.alert import Alert, AlertDirection, AlertHistory


async def get_alerts(db: AsyncSession, user_id: int) -> list[Alert]:
    result = await db.execute(
        select(Alert)
        .where(Alert.user_id == user_id)
        .order_by(Alert.created_at.desc())
    )
    return result.scalars().all()


async def get_alert_by_id(db: AsyncSession, alert_id: int, user_id: int) -> Alert | None:
    result = await db.execute(
        select(Alert)
        .where(Alert.id == alert_id, Alert.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def create_alert(
    db: AsyncSession,
    user_id: int,
    coin_id: str,
    coin_symbol: str,
    target_price: Decimal,
    direction: AlertDirection
) -> Alert:
    alert = Alert(
        user_id=user_id,
        coin_id=coin_id,
        coin_symbol=coin_symbol,
        target_price=target_price,
        direction=direction
    )
    db.add(alert)
    await db.flush()
    await db.refresh(alert)
    return alert


async def delete_alert(db: AsyncSession, alert_id: int, user_id: int) -> bool:
    result = await db.execute(
        delete(Alert).where(Alert.id == alert_id, Alert.user_id == user_id)
    )
    return result.rowcount > 0


async def get_alert_history(db: AsyncSession, user_id: int) -> list[AlertHistory]:
    result = await db.execute(
        select(AlertHistory)
        .join(Alert)
        .where(Alert.user_id == user_id)
        .order_by(AlertHistory.triggered_at.desc())
        .limit(100)
    )
    return result.scalars().all()


async def get_all_active_alerts(db: AsyncSession) -> list[Alert]:
    # Используется Celery для проверки цен.
    result = await db.execute(
        select(Alert).where(Alert.is_active == True)
    )
    return result.scalars().all()