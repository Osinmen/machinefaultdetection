from pydantic import BaseModel, Field, field_validator
from pydantic.config import ConfigDict
from typing import Optional

# Categories the model was actually trained on — baked into the
# fitted OneHotEncoder, so anything outside these lists is silently
# treated as "unknown" by the pipeline rather than raising an error.
VALID_MACHINE_TYPES = ["CNC", "Compressor", "Pump", "Robotic Arm"]
VALID_OPERATING_MODES = ["idle", "normal", "peak"]


class SensorInput(BaseModel):
    machine_id: Optional[str] = Field(None, example="MCH-001")
    machine_type: str = Field(..., example="Pump")
    operating_mode: str = Field(..., example="normal")

    vibration_rms: float = Field(..., ge=0, example=2.4)
    temperature_motor: float = Field(..., example=68.5)
    current_phase_avg: float = Field(..., ge=0, example=9.2)
    pressure_level: float = Field(..., ge=0, example=55.0)
    rpm: float = Field(..., ge=0, example=1200)
    hours_since_maintenance: float = Field(..., ge=0, example=150)
    ambient_temp: float = Field(..., example=13.0)

    @field_validator("machine_type")
    @classmethod
    def machine_type_valid(cls, v):
        if v not in VALID_MACHINE_TYPES:
            raise ValueError(
                f"machine_type must be one of {VALID_MACHINE_TYPES}, got '{v}'"
            )
        return v

    @field_validator("operating_mode")
    @classmethod
    def operating_mode_valid(cls, v):
        if v not in VALID_OPERATING_MODES:
            raise ValueError(
                f"operating_mode must be one of {VALID_OPERATING_MODES}, got '{v}'"
            )
        return v
