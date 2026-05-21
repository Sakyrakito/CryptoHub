import asyncio
import logging
from decimal import Decimal

from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.price_checker.check_prices")
def check_prices():
    asyncio.run(_check_prices_async())


async def _check_prices_async():
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
    from app.core.config import settings
    from app.models.alert import AlertDirection, AlertHistory
    from app.services.alert import get_all_active_alerts
    from app.services.coingecko import get_coin_price

    # создаём свежий engine для каждого вызова задачи
    engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as db:
        try:
            alerts = await get_all_active_alerts(db)
            if not alerts:
                logger.info("Нет активных уведомлений")
                return

            coin_ids = list({alert.coin_id for alert in alerts})
            logger.info(f"Проверяем цены для: {coin_ids}")

            prices = await get_coin_price(coin_ids)

            triggered_count = 0
            for alert in alerts:
                coin_data = prices.get(alert.coin_id)
                if not coin_data:
                    continue

                current_price = Decimal(str(coin_data["usd"]))
                target_price = alert.target_price

                should_trigger = (
                    alert.direction == AlertDirection.ABOVE
                    and current_price >= target_price
                ) or (
                    alert.direction == AlertDirection.BELOW
                    and current_price <= target_price
                )

                if should_trigger:
                    alert.is_active = False
                    history = AlertHistory(
                        alert_id=alert.id,
                        price_at_trigger=current_price,
                    )
                    db.add(history)
                    triggered_count += 1
                    logger.info(
                        f"Уведомление сработало: {alert.coin_symbol} "
                        f"{alert.direction} {target_price} "
                        f"(текущая: {current_price})"
                    )

            await db.commit()
            logger.info(f"Проверка завершена. Сработало уведомлений: {triggered_count}")

        except Exception as e:
            await db.rollback()
            logger.error(f"Ошибка при проверке цен: {e}")
            raise

    await engine.dispose()