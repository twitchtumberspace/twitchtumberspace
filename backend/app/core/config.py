from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Trading Platform MVP"
    app_env: str = Field(default="development", alias="APP_ENV")
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")
    database_url: str = Field(default="sqlite:///./trading.db", alias="DATABASE_URL")
    allow_live_trading: bool = Field(default=False, alias="ALLOW_LIVE_TRADING")
    default_assets: str = Field(default="BTC-USD,XAU-USD,CL=F", alias="DEFAULT_ASSETS")

    model_config = {"env_file": ".env", "case_sensitive": False, "populate_by_name": True}


@lru_cache
def get_settings() -> Settings:
    return Settings()
