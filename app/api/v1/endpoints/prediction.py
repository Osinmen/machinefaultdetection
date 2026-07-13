from fastapi import APIRouter
from app.schemas.prediction import SensorInput
from app.schemas.response import PredictionResponse
from app.services.prediction_service import run_prediction

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, summary="Run failure prediction")
def predict(data: SensorInput):
    """
    Submit sensor readings for a machine and get a failure prediction.

    - **prediction**: 0 = healthy, 1 = at risk
    - **risk_probability**: confidence score (0.0 – 1.0)
    - **risk_level**: HEALTHY | AT_RISK | CRITICAL
    - **recommendation**: human-readable action to take
    """
    return run_prediction(data)
