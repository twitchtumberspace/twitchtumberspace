# AI Trading Platform MVP

Eine produktionsnahe, modulare Webplattform für historische Marktanalyse, Explainable-AI-Signale, Backtesting und automatisiertes **Paper Trading**. Live-Trading bleibt standardmäßig deaktiviert.

## Projektarchitektur

```text
ai-trading-platform/
├── backend/
│   ├── app/
│   │   ├── api/routes        # REST-Endpunkte
│   │   ├── core              # Settings, Sicherheit, Konfiguration
│   │   ├── db                # Datenbank, Session, Seed-Daten
│   │   ├── models            # SQLAlchemy-Modelle
│   │   ├── schemas           # Pydantic-Schemas
│   │   ├── services          # Datenimport, Trading, Backtesting, Explainability
│   │   ├── ml                # Feature-Engineering und ML-Pipeline
│   │   └── main.py           # FastAPI-App
│   ├── tests                 # API- und Service-Tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/app               # React/Next.js Seiten
│   ├── src/components        # Dashboard-Komponenten
│   ├── src/lib               # API-Client und Mock-Fallbacks
│   ├── package.json
│   └── Dockerfile
├── docs/
│   └── architecture.md       # Detaillierte Zielarchitektur
├── scripts/
│   └── seed_demo_data.py     # Beispiel-Pipeline-Trigger
├── docker-compose.yml
└── README.md
```

## MVP-Umfang

- FastAPI-Backend mit modularen Services
- PostgreSQL/TimescaleDB-kompatible Datenmodelle via SQLAlchemy
- Historische Markt-, Nachrichten- und Ereignisdaten mit Mock-Ingestion
- ML-Pipeline für Signal-Scoring und Regime-Erkennung
- Backtesting- und Paper-Trading-Engine mit Risikoregeln
- Explainable-AI-Entscheidungsprotokollierung
- Next.js-Dashboard für Märkte, Signale, Positionen und Backtests
- Docker Compose für lokale Entwicklung

## Schnellstart

### Voraussetzungen

- Docker + Docker Compose **oder**
- Python 3.11+ und Node.js 20+

### Mit Docker

```bash
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- OpenAPI: http://localhost:8000/docs

### Lokal

#### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Konfiguration

Die Anwendung nutzt Umgebungsvariablen. Relevante Variablen:

- `DATABASE_URL`
- `APP_ENV`
- `SECRET_KEY`
- `ALLOW_LIVE_TRADING=false`
- `DEFAULT_ASSETS=BTC-USD,XAU-USD,CL=F`

## Roadmap nach MVP

1. Echte Datenquellen (Polygon, Alpha Vantage, Binance, NewsAPI, GDELT)
2. Celery/Redis für asynchrone Jobs
3. TimescaleDB-Hypertables und Partitionierung
4. Modell-Registry, Feature Store, Experiment Tracking
5. Broker-Integrationen für Live-Trading (nur nach expliziter Freigabe)

## Sicherheit und Compliance

- Live-Trading ist standardmäßig deaktiviert.
- API-Secrets werden ausschließlich über Umgebungsvariablen bezogen.
- Jede Handelsentscheidung wird mit Kontext, Risiko und Erklärung gespeichert.
- Rollenmodell ist vorbereitet und kann an OAuth/JWT angebunden werden.
