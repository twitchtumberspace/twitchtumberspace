from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.ml.pipeline import MLOrchestrator
from app.models.entities import Asset, EnvironmentType, Trade, TradeSide, TradingSignal
from app.services.market import MarketDataService


class TradingService:
    def __init__(self, db: Session):
        self.db = db
        self.market_service = MarketDataService(db)
        self.ml = MLOrchestrator()
        self.settings = get_settings()

    def generate_signals(self) -> list[TradingSignal]:
        assets = self.market_service.list_assets()
        generated: list[TradingSignal] = []
        for asset in assets:
            context = self.market_service.get_asset_context(asset.id)
            candles = [
                {"timestamp": c.timestamp, "close": c.close, "volume": c.volume, "high": c.high, "low": c.low}
                for c in context["candles"]
            ]
            news_items = [{"sentiment": n.sentiment, "headline": n.headline} for n in context["news"]]
            result = self.ml.score_market(self.ml.build_features(candles, news_items))
            side = TradeSide.buy if result["probability_up"] > 0.58 else TradeSide.sell if result["probability_up"] < 0.42 else TradeSide.hold
            signal = TradingSignal(
                asset_id=asset.id,
                side=side,
                confidence=result["confidence"],
                probability_up=result["probability_up"],
                rationale={
                    "top_features": result["top_features"],
                    "latest_news": news_items[-2:],
                    "regime_cluster": result["regime_cluster"],
                    "anomaly_score": result["anomaly_score"],
                },
                risk_snapshot=self._build_risk_snapshot(asset, result),
            )
            self.db.add(signal)
            generated.append(signal)
        self.db.commit()
        return generated

    def _build_risk_snapshot(self, asset: Asset, result: dict) -> dict:
        return {
            "asset": asset.symbol,
            "max_drawdown_limit": 0.12,
            "risk_per_trade": 0.01,
            "allow_live_trading": self.settings.allow_live_trading,
            "guardrails_passed": result["confidence"] >= 0.1 and result["anomaly_score"] > -0.2,
        }

    def execute_paper_trades(self) -> list[Trade]:
        signals = self.db.scalars(select(TradingSignal).order_by(TradingSignal.timestamp.desc())).all()
        trades: list[Trade] = []
        for signal in signals[:10]:
            if signal.side == TradeSide.hold or not signal.risk_snapshot.get("guardrails_passed"):
                continue
            price_anchor = 100 * signal.probability_up if signal.side == TradeSide.buy else 100 * (1 - signal.probability_up)
            trade = Trade(
                asset_id=signal.asset_id,
                signal_id=signal.id,
                environment=EnvironmentType.paper,
                side=signal.side,
                quantity=round(max(0.01, signal.confidence * 2), 4),
                entry_price=round(max(1.0, price_anchor), 2),
                pnl=0.0,
                decision_log={
                    "reason": "paper execution from ML signal",
                    "confidence": signal.confidence,
                    "rationale": signal.rationale,
                },
            )
            self.db.add(trade)
            trades.append(trade)
        self.db.commit()
        return trades
