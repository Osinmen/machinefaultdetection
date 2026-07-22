import joblib
import logging
from pathlib import Path
from app.core.config import settings
from app.core.exceptions import ModelNotLoadedException

logger = logging.getLogger(__name__)

# The pipeline's LGBMClassifier was fit on integer-encoded labels
# (sklearn's LabelEncoder, alphabetical order) and only ever outputs
# 0-4 — this mapping is NOT saved inside the .pkl, it's reconstructed
# from the training notebook's printed "Class mapping" output, so it
# must stay in sync if the model is ever retrained.
CLASS_NAMES = ["bearing", "electrical", "healthy", "hydraulic", "motor_overheat"]


class ModelService:
    _model = None

    @classmethod
    def load_model(cls):
        model_path = Path(settings.MODEL_PATH)
        if not model_path.exists():
            logger.warning(f"Model file not found at {model_path}. Place lightgbm_model.pkl in /artifacts")
            return
        cls._model = joblib.load(model_path)
        logger.info(f"LightGBM model loaded successfully from {model_path}")

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
