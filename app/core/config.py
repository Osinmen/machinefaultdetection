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
    MODEL_PATH: str = str(BASE_DIR / "artifacts" / "lightgbm_model.pkl")

    # CORS — allow all in dev; tighten in prod
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Below this, the top predicted class's probability is considered
    # too close to flag confidently — response marks low_confidence=True
    # rather than picking a binary risk tier (multi-class output has no
    # single "risk score" the way the old binary model did).
    LOW_CONFIDENCE_THRESHOLD: float = 0.5

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
