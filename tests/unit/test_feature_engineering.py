import pytest
from app.schemas.prediction import SensorInput
from app.services.feature_engineering import engineer_features

SAMPLE_INPUT = SensorInput(
    machine_id="TEST-001",
    machine_type="Compressor",
    installation_year=2018,
    temperature_c=75.0,
    vibration_mms=3.5,
    power_consumption_kw=12.0,
    operational_hours=14000,
    days_since_last_maintenance=45,
    maintenance_count=8,
    oil_level_pct=72.0,
    coolant_level_pct=85.0,
    ai_supervision=True,
    remaining_useful_life_days=120.0,
)

def test_engineer_features_returns_dataframe():
    df = engineer_features(SAMPLE_INPUT)
    assert df is not None
    assert len(df) == 1

def test_machine_age_computed():
    df = engineer_features(SAMPLE_INPUT)
    assert "Machine_Age" in df.columns
    assert df["Machine_Age"].iloc[0] == 2026 - 2018

def test_machine_type_one_hot_encoded():
    df = engineer_features(SAMPLE_INPUT)
    assert "Machine_Type_Compressor" in df.columns
    assert df["Machine_Type_Compressor"].iloc[0] == 1

def test_negative_sensor_values_rejected():
    with pytest.raises(Exception):
        SensorInput(**{**SAMPLE_INPUT.dict(), "temperature_c": -10})
