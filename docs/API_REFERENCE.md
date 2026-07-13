# MachineGuard API Reference

## Base URL
- Local: `http://localhost:8000`
- Production: `https://machineguard-api.onrender.com`

## Endpoints

### GET /api/v1/health
Returns API and model status.

### POST /api/v1/predict
Submit sensor readings, get a failure prediction.

**Request body:** SensorInput (see schemas/prediction.py)

**Response:**
```json
{
  "machine_id": "MCH-001",
  "prediction": 1,
  "risk_probability": 0.83,
  "risk_percentage": 83.0,
  "risk_level": "CRITICAL",
  "recommendation": "CRITICAL: Immediate inspection required.",
  "model_version": "1.0.0"
}
```

### GET /api/v1/machines/types
Returns supported machine types.

## Risk Levels
| Level    | Threshold       | Action                  |
|----------|----------------|-------------------------|
| HEALTHY  | < 50%          | Normal monitoring        |
| AT_RISK  | 50% – 74%      | Schedule maintenance     |
| CRITICAL | >= 75%         | Immediate inspection     |

## Setup
1. Copy `.env.example` to `.env`
2. Place `cat_model.joblib` in `/artifacts`
3. `pip install -r requirements.txt`
4. `uvicorn app.main:app --reload`
