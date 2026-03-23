from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import StrategyRun, Trade, TradingSignal
from app.schemas.trading import AssetRead, DashboardResponse, SignalRead, TradeRead
from app.services.market import MarketDataService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    market = MarketDataService(db)
    assets = market.list_assets()
    signals = db.scalars(select(TradingSignal).order_by(TradingSignal.timestamp.desc()).limit(10)).all()
    trades = db.scalars(select(Trade).order_by(Trade.created_at.desc()).limit(10)).all()
    backtests = db.scalars(select(StrategyRun).order_by(StrategyRun.created_at.desc()).limit(10)).all()
    insights = {
        "paper_trading_only": True,
        "live_trading_enabled": False,
        "explainability": "Jede Entscheidung enthält Feature-Gewichte, News-Kontext und Risikosnapshot.",
    }
    return DashboardResponse(
        assets=[AssetRead.model_validate(asset) for asset in assets],
        signals=[SignalRead.model_validate(signal) for signal in signals],
        trades=[TradeRead.model_validate(trade) for trade in trades],
        backtests=[{"id": item.id, "name": item.name, "metrics": item.metrics} for item in backtests],
        insights=insights,
    )
