"""
Sensor anomaly thresholds, recomputed from the healthy subset of
predictive_maintenance_v3.csv (n≈19.6k–20.5k per sensor, varies with
missing data). These replace the old thresholds, which were built on
composite/engineered features (Temperature_C, Thermal_Vibration_Index,
Hours_Per_Year) that no longer exist — the new model takes raw sensor
readings directly, so thresholds are computed on those raw columns.

Methodology (unchanged from before):
  Warning  = 5th-95th percentile of the healthy subset
  Critical = mean +/- 3*std of the healthy subset

For sensors that can't physically go negative (vibration, current,
pressure, rpm, hours since maintenance), a computed low bound below 0
is clamped to 0 rather than left negative — matching how
sensor_diagnostics.py already skips the low-side check whenever
crit_low <= 0.
"""

SENSOR_THRESHOLDS = {
    "vibration_rms": {
        "display_name": "Vibration (RMS)",
        "unit": "mm/s",
        "warn_low":  0.40,
        "warn_high": 3.11,
        "crit_low":  0.0,
        "crit_high": 4.23,
        "messages": {
            "crit_high": "Vibration critically high — likely bearing or mounting fault, inspect immediately",
            "warn_high": "Vibration elevated above normal range, monitor closely",
            "crit_low":  "Vibration critically low, machine may be stopped or sensor fault detected",
            "warn_low":  "Vibration below normal range, verify machine is running correctly",
        }
    },
    "temperature_motor": {
        "display_name": "Motor Temperature",
        "unit": "°C",
        "warn_low":  31.42,
        "warn_high": 67.42,
        "crit_low":  15.81,
        "crit_high": 82.97,
        "messages": {
            "crit_high": "Motor temperature critically high, risk of thermal damage — check cooling immediately",
            "warn_high": "Motor temperature elevated above normal range",
            "crit_low":  "Motor temperature critically low, verify sensor and machine status",
            "warn_low":  "Motor temperature below normal range",
        }
    },
    "current_phase_avg": {
        "display_name": "Phase Current (avg)",
        "unit": "A",
        "warn_low":  2.39,
        "warn_high": 15.98,
        "crit_low":  0.0,
        "crit_high": 23.61,
        "messages": {
            "crit_high": "Phase current critically high — possible electrical fault, inspect immediately",
            "warn_high": "Phase current elevated above normal range",
            "crit_low":  "Phase current critically low, machine may be idle or sensor fault detected",
            "warn_low":  "Phase current below normal range",
        }
    },
    "pressure_level": {
        "display_name": "Pressure Level",
        "unit": "psi",
        "warn_low":  16.10,
        "warn_high": 122.90,
        "crit_low":  0.0,
        "crit_high": 174.64,
        "messages": {
            "crit_high": "Pressure critically high — possible hydraulic fault, inspect immediately",
            "warn_high": "Pressure elevated above normal range",
            "crit_low":  "Pressure critically low, check for leaks or sensor fault",
            "warn_low":  "Pressure below normal range",
        }
    },
    "rpm": {
        "display_name": "Rotational Speed",
        "unit": "RPM",
        "warn_low":  151.10,
        "warn_high": 3004.78,
        "crit_low":  0.0,
        "crit_high": 3914.05,
        "messages": {
            "crit_high": "RPM critically high — verify load and control settings",
            "warn_high": "RPM elevated above normal range",
            "crit_low":  "RPM critically low, machine may be idle or stalled",
            "warn_low":  "RPM below normal range",
        }
    },
    "hours_since_maintenance": {
        "display_name": "Hours Since Maintenance",
        "unit": "hrs",
        "warn_low":  0.0,
        "warn_high": 440.60,
        "crit_low":  0.0,
        "crit_high": 602.93,
        "messages": {
            "crit_high": "Machine is significantly overdue for maintenance — schedule immediately",
            "warn_high": "Machine is approaching or past the normal maintenance interval",
            "crit_low":  "Hours since maintenance is unexpectedly low, verify log",
            "warn_low":  "Hours since maintenance is unexpectedly low, verify log",
        }
    },
    "ambient_temp": {
        "display_name": "Ambient Temperature",
        "unit": "°C",
        "warn_low":  8.50,
        "warn_high": 17.50,
        "crit_low":  4.34,
        "crit_high": 21.64,
        "messages": {
            "crit_high": "Ambient temperature critically high, may accelerate component wear",
            "warn_high": "Ambient temperature elevated above normal range",
            "crit_low":  "Ambient temperature critically low, verify environment and sensor",
            "warn_low":  "Ambient temperature below normal range",
        }
    },
}
