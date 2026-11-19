from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from src.weather_fetcher import get_weather_data, WeatherFetchError
from src.data_processor import (
    save_observation_to_db,
    build_forecast_dataframe,
    compute_forecast_summary,
    get_recent_logs,
)
from src.alert_engine import evaluate_weather_alerts

app = FastAPI(
    title="Weather Forecast & Alert API",
    description="Real-time & simulated meteorological ingestion, risk rule evaluation, and reporting API.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Weather Forecast & Alert API"}


@app.get("/weather/{city}")
def get_city_weather(
    city: str,
    mode: str = Query("auto", description="Ingestion mode: 'auto', 'live', or 'simulation'"),
    temp_limit: Optional[float] = Query(None, description="Custom max temperature threshold (°C)"),
    rain_limit: Optional[float] = Query(None, description="Custom rain probability threshold (%)"),
):
    try:
        payload = get_weather_data(city, mode=mode)
    except WeatherFetchError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    save_observation_to_db(payload)
    forecast_df = build_forecast_dataframe(payload)
    summary = compute_forecast_summary(forecast_df)

    custom_thresholds = {}
    if temp_limit is not None:
        custom_thresholds["temp_c"] = temp_limit
    if rain_limit is not None:
        custom_thresholds["rain_prob_pct"] = rain_limit

    alerts = evaluate_weather_alerts(payload, forecast_df, thresholds=custom_thresholds)

    return {
        "city": payload["city"],
        "country": payload.get("country", ""),
        "coordinates": {"lat": payload.get("lat"), "lon": payload.get("lon")},
        "source": payload.get("source"),
        "current": payload["current"],
        "forecast_summary": summary,
        "alerts": alerts,
        "forecast": payload["forecast"],
    }


@app.get("/logs")
def fetch_historical_logs(limit: int = Query(15, ge=1, le=100)):
    df = get_recent_logs(limit=limit)
    return {"count": len(df), "logs": df.to_dict(orient="records")}
