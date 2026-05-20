from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.alert import AlertCreate, AlertResponse, AlertHistoryResponse
from app.services.alert import (
    get_alerts,
    create_alert,
    delete_alert,
    get_alert_history,
)

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertResponse])
async def list_alerts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_alerts(db, current_user.id)


@router.post("", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_new_alert(
    data: AlertCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await create_alert(
        db,
        user_id=current_user.id,
        coin_id=data.coin_id,
        coin_symbol=data.coin_symbol,
        target_price=data.target_price,
        direction=data.direction,
    )


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    removed = await delete_alert(db, alert_id, current_user.id)
    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено",
        )


@router.get("/history", response_model=list[AlertHistoryResponse])
async def alert_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_alert_history(db, current_user.id)