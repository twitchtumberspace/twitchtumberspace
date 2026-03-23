from fastapi import FastAPI

from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.trading import router as trading_router
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine

settings = get_settings()
app = FastAPI(title=settings.app_name)
Base.metadata.create_all(bind=engine)
app.include_router(dashboard_router)
app.include_router(trading_router)


@app.get("/health")
def healthcheck():
    return {
        "status": "ok",
        "environment": settings.app_env,
        "paper_trading_only": not settings.allow_live_trading,
    }
