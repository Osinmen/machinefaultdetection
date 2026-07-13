from pydantic import BaseModel, Field, field_validator
from pydantic.config import ConfigDict

# Real machine types from the training dataset
VALID_MACHINE_TYPES = [
    "CMM",
    "CNC Lathe",
    "Industrial Chiller",
    "Injection Molder",
    "Labeler",
    "Pump",
    "Vacuum Packer",
    "Conveyor Belt",  # reference category (dropped in encoding)
]

class SensorInput(BaseModel):
    machine_id: str = Field(..., example="MCH-001")
    machine_type: str = Field(..., example="Pump")
    installation_year: int = Field(..., ge=1990, le=2026, example=2018)
    temperature_c: float = Field(..., example=75.4)
    vibration_mms: float = Field(..., example=3.2)
    power_consumption_kw: float = Field(..., example=12.5)
    operational_hours: float = Field(..., ge=0, example=14500)
    last_maintenance_days_ago: int = Field(..., ge=0, example=45)
    maintenance_history_count: int = Field(..., ge=0, example=8)
    failure_history_count: int = Field(..., ge=0, example=2)
    oil_level_pct: float = Field(..., ge=0, le=100, example=72.0)
    coolant_level_pct: float = Field(..., ge=0, le=100, example=85.0)
    ai_supervision: bool = Field(..., example=True)
    ai_override_events: int = Field(..., ge=0, example=3)
    remaining_useful_life_days: float = Field(..., ge=0, example=120.0)
    error_codes_last_30_days: int = Field(..., ge=0, example=2)
    sound_db: float = Field(..., ge=0, example=68.5)

    @field_validator("temperature_c", "vibration_mms", "power_consumption_kw")
    @classmethod
    def must_be_non_negative(cls, v, info):
        if v < 0:
            raise ValueError(f"{info.field_name} cannot be negative")
        return v

    @field_validator("installation_year")
    @classmethod
    def year_not_future(cls, v):
        if v > 2026:
            raise ValueError("Installation year cannot be in the future")
        return v