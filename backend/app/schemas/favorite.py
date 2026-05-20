from datetime import datetime
from pydantic import BaseModel


class FavoriteAdd(BaseModel):
    coin_id: str
    coin_symbol: str
    coin_name: str


class FavoriteResponse(BaseModel):
    id: int
    coin_id: str
    coin_symbol: str
    coin_name: str
    added_at: datetime

    model_config = {"from_attributes": True}