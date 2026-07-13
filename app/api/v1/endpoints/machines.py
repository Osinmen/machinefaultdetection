from fastapi import APIRouter

router = APIRouter()

@router.get("/machines/types", summary="Get supported machine types")
def get_machine_types():
    """Returns the list of machine types the model was trained on."""
    return {
        "machine_types": [
            "Conveyor Belt", "Compressor", "Pump", "Motor", "Turbine",
            "Generator", "Hydraulic Press", "CNC Machine", "Robotic Arm", "Lathe"
        ]
    }
