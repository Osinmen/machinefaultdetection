from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "MachineGuard API"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # Model
    MODEL_PATH: str = str(BASE_DIR / "artifacts" / "cat_model.joblib")

    # CORS — allow all in dev; tighten in prod
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Risk thresholds
    HIGH_RISK_THRESHOLD: float = 0.5   # >= 50% → AT RISK
    CRITICAL_RISK_THRESHOLD: float = 0.75  # >= 75% → CRITICAL

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
