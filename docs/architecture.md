# Zielarchitektur der KI-Trading-Plattform

## 1. Systemkontext

Die Plattform besteht aus vier Hauptdomänen:

1. **Data Ingestion**: Import historischer Preis-, Volumen-, News- und Makrodaten.
2. **Research & AI**: Feature-Engineering, NLP/Sentiment, Regime Detection, Signalgenerierung.
3. **Execution & Risk**: Paper-/Live-Trading, Risikoregeln, Positionsverwaltung.
4. **Presentation**: Web-Dashboard, API, Explainability und Audit Trail.

## 2. Module

### Backend (FastAPI)
- REST-API für Assets, Signale, Trades, Backtests und Pipelines
- Service-Schicht mit klar getrennten Verantwortlichkeiten
- SQLAlchemy ORM + Alembic-Migrationen
- Pydantic-Schemas für Serialisierung und API-Verträge

### Datenhaltung
- PostgreSQL als primäre relationale Datenbank
- TimescaleDB-kompatibles Schema für Candles/Time-Series
- Tabellen für News, Events, Signals, Strategies, Trades, Risk Snapshots

### ML/AI
- Feature-Pipeline: Returns, Volatilität, Momentum, News-Sentiment, Regime-Marker
- Baseline-Modelle: RandomForestClassifier, IsolationForest, KMeans
- Erklärbarkeit: Feature Contribution Summary + News/Events Referenzen

### Trading-Engine
- Paper-Trading standardmäßig aktiv
- Risikoregeln: max. Drawdown, Risiko pro Trade, Positionsgröße, Cooldown
- Trading Guardrails: keine Orders ohne Datenqualität, ohne Modellvertrauen oder bei Risk-Breach

### Frontend (Next.js)
- Dashboard mit KPI-Kacheln, Signal-Liste, Backtest-Metriken, Positionen, Erklärungen
- API-Client gegen FastAPI
- SSR/CSR-Hybrid, vorbereitet für Auth und Live-Updates

## 3. Datenfluss

1. Ingestion lädt historische Daten oder Mock-Daten.
2. Normalisierung speichert Candles, News und Makro-Events.
3. ML-Pipeline berechnet Features und Signale.
4. Trading-Engine validiert Risiken und erzeugt Paper-Trades.
5. Dashboard visualisiert Zustände, Begründungen und Performance.

## 4. Erweiterbarkeit

- Neue Asset-Klassen über `AssetType` und Adapter-Service registrieren.
- Neue Datenquellen über Provider-Interface einhängen.
- Modellfamilien über `MLOrchestrator` austauschen.
- Broker später via `ExecutionService` adaptieren.
