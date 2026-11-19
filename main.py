import argparse
import sys
from src.weather_fetcher import get_weather_data, WeatherFetchError
from src.data_processor import (
    save_observation_to_db,
    build_forecast_dataframe,
    compute_forecast_summary,
)
from src.alert_engine import evaluate_weather_alerts
from src.visualizer import generate_forecast_chart
from src.report_generator import save_reports


def run_pipeline(city: str, mode: str = "auto") -> None:
    print(f"\nFetching weather intelligence for '{city}' [Mode: {mode.upper()}]...")
    try:
        payload = get_weather_data(city, mode=mode)
    except WeatherFetchError as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)

    save_observation_to_db(payload)
    forecast_df = build_forecast_dataframe(payload)
    summary = compute_forecast_summary(forecast_df)
    alerts = evaluate_weather_alerts(payload, forecast_df)

    chart_path = generate_forecast_chart(payload["city"], forecast_df)
    report_paths = save_reports(payload, forecast_df, summary, alerts)

    curr = payload["current"]
    print("\n" + "=" * 60)
    print(f"WEATHER REPORT: {payload['city'].upper()}, {payload.get('country', '')}")
    print(f"Source: {payload.get('source')}")
    print("=" * 60)
    print(f"Temperature : {curr['temp_c']}°C (Feels like {curr['feels_like_c']}°C)")
    print(f"Humidity    : {curr['humidity']}%")
    print(f"Wind Speed  : {curr['wind_speed_ms']} m/s")
    print(f"Rain Prob   : {curr['rain_prob_pct']}%")
    print(f"Air Quality : US AQI {curr.get('aqi', 'N/A')}")
    print(f"Condition   : {curr['weather_desc'].title()}")

    print("\n--- 24-HOUR FORECAST SUMMARY ---")
    print(
        f"Temp Range: {summary['min_temp_c']}°C - {summary['max_temp_c']}°C | "
        f"Avg Humidity: {summary['avg_humidity_pct']}% | "
        f"Peak Rain Prob: {summary['max_rain_prob_pct']}%"
    )

    print("\n--- ACTIVE WEATHER ALERTS ---")
    for alert in alerts:
        print(f"[{alert['severity']}] {alert['type']}: {alert['message']}")
        print(f"   -> Action: {alert['action']}")

    print("\n--- GENERATED ARTIFACTS ---")
    print(f"Chart Saved : {chart_path}")
    print(f"CSV Report  : {report_paths['csv_report']}")
    print(f"TXT Report  : {report_paths['txt_report']}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weather Forecast & Alert CLI Application")
    parser.add_argument("--city", type=str, help="Target city name (e.g., Mumbai, Delhi, London)")
    parser.add_argument("--mode", type=str, default="auto", choices=["auto", "live", "simulation"])
    args = parser.parse_args()

    target_city = args.city or input("Enter city name (e.g., Mumbai, Delhi, London, Tokyo): ").strip()
    if not target_city:
        target_city = "Mumbai"

    run_pipeline(city=target_city, mode=args.mode)
