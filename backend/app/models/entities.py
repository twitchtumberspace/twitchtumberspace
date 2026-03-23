from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AssetType(str, Enum):
    commodity = "commodity"
    metal = "metal"
    crypto = "crypto"
    equity = "equity"
    forex = "forex"
    index = "index"


class TradeSide(str, Enum):
    buy = "buy"
    sell = "sell"
    hold = "hold"


class EnvironmentType(str, Enum):
    paper = "paper"
    live = "live"


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    asset_type: Mapped[AssetType] = mapped_column(SqlEnum(AssetType))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    candles: Mapped[list["MarketCandle"]] = relationship(back_populates="asset", cascade="all, delete-orphan")
    news_items: Mapped[list["NewsEvent"]] = relationship(back_populates="asset", cascade="all, delete-orphan")
    signals: Mapped[list["TradingSignal"]] = relationship(back_populates="asset", cascade="all, delete-orphan")


class MarketCandle(Base):
    __tablename__ = "market_candles"

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    interval: Mapped[str] = mapped_column(String(8), index=True)
    open: Mapped[float] = mapped_column(Float)
    high: Mapped[float] = mapped_column(Float)
    low: Mapped[float] = mapped_column(Float)
    close: Mapped[float] = mapped_column(Float)
    volume: Mapped[float] = mapped_column(Float)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)

    asset: Mapped[Asset] = relationship(back_populates="candles")


class NewsEvent(Base):
    __tablename__ = "news_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    headline: Mapped[str] = mapped_column(String(255))
    source: Mapped[str] = mapped_column(String(120))
    sentiment: Mapped[float] = mapped_column(Float, default=0.0)
    event_type: Mapped[str] = mapped_column(String(50), default="news")
    summary: Mapped[str] = mapped_column(Text)

    asset: Mapped[Asset] = relationship(back_populates="news_items")


class TradingSignal(Base):
    __tablename__ = "trading_signals"

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    side: Mapped[TradeSide] = mapped_column(SqlEnum(TradeSide))
    confidence: Mapped[float] = mapped_column(Float)
    probability_up: Mapped[float] = mapped_column(Float)
    rationale: Mapped[dict] = mapped_column(JSON, default=dict)
    risk_snapshot: Mapped[dict] = mapped_column(JSON, default=dict)

    asset: Mapped[Asset] = relationship(back_populates="signals")
    trades: Mapped[list["Trade"]] = relationship(back_populates="signal")


class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), index=True)
    signal_id: Mapped[int | None] = mapped_column(ForeignKey("trading_signals.id"), nullable=True)
    environment: Mapped[EnvironmentType] = mapped_column(SqlEnum(EnvironmentType), default=EnvironmentType.paper)
    side: Mapped[TradeSide] = mapped_column(SqlEnum(TradeSide))
    quantity: Mapped[float] = mapped_column(Float)
    entry_price: Mapped[float] = mapped_column(Float)
    exit_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    pnl: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(30), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    decision_log: Mapped[dict] = mapped_column(JSON, default=dict)

    signal: Mapped[TradingSignal | None] = relationship(back_populates="trades")


class StrategyRun(Base):
    __tablename__ = "strategy_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    metrics: Mapped[dict] = mapped_column(JSON, default=dict)
    config: Mapped[dict] = mapped_column(JSON, default=dict)
