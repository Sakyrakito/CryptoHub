from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from app.models.alert import AlertDirection


class AlertCreate(BaseModel):
    coin_id: str
    coin_symbol: str
    target_price: Decimal
    direction: AlertDirection


class AlertResponse(BaseModel):
    id: int
    coin_id: str
    coin_symbol: str
    target_price: Decimal
    direction: AlertDirection
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AlertHistoryResponse(BaseModel):
    id: int
    alert_id: int
    triggered_at: datetime
    price_at_trigger: Decimal

    model_config = {"from_attributes": True}