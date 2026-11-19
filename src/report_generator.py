from datetime import datetime
from typing import List
import pandas as pd
from src.config import REPORTS_DIR


def save_reports(payload: dict, forecast_df: pd.DataFrame, summary: dict, alerts: List[dict]) -> dict:
    safe_city = payload["city"].lower().replace(" ", "_")
    timestamp_tag = datetime.now().strftime("%Y%m%d_%H%M%S")

    csv_path = REPORTS_DIR / f"{safe_city}_forecast_{timestamp_tag}.csv"
    txt_path = REPORTS_DIR / f"{safe_city}_alert_report_{timestamp_tag}.txt"

    if not forecast_df.empty:
        forecast_df.to_csv(csv_path, index=False)

    curr = payload["current"]
    lines = [
        "=" * 65,
        f"WEATHER FORECAST & RISK ALERT REPORT — {payload['city'].upper()} ({payload.get('country', '')})",
        "=" * 65,
        f"Generated At : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Data Source  : {payload.get('source', 'N/A')}",
        f"Coordinates  : Lat {payload.get('lat')}, Lon {payload.get('lon')}",
        "-" * 65,
        "1. CURRENT OBSERVATION",
        f"   Temperature  : {curr['temp_c']}°C (Feels like {curr['feels_like_c']}°C)",
        f"   Humidity     : {curr['humidity']}%",
        f"   Wind Speed   : {curr['wind_speed_ms']} m/s",
        f"   Rain Prob    : {curr['rain_prob_pct']}%",
        f"   Air Quality  : US AQI {curr.get('aqi', 'N/A')}",
        f"   Condition    : {curr['weather_desc'].title()}",
        "-" * 65,
        "2. FORECAST SUMMARY (24-HOUR OUTLOOK)",
        f"   Temp Range   : {summary['min_temp_c']}°C to {summary['max_temp_c']}°C (Avg: {summary['avg_temp_c']}°C)",
        f"   Avg Humidity : {summary['avg_humidity_pct']}%",
        f"   Peak Rain    : {summary['max_rain_prob_pct']}%",
        f"   Peak Wind    : {summary['max_wind_ms']} m/s",
        "-" * 65,
        "3. AUTOMATED RISK ALERTS & RECOMMENDATIONS",
    ]

    for idx, alert in enumerate(alerts, start=1):
        lines.append(f"   [{alert['severity']}] {idx}. {alert['type']} ({alert['metric_value']} vs limit {alert['threshold']})")
        lines.append(f"       Detail : {alert['message']}")
        lines.append(f"       Action : {alert['action']}")

    lines.append("=" * 65)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return {"csv_report": str(csv_path), "txt_report": str(txt_path)}
