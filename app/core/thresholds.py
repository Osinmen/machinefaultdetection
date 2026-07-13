# app/core/thresholds.py — CREATE THIS FILE

"""
Sensor anomaly thresholds derived from healthy subset (n=49,382).

Only 3 features are used for alerts — these are the only features
that show statistically meaningful differences between healthy and
faulty machines in the training data:

  - Temperature_C           (+2.8% higher in faulty machines)
  - Thermal_Vibration_Index (+10.4% higher in faulty machines)
  - Hours_Per_Year          (+100.9% higher in faulty machines)

Methodology:
  Warning  = 5th-95th percentile of healthy subset (Malpani 2019, IJERA 9(9))
  Critical = mean +/- 3*std of healthy subset (Li et al. 2026, Eksploatacja 28(3))
"""

SENSOR_THRESHOLDS = {
    "Temperature_C": {
        "display_name": "Temperature",
        "unit": "°C",
        "warn_low":  35.52,
        "warn_high": 84.73,
        "crit_low":  14.84,
        "crit_high": 105.06,
        "messages": {
            "crit_high": "Temperature critically high, immediate risk of thermal damage and component failure",
            "warn_high": "Temperature elevated above normal range, check cooling system",
            "crit_low":  "Temperature critically low, machine may be stopped or sensor fault detected",
            "warn_low":  "Temperature below normal range, verify machine is running correctly",
        }
    },
    "Thermal_Vibration_Index": {
        "display_name": "Thermal-Vibration Stress",
        "unit": "index",
        "warn_low":  88.44,
        "warn_high": 1202.82,
        "crit_low":  0.0,
        "crit_high": 1608.39,
        "messages": {
            "crit_high": "Combined thermal and vibration stress critically high — inspect immediately",
            "warn_high": "Thermal-vibration stress elevated temperature and vibration interaction is abnormal",
            "crit_low":  "Thermal-vibration index critically low machine may not be operating",
            "warn_low":  "Thermal-vibration index below normal range",
        }
    },
    "Hours_Per_Year": {
        "display_name": "Usage Intensity",
        "unit": "hrs/year",
        "warn_low":  337.63,
        "warn_high": 26004.22,
        "crit_low":  0.0,
        "crit_high": 41240.57,
        "messages": {
            "crit_high": "Machine usage critically high — running far beyond normal annual hours, failure risk elevated",
            "warn_high": "Machine usage intensity high — monitor closely for wear",
            "crit_low":  "Machine usage extremely low — verify operational status",
            "warn_low":  "Machine usage below normal range",
        }
    },
}