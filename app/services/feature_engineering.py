"""
Feature preparation for the LightGBM fault-classification model.

Unlike the previous binary-risk model, this one does NOT use engineered
/ composite features — the training notebook confirmed no interaction
terms, polynomial features, or domain-specific features were created.
The fitted pipeline's ColumnTransformer expects exactly these raw
columns, selected by name:

  numeric:     vibration_rms, temperature_motor, current_phase_avg,
               pressure_level, rpm, hours_since_maintenance, ambient_temp
  categorical: machine_type, operating_mode

So this module just assembles a one-row DataFrame with the right
column names — the model's own Pipeline (imputer + scaler + one-hot)
handles the rest.
"""

import pandas as pd
from app.schemas.prediction import SensorInput


def build_feature_row(data: SensorInput) -> pd.DataFrame:
    """Convert SensorInput into the raw one-row DataFrame the pipeline expects."""
    raw = {
        "vibration_rms":           data.vibration_rms,
        "temperature_motor":       data.temperature_motor,
        "current_phase_avg":       data.current_phase_avg,
        "pressure_level":          data.pressure_level,
        "rpm":                     data.rpm,
        "hours_since_maintenance": data.hours_since_maintenance,
        "ambient_temp":            data.ambient_temp,
        "machine_type":            data.machine_type,
        "operating_mode":          data.operating_mode,
    }
    return pd.DataFrame([raw])


def get_raw_sensor_values(data: SensorInput) -> dict:
    """
    Raw sensor readings keyed by the same names used in
    core/thresholds.py, for the independent rule-based diagnostics layer.
    """
    return {
        "vibration_rms":           data.vibration_rms,
        "temperature_motor":       data.temperature_motor,
        "current_phase_avg":       data.current_phase_avg,
        "pressure_level":          data.pressure_level,
        "rpm":                     data.rpm,
        "hours_since_maintenance": data.hours_since_maintenance,
        "ambient_temp":            data.ambient_temp,
    }
