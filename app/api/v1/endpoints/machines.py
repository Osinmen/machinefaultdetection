from fastapi import APIRouter
from app.schemas.prediction import VALID_MACHINE_TYPES, VALID_OPERATING_MODES

router = APIRouter()

@router.get("/machines/types", summary="Get supported machine types")
def get_machine_types():
    """Returns the list of machine types the model was trained on."""
    return {"machine_types": VALID_MACHINE_TYPES}

@router.get("/machines/operating-modes", summary="Get supported operating modes")
def get_operating_modes():
    """Returns the list of operating modes the model was trained on."""
    return {"operating_modes": VALID_OPERATING_MODES}
