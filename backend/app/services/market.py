from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import Asset, MarketCandle, NewsEvent
from app.services.seed import seed_demo_data


class MarketDataService:
    def __init__(self, db: Session):
        self.db = db

    def ensure_seeded(self) -> None:
        seed_demo_data(self.db)

    def list_assets(self):
        self.ensure_seeded()
        return self.db.scalars(select(Asset).order_by(Asset.symbol)).all()

    def get_asset_context(self, asset_id: int) -> dict:
        candles = self.db.scalars(
            select(MarketCandle).where(MarketCandle.asset_id == asset_id).order_by(MarketCandle.timestamp)
        ).all()
        news = self.db.scalars(select(NewsEvent).where(NewsEvent.asset_id == asset_id).order_by(NewsEvent.timestamp)).all()
        return {"candles": candles, "news": news}
