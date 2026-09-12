from typing import Literal
from pydantic import BaseModel, Field


class OrderRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    side: Literal["BUY", "SELL"]
    volume: int = Field(gt=0)
    price: float = Field(gt=0)
    price_type: Literal["LIMIT"] = "LIMIT"


class OrderResult(BaseModel):
    accepted: bool
    order_id: str | None = None
    message: str
    mode: str


class RiskStatus(BaseModel):
    trading_enabled: bool
    emergency_stop: bool
    daily_pnl: float
    max_daily_loss_thb: float
