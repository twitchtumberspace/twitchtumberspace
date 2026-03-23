from datetime import datetime
from pydantic import BaseModel

from app.models.entities import AssetType, EnvironmentType, TradeSide


class AssetRead(BaseModel):
    id: int
    symbol: str
    name: str
    asset_type: AssetType
    is_active: bool

    model_config = {"from_attributes": True}


class SignalRead(BaseModel):
    id: int
    asset_id: int
    timestamp: datetime
    side: TradeSide
    confidence: float
    probability_up: float
    rationale: dict
    risk_snapshot: dict

    model_config = {"from_attributes": True}


class TradeRead(BaseModel):
    id: int
    asset_id: int
    signal_id: int | None
    environment: EnvironmentType
    side: TradeSide
    quantity: float
    entry_price: float
    exit_price: float | None
    pnl: float
    status: str
    decision_log: dict

    model_config = {"from_attributes": True}


class BacktestResult(BaseModel):
    strategy_name: str
    metrics: dict
    trades: list[dict]


class DashboardResponse(BaseModel):
    assets: list[AssetRead]
    signals: list[SignalRead]
    trades: list[TradeRead]
    backtests: list[dict]
    insights: dict
