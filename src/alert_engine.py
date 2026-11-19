from typing import Dict, List
import pandas as pd
from src.config import DEFAULT_THRESHOLDS


def evaluate_weather_alerts(
    payload: dict,
    forecast_df: pd.DataFrame,
    thresholds: Dict[str, float] | None = None,
) -> List[dict]:
    rules = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    curr = payload["current"]
    city = payload["city"]

    peak_temp = max(curr["temp_c"], float(forecast_df["temp_c"].max()) if not forecast_df.empty else curr["temp_c"])
    peak_humidity = max(curr["humidity"], int(forecast_df["humidity"].max()) if not forecast_df.empty else curr["humidity"])
    peak_rain_prob = max(curr["rain_prob_pct"], float(forecast_df["rain_prob_pct"].max()) if not forecast_df.empty else curr["rain_prob_pct"])
    peak_wind = max(curr["wind_speed_ms"], float(forecast_df["wind_speed_ms"].max()) if not forecast_df.empty else curr["wind_speed_ms"])
    current_aqi = int(curr.get("aqi", 50))

    alerts = []

    if peak_temp >= rules["temp_c"]:
        severity = "CRITICAL" if peak_temp >= rules["temp_c"] + 5 else "WARNING"
        alerts.append({
            "code": "HIGH_TEMP",
            "type": "Heat Advisory",
            "severity": severity,
            "metric_value": f"{peak_temp:.1f}°C",
            "threshold": f"{rules['temp_c']}°C",
            "message": f"High temperature of {peak_temp:.1f}°C expected in {city}.",
            "action": "Stay hydrated, avoid peak afternoon sun, and monitor cooling systems.",
        })

    if peak_rain_prob >= rules["rain_prob_pct"]:
        severity = "CRITICAL" if peak_rain_prob >= 80 else "WARNING"
        alerts.append({
            "code": "RAIN_RISK",
            "type": "Precipitation & Storm Alert",
            "severity": severity,
            "metric_value": f"{peak_rain_prob:.0f}%",
            "threshold": f"{rules['rain_prob_pct']:.0f}%",
            "message": f"High rain probability ({peak_rain_prob:.0f}%) forecasted for {city}.",
            "action": "Carry rain gear, delay outdoor events, and adjust logistics routes.",
        })

    if peak_humidity >= rules["humidity_pct"]:
        alerts.append({
            "code": "HIGH_HUMIDITY",
            "type": "High Humidity Warning",
            "severity": "WARNING",
            "metric_value": f"{peak_humidity}%",
            "threshold": f"{rules['humidity_pct']:.0f}%",
            "message": f"Elevated humidity reaching {peak_humidity}% in {city}.",
            "action": "Protect moisture-sensitive goods and watch for heat-index discomfort.",
        })

    if peak_wind >= rules["wind_ms"]:
        severity = "CRITICAL" if peak_wind >= 15.0 else "WARNING"
        alerts.append({
            "code": "HIGH_WIND",
            "type": "Strong Wind Advisory",
            "severity": severity,
            "metric_value": f"{peak_wind:.1f} m/s",
            "threshold": f"{rules['wind_ms']} m/s",
            "message": f"Strong wind speeds up to {peak_wind:.1f} m/s expected in {city}.",
            "action": "Secure loose outdoor equipment and exercise caution during transit.",
        })

    if current_aqi >= rules["aqi"]:
        severity = "CRITICAL" if current_aqi >= 200 else "WARNING"
        alerts.append({
            "code": "POOR_AQI",
            "type": "Air Quality Alert",
            "severity": severity,
            "metric_value": f"AQI {current_aqi}",
            "threshold": f"AQI {rules['aqi']}",
            "message": f"Unhealthy air quality detected in {city} (US AQI: {current_aqi}).",
            "action": "Wear N95 masks outdoors and limit prolonged outdoor exertion.",
        })

    if not alerts:
        alerts.append({
            "code": "ALL_CLEAR",
            "type": "Normal Weather",
            "severity": "INFO",
            "metric_value": "Optimal",
            "threshold": "Within Limits",
            "message": f"Weather conditions in {city} are stable and within safe thresholds.",
            "action": "No weather disruptions expected. Safe for normal operations.",
        })

    return alerts
