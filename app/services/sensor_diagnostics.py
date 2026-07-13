"""
Rule-based sensor diagnostics.
Runs independently of the ML model.

Checks 3 engineered features that show statistically meaningful
differences between healthy and faulty machines in training data.
"""

from typing import List, Dict, Any
from app.core.threshold import SENSOR_THRESHOLDS


def _check_sensor(feature_name: str, value: float) -> Dict[str, Any] | None:
    if feature_name not in SENSOR_THRESHOLDS:
        return None
    t = SENSOR_THRESHOLDS[feature_name]

    if value > t["crit_high"]:
        status, message = "CRITICAL", t["messages"]["crit_high"]
    elif value < t["crit_low"] and t["crit_low"] > 0:
        status, message = "CRITICAL", t["messages"]["crit_low"]
    elif value > t["warn_high"]:
        status, message = "WARNING", t["messages"]["warn_high"]
    elif value < t["warn_low"] and t["warn_low"] > 0:
        status, message = "WARNING", t["messages"]["warn_low"]
    else:
        return None

    return {
        "sensor":      t["display_name"],
        "feature_key": feature_name,
        "value":       round(float(value), 3),
        "unit":        t["unit"],
        "status":      status,
        "message":     message,
        "warn_range":  [t["warn_low"], t["warn_high"]],
        "crit_range":  [t["crit_low"], t["crit_high"]],
    }


def run_sensor_diagnostics(engineered_values: Dict[str, float]) -> Dict[str, Any]:
    """
    Check engineered feature values against thresholds.
    Returns alerts list and counts.
    """
    alerts: List[Dict] = []

    for feature_name in SENSOR_THRESHOLDS:
        if feature_name in engineered_values:
            alert = _check_sensor(feature_name, engineered_values[feature_name])
            if alert:
                alerts.append(alert)

    # CRITICAL first
    alerts.sort(key=lambda a: 0 if a["status"] == "CRITICAL" else 1)

    return {
        "sensor_alerts":  alerts,
        "alert_count":    len(alerts),
        "critical_count": sum(1 for a in alerts if a["status"] == "CRITICAL"),
        "warning_count":  sum(1 for a in alerts if a["status"] == "WARNING"),
    }