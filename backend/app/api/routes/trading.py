from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.trading import BacktestResult, SignalRead, TradeRead
from app.services.backtesting import BacktestingService
from app.services.trading import TradingService

router = APIRouter(prefix="/trading", tags=["trading"])


@router.post("/signals", response_model=list[SignalRead])
def generate_signals(db: Session = Depends(get_db)):
    service = TradingService(db)
    return service.generate_signals()


@router.post("/paper-trades", response_model=list[TradeRead])
def execute_paper_trades(db: Session = Depends(get_db)):
    service = TradingService(db)
    return service.execute_paper_trades()


@router.post("/backtest", response_model=BacktestResult)
def run_backtest(db: Session = Depends(get_db)):
    service = BacktestingService(db)
    result = service.run_baseline_backtest()
    return BacktestResult(strategy_name=result.name, metrics=result.metrics, trades=[])
