"""
Test the API with real values from the training dataset.
Run: python scripts/test_api.py
Make sure the server is running: uvicorn app.main:app --reload
"""
import requests
import json

BASE = "http://localhost:8000/api/v1"


def test_health():
    r = requests.get(f"{BASE}/health")
    print("Health:", json.dumps(r.json(), indent=2))


def test_machine_types():
    r = requests.get(f"{BASE}/machines/types")
    print("\nMachine Types:", r.json())


def test_healthy_machine():
    """Normal machine readings — should return HEALTHY with no sensor alerts"""
    payload = {
        "machine_id": "MCH-HEALTHY-001",
        "machine_type": "Pump",
        "installation_year": 2018,
        "temperature_c": 63.07,
        "vibration_mms": 2.1,
        "power_consumption_kw": 120.0,
        "operational_hours": 14500,
        "last_maintenance_days_ago": 45,
        "maintenance_history_count": 8,
        "failure_history_count": 1,
        "oil_level_pct": 75.0,
        "coolant_level_pct": 80.0,
        "ai_supervision": False,
        "ai_override_events": 0,
        "remaining_useful_life_days": 200.0,
        "error_codes_last_30_days": 2,
        "sound_db": 68.5,
    }
    r = requests.post(f"{BASE}/predict", json=payload)
    print("\nHealthy Machine Result:")
    print(json.dumps(r.json(), indent=2))


def test_faulty_machine():
    """
    Machine with critically high temperature and vibration.
    Temperature = 108.5°C (critical threshold = 105.06°C)
    Thermal_Vibration_Index = 108.5 * 14.2 = 1540.7 (warning threshold = 1202.82)
    Should return AT_RISK/CRITICAL with sensor alerts.
    """
    payload = {
        "machine_id": "MCH-FAULTY-001",
        "machine_type": "CNC Lathe",
        "installation_year": 2010,
        "temperature_c": 108.5,
        "vibration_mms": 14.2,
        "power_consumption_kw": 380.0,
        "operational_hours": 65000,
        "last_maintenance_days_ago": 320,
        "maintenance_history_count": 3,
        "failure_history_count": 7,
        "oil_level_pct": 12.0,
        "coolant_level_pct": 15.0,
        "ai_supervision": True,
        "ai_override_events": 8,
        "remaining_useful_life_days": 15.0,
        "error_codes_last_30_days": 11,
        "sound_db": 107.0,
    }
    r = requests.post(f"{BASE}/predict", json=payload)
    print("\nFaulty Machine Result:")
    print(json.dumps(r.json(), indent=2))


if __name__ == "__main__":
    test_health()
    test_machine_types()
    test_healthy_machine()
    test_faulty_machine()