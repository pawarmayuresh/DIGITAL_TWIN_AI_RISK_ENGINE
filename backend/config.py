from typing import List

# Use pydantic v2 settings API
try:
    from pydantic_settings import BaseSettings
    from pydantic import Field
except Exception:
    # fall back for environments with older pydantic
    from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    app_env: str = "development"
    app_version: str = "0.1.0"
    cors_origins: List[str] = ["*"]

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


settings = Settings()
