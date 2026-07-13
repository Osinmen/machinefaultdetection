import joblib
import logging
from pathlib import Path
from app.core.config import settings
from app.core.exceptions import ModelNotLoadedException

logger = logging.getLogger(__name__)

class ModelService:
    _model = None

    @classmethod
    def load_model(cls):
        model_path = Path(settings.MODEL_PATH)
        if not model_path.exists():
            logger.warning(f"Model file not found at {model_path}. Place cat_model.joblib in /artifacts")
            return
        cls._model = joblib.load(model_path)
        logger.info(f"CatBoost model loaded successfully from {model_path}")

    @classmethod
    def unload_model(cls):
        cls._model = None
        logger.info("Model unloaded")

    @classmethod
    def get_model(cls):
        if cls._model is None:
            raise ModelNotLoadedException("Model is not loaded")
        return cls._model

    @classmethod
    def is_loaded(cls) -> bool:
        return cls._model is not None
