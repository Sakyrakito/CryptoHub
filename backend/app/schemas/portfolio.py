from pydantic import BaseModel


class AssetAdd(BaseModel):
    coin_id: str
    coin_symbol: str
    coin_name: str
    amount: float


class AssetResponse(BaseModel):
    id: int
    coin_id: str
    coin_symbol: str
    coin_name: str
    amount: float
    current_price: float | None = None
    total_value: float | None = None
    change_24h: float | None = None

    model_config = {"from_attributes": True}


class PortfolioResponse(BaseModel):
    assets: list[AssetResponse]
    total_value: float