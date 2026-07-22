from fastapi import APIRouter
from app.schemas.prediction import SensorInput
from app.schemas.response import PredictionResponse
from app.services.prediction_service import run_prediction

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, summary="Run failure prediction")
def predict(data: SensorInput):
    """
    Submit sensor readings for a machine and get a fault-type prediction.

    - **predicted_class**: healthy | bearing | electrical | hydraulic | motor_overheat
    - **confidence**: probability of the predicted class (0.0 – 1.0)
    - **class_probabilities**: probability for all 5 classes
    - **low_confidence**: true if the top prediction is below the confidence threshold
    - **recommendation**: human-readable action to take
    """
    return run_prediction(data)
