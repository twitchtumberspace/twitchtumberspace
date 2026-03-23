from datetime import datetime, timedelta
import random

from sqlalchemy.orm import Session

from app.models.entities import Asset, AssetType, MarketCandle, NewsEvent


ASSETS = [
    ("BTC-USD", "Bitcoin", AssetType.crypto, 65000),
    ("XAU-USD", "Gold", AssetType.metal, 2150),
    ("CL=F", "Crude Oil", AssetType.commodity, 78),
]


NEWS_TEMPLATES = [
    ("Makrodaten überraschen positiv", 0.6, "macro"),
    ("Zentralbank signalisiert Straffung", -0.4, "macro"),
    ("ETF-Zuflüsse steigen deutlich", 0.8, "market"),
    ("Risikomärkte unter Druck", -0.7, "risk"),
]


def seed_demo_data(db: Session) -> None:
    if db.query(Asset).count() > 0:
        return

    now = datetime.utcnow()
    for symbol, name, asset_type, base_price in ASSETS:
        asset = Asset(symbol=symbol, name=name, asset_type=asset_type)
        db.add(asset)
        db.flush()

        price = base_price
        for step in range(180):
            ts = now - timedelta(hours=step * 4)
            drift = random.uniform(-0.03, 0.03)
            price = max(1, price * (1 + drift))
            candle = MarketCandle(
                asset_id=asset.id,
                timestamp=ts,
                interval="4h",
                open=price * (1 - 0.01),
                high=price * (1 + 0.015),
                low=price * (1 - 0.02),
                close=price,
                volume=random.uniform(1000, 100000),
                metadata_json={"source": "mock"},
            )
            db.add(candle)

        for idx, tpl in enumerate(NEWS_TEMPLATES):
            headline, sentiment, event_type = tpl
            db.add(
                NewsEvent(
                    asset_id=asset.id,
                    timestamp=now - timedelta(days=idx * 3 + 1),
                    headline=f"{name}: {headline}",
                    source="mock-feed",
                    sentiment=sentiment,
                    event_type=event_type,
                    summary=f"Mock-Zusammenfassung für {name} mit Sentiment {sentiment}.",
                )
            )

    db.commit()
