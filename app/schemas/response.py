from pydantic import BaseModel
from pydantic.config import ConfigDict
from typing import List
from enum import Enum


class RiskLevel(str, Enum):
    HEALTHY  = "HEALTHY"
    AT_RISK  = "AT_RISK"
    CRITICAL = "CRITICAL"


class AlertStatus(str, Enum):
    WARNING  = "WARNING"
    CRITICAL = "CRITICAL"
    
class SensorAlert(BaseModel):
    sensor: str
    feature_key: str
    value: float
    unit: str
    status: AlertStatus
    message: str
    warn_range: List[float]
    crit_range: List[float]


class PredictionResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    machine_id: str
    prediction: int
    risk_probability: float
    risk_percentage: float
    risk_level: RiskLevel
    recommendation: str
    sensor_alerts: List[SensorAlert] = []
    alert_count: int = 0
    critical_count: int = 0
    warning_count: int = 0
    model_version: str = "1.0.0"


class HealthResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    status: str
    model_loaded: bool
    version: str