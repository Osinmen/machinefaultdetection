"""
Feature engineering — mirrors the notebook pipeline exactly.
Sources: cleaning.py, transforms.py, encoding.py, pipeline.py

Machine types in training data (after pd.get_dummies drop_first=True):
  Encoded: CMM, CNC_Lathe, Industrial_Chiller, Injection_Molder,
           Labeler, Pump, Vacuum_Packer
  Reference (dropped): Conveyor_Belt (first alphabetically)
"""

import numpy as np
import pandas as pd
from app.schemas.prediction import SensorInput

DATASET_YEAR = 2026

# Columns dropped after engineering — from pipeline.py cols_to_drop
COLS_TO_DROP = [
    "Remaining_Useful_Life_days", "RUL_Critical_Flag",
    "Error_Codes_Last_30_Days", "Oil_Level_pct", "Coolant_Level_pct",
    "Low_Oil_Flag", "Low_Coolant_Flag", "AI_Override_Events",
    "Maintenance_History_Count", "MachineType_Crane",
    "MachineType_Shuttle_System", "Acoustic_Power_Index",
    "AI_Conflict_Flag", "Vibration_mms", "RUL_Log", "Health_Risk_Score",
]

# Real machine types from training dataset
# drop_first=True drops "Conveyor_Belt" (first alphabetically)
MACHINE_TYPE_DUMMIES = [
    "MachineType_CMM",
    "MachineType_CNC_Lathe",
    "MachineType_Industrial_Chiller",
    "MachineType_Injection_Molder",
    "MachineType_Labeler",
    "MachineType_Pump",
    "MachineType_Vacuum_Packer",
]

CLIP_RULES = {
    "Vibration_mms":        (0, None),
    "Power_Consumption_kW": (0, None),
    "Temperature_C":        (0, None),
    "Oil_Level_pct":        (0, 100),
    "Coolant_Level_pct":    (0, 100),
}

def _clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col, (lower, upper) in CLIP_RULES.items():
        if col in df.columns:
            df[col] = df[col].clip(lower=lower, upper=upper)
    return df

def _add_age_features(df):
    df = df.copy()
    df["Machine_Age_Years"] = DATASET_YEAR - df["Installation_Year"]
    df["Machine_Age_Years"] = df["Machine_Age_Years"].clip(lower=0) + 1
    df["Hours_Per_Year"] = df["Operational_Hours"] / df["Machine_Age_Years"]
    return df

def _add_maintenance_features(df):
    df = df.copy()
    df["Failure_Per_Maintenance"] = (
        df["Failure_History_Count"] / (df["Maintenance_History_Count"] + 1)
    )
    df["Maintenance_Gap_Risk"] = (
        df["Last_Maintenance_Days_Ago"] / (df["Maintenance_History_Count"] + 1)
    )
    df["Overdue_Maintenance"] = (df["Last_Maintenance_Days_Ago"] > 180).astype(int)
    df["Daily_Error_Rate"] = df["Error_Codes_Last_30_Days"] / 30
    return df

def _add_sensor_features(df):
    df = df.copy()
    df["Fluid_Deficit_Score"] = (
        (100 - df["Oil_Level_pct"]) + (100 - df["Coolant_Level_pct"])
    )
    df["Low_Oil_Flag"]        = (df["Oil_Level_pct"] < 20).astype(int)
    df["Low_Coolant_Flag"]    = (df["Coolant_Level_pct"] < 20).astype(int)
    df["Fluid_Critical_Flag"] = (
        (df["Low_Oil_Flag"] == 1) | (df["Low_Coolant_Flag"] == 1)
    ).astype(int)
    df["Thermal_Vibration_Index"] = df["Temperature_C"] * df["Vibration_mms"]
    df["Acoustic_Power_Index"]    = df["Sound_dB"] * df["Power_Consumption_kW"]
    return df

def _add_rul_features(df):
    df = df.copy()
    df["RUL_Critical_Flag"] = (df["Remaining_Useful_Life_days"] <= 30).astype(int)
    df["RUL_Log"]           = np.log1p(df["Remaining_Useful_Life_days"])
    return df

def _add_ai_features(df):
    df = df.copy()
    df["Override_Rate"] = (
        df["AI_Override_Events"] / (df["Operational_Hours"] / 1000 + 1)
    )
    df["AI_Conflict_Flag"] = (
        (df["AI_Supervision"] == 1) & (df["AI_Override_Events"] > 0)
    ).astype(int)
    return df

def _add_composite_health_score(df):
    df = df.copy()
    RUL_MAX   = 365.0
    TEMP_MAX  = 120.0
    VIB_MAX   = 20.0
    FLUID_MAX = 200.0
    ERROR_MAX = 30.0

    rul_norm   = 1 - (df["Remaining_Useful_Life_days"] / (RUL_MAX + 1e-9))
    temp_norm  = df["Temperature_C"] / (TEMP_MAX + 1e-9)
    vib_norm   = df["Vibration_mms"] / (VIB_MAX + 1e-9)
    fluid_norm = df["Fluid_Deficit_Score"] / (FLUID_MAX + 1e-9)
    error_norm = df["Error_Codes_Last_30_Days"] / (ERROR_MAX + 1e-9)

    df["Health_Risk_Score"] = (
        0.35 * rul_norm + 0.20 * fluid_norm + 0.20 * vib_norm +
        0.15 * temp_norm + 0.10 * error_norm
    ).clip(0, 1)
    return df

def _drop_redundant(df):
    df = df.copy()
    for col in ["Operational_Hours", "Installation_Year"]:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)
    return df

def _encode(df):
    df = df.copy()
    machine_type = df["Machine_Type"].iloc[0]
    # Normalise input to match training encoding format
    normalised = machine_type.strip().replace(" ", "_")
    df = df.drop(columns=["Machine_Type"])
    for col in MACHINE_TYPE_DUMMIES:
        type_name = col.replace("MachineType_", "")
        df[col] = int(normalised == type_name)
    bool_cols = df.select_dtypes(include="bool").columns.tolist()
    for col in bool_cols:
        df[col] = df[col].astype(int)
    return df

def engineer_features(data: SensorInput) -> pd.DataFrame:
    """Convert SensorInput into fully engineered feature DataFrame."""
    raw = {
        "Machine_Type":               data.machine_type,
        "Installation_Year":          data.installation_year,
        "Temperature_C":              data.temperature_c,
        "Vibration_mms":              data.vibration_mms,
        "Power_Consumption_kW":       data.power_consumption_kw,
        "Operational_Hours":          data.operational_hours,
        "Last_Maintenance_Days_Ago":  data.last_maintenance_days_ago,
        "Maintenance_History_Count":  data.maintenance_history_count,
        "Failure_History_Count":      data.failure_history_count,
        "Oil_Level_pct":              data.oil_level_pct,
        "Coolant_Level_pct":          data.coolant_level_pct,
        "AI_Supervision":             int(data.ai_supervision),
        "AI_Override_Events":         data.ai_override_events,
        "Remaining_Useful_Life_days": data.remaining_useful_life_days,
        "Error_Codes_Last_30_Days":   data.error_codes_last_30_days,
        "Sound_dB":                   data.sound_db,
    }

    df = pd.DataFrame([raw])
    df = _clean(df)
    df = _add_age_features(df)
    df = _add_maintenance_features(df)
    df = _add_sensor_features(df)
    df = _add_rul_features(df)
    df = _add_ai_features(df)
    df = _add_composite_health_score(df)
    df = _drop_redundant(df)
    df = _encode(df)

    cols_present = [c for c in COLS_TO_DROP if c in df.columns]
    df = df.drop(columns=cols_present)
    return df


def get_engineered_values(data: SensorInput) -> dict:
    """
    Returns the engineered feature values as a dict
    for use by the sensor diagnostics service.
    Called BEFORE dropping cols so we can check all features.
    """
    raw = {
        "Machine_Type":               data.machine_type,
        "Installation_Year":          data.installation_year,
        "Temperature_C":              data.temperature_c,
        "Vibration_mms":              data.vibration_mms,
        "Power_Consumption_kW":       data.power_consumption_kw,
        "Operational_Hours":          data.operational_hours,
        "Last_Maintenance_Days_Ago":  data.last_maintenance_days_ago,
        "Maintenance_History_Count":  data.maintenance_history_count,
        "Failure_History_Count":      data.failure_history_count,
        "Oil_Level_pct":              data.oil_level_pct,
        "Coolant_Level_pct":          data.coolant_level_pct,
        "AI_Supervision":             int(data.ai_supervision),
        "AI_Override_Events":         data.ai_override_events,
        "Remaining_Useful_Life_days": data.remaining_useful_life_days,
        "Error_Codes_Last_30_Days":   data.error_codes_last_30_days,
        "Sound_dB":                   data.sound_db,
    }
    df = pd.DataFrame([raw])
    df = _clean(df)
    df = _add_age_features(df)
    df = _add_maintenance_features(df)
    df = _add_sensor_features(df)
    df = _add_rul_features(df)
    df = _add_ai_features(df)
    df = _add_composite_health_score(df)
    df = _drop_redundant(df)
    return df.iloc[0].to_dict()