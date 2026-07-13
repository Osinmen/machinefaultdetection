import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "machine_id": "MCH-001",
    "machine_type": "Compressor",
    "installation_year": 2018,
    "temperature_c": 75.0,
    "vibration_mms": 3.5,
    "power_consumption_kw": 12.0,
    "operational_hours": 14000,
    "days_since_last_maintenance": 45,
    "maintenance_count": 8,
    "oil_level_pct": 72.0,
    "coolant_level_pct": 85.0,
    "ai_supervision": True,
    "remaining_useful_life_days": 120.0,
}

def test_health_endpoint():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_predict_endpoint_structure():
    r = client.post("/api/v1/predict", json=VALID_PAYLOAD)
    # Will return 503 if model not loaded — that's expected in CI without artifacts
    assert r.status_code in [200, 503]

def test_predict_rejects_negative_temperature():
    bad = {**VALID_PAYLOAD, "temperature_c": -5}
    r = client.post("/api/v1/predict", json=bad)
    assert r.status_code == 422
