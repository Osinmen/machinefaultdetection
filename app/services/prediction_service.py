import logging
from app.schemas.prediction import SensorInput
from app.schemas.response import PredictionResponse, RiskLevel, SensorAlert
from app.services.model_service import ModelService
from app.services.feature_engineering import engineer_features, get_engineered_values
from app.services.sensor_diagnostics import run_sensor_diagnostics
from app.core.config import settings
from app.core.exceptions import FeatureEngineeringException

logger = logging.getLogger(__name__)


def get_recommendation(risk_level: RiskLevel, risk_pct: float) -> str:
    if risk_level == RiskLevel.CRITICAL:
        return "CRITICAL: Immediate inspection required. Take machine offline if possible."
    elif risk_level == RiskLevel.AT_RISK:
        return f"WARNING: Schedule maintenance within 3-5 days. Risk at {risk_pct:.1f}%."
    else:
        return "Machine is healthy. Continue standard monitoring schedule."

def run_prediction(data: SensorInput) -> PredictionResponse:
    try:
        # Get engineered values for sensor diagnostics (before dropping cols)
        eng_values = get_engineered_values(data)

        # Get feature DataFrame for model (after dropping cols)
        features_df = engineer_features(data)
    except Exception as e:
        raise FeatureEngineeringException(str(e))

    # ML Prediction
    model       = ModelService.get_model()
    prediction  = int(model.predict(features_df)[0])
    probability = float(model.predict_proba(features_df)[0][1])
    risk_pct    = round(probability * 100, 2)

    if probability >= settings.CRITICAL_RISK_THRESHOLD:
        risk_level = RiskLevel.CRITICAL
    elif probability >= settings.HIGH_RISK_THRESHOLD:
        risk_level = RiskLevel.AT_RISK
    else:
        risk_level = RiskLevel.HEALTHY

    # Sensor Diagnostics — independent rule engine
    diagnostics   = run_sensor_diagnostics(eng_values)
    sensor_alerts = [SensorAlert(**a) for a in diagnostics["sensor_alerts"]]

    return PredictionResponse(
        machine_id=data.machine_id,
        prediction=prediction,
        risk_probability=probability,
        risk_percentage=risk_pct,
        risk_level=risk_level,
        recommendation=get_recommendation(risk_level, risk_pct),
        sensor_alerts=sensor_alerts,
        alert_count=diagnostics["alert_count"],
        critical_count=diagnostics["critical_count"],
        warning_count=diagnostics["warning_count"],
    )