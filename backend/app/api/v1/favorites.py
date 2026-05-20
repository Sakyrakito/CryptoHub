from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.favorite import FavoriteAdd, FavoriteResponse
from app.services.favorite import (
    get_favorites,
    add_favorite,
    remove_favorite,
    is_favorite,
)

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("", response_model=list[FavoriteResponse])
async def list_favorites(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_favorites(db, current_user.id)


@router.post("", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
async def add_to_favorites(
    data: FavoriteAdd,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    already = await is_favorite(db, current_user.id, data.coin_id)
    if already:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Монета уже в избранном",
        )
    return await add_favorite(
        db,
        user_id=current_user.id,
        coin_id=data.coin_id,
        coin_symbol=data.coin_symbol,
        coin_name=data.coin_name,
    )


@router.delete("/{coin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_favorites(
    coin_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    removed = await remove_favorite(db, current_user.id, coin_id)
    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Монета не найдена в избранном",
        )


@router.get("/{coin_id}/check")
async def check_favorite(
    coin_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return {"is_favorite": await is_favorite(db, current_user.id, coin_id)}