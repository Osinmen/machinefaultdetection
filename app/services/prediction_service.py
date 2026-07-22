import logging
import uuid
from app.schemas.prediction import SensorInput
from app.schemas.response import PredictionResponse, SensorAlert
from app.services.model_service import ModelService, CLASS_NAMES
from app.services.feature_engineering import build_feature_row, get_raw_sensor_values
from app.services.sensor_diagnostics import run_sensor_diagnostics
from app.core.config import settings
from app.core.exceptions import FeatureEngineeringException

logger = logging.getLogger(__name__)


def get_recommendation(predicted_class: str, confidence: float, low_confidence: bool) -> str:
    if predicted_class == "healthy":
        if low_confidence:
            return "Likely healthy, but confidence is low — recheck sensor readings or re-run shortly."
        return "Machine is healthy. Continue standard monitoring schedule."

    label = predicted_class.replace("_", " ")
    if low_confidence:
        return (
            f"Possible {label} fault detected, but confidence is low "
            f"({confidence * 100:.1f}%) — verify readings before acting."
        )
    return f"{label.capitalize()} fault detected (confidence {confidence * 100:.1f}%). Schedule inspection."


def run_prediction(data: SensorInput) -> PredictionResponse:
    try:
        raw_sensor_values = get_raw_sensor_values(data)
        features_df = build_feature_row(data)
    except Exception as e:
        raise FeatureEngineeringException(str(e))

    # ML Prediction — multi-class, 5 possible fault types
    model = ModelService.get_model()
    probabilities = model.predict_proba(features_df)[0]

    class_probabilities = {
        CLASS_NAMES[i]: round(float(p), 4) for i, p in enumerate(probabilities)
    }
    predicted_idx = int(probabilities.argmax())
    predicted_class = CLASS_NAMES[predicted_idx]
    confidence = float(probabilities[predicted_idx])
    low_confidence = confidence < settings.LOW_CONFIDENCE_THRESHOLD

    # Sensor Diagnostics (independent rule engine, runs on raw readings)
    diagnostics = run_sensor_diagnostics(raw_sensor_values)
    sensor_alerts = [SensorAlert(**a) for a in diagnostics["sensor_alerts"]]

    machine_id = data.machine_id or f"MCH-{uuid.uuid4().hex[:8].upper()}"

    return PredictionResponse(
        machine_id=machine_id,
        predicted_class=predicted_class,
        confidence=round(confidence, 4),
        class_probabilities=class_probabilities,
        is_healthy=(predicted_class == "healthy"),
        low_confidence=low_confidence,
        recommendation=get_recommendation(predicted_class, confidence, low_confidence),
        sensor_alerts=sensor_alerts,
        alert_count=diagnostics["alert_count"],
        critical_count=diagnostics["critical_count"],
        warning_count=diagnostics["warning_count"],
    )
