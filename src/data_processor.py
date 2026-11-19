import sqlite3
from datetime import datetime
import pandas as pd
from src.config import DB_PATH


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS weather_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                logged_at TEXT NOT NULL,
                city TEXT NOT NULL,
                country TEXT,
                source TEXT,
                temp_c REAL,
                humidity INTEGER,
                wind_speed_ms REAL,
                rain_prob_pct REAL,
                aqi INTEGER,
                condition TEXT
            )
            """
        )
        conn.commit()


def save_observation_to_db(payload: dict) -> None:
    init_db()
    curr = payload["current"]
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO weather_logs
            (logged_at, city, country, source, temp_c, humidity, wind_speed_ms, rain_prob_pct, aqi, condition)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                payload["city"],
                payload.get("country", ""),
                payload.get("source", ""),
                curr["temp_c"],
                curr["humidity"],
                curr["wind_speed_ms"],
                curr["rain_prob_pct"],
                curr.get("aqi", 50),
                curr["weather_desc"],
            ),
        )
        conn.commit()


def get_recent_logs(limit: int = 20) -> pd.DataFrame:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(f"SELECT * FROM weather_logs ORDER BY id DESC LIMIT {int(limit)}", conn)


def build_forecast_dataframe(payload: dict) -> pd.DataFrame:
    df = pd.DataFrame(payload.get("forecast", []))
    if df.empty:
        return df
    df["city"] = payload["city"]
    return df


def compute_forecast_summary(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "min_temp_c": 0.0,
            "max_temp_c": 0.0,
            "avg_temp_c": 0.0,
            "avg_humidity_pct": 0.0,
            "max_rain_prob_pct": 0.0,
            "max_wind_ms": 0.0,
        }
    return {
        "min_temp_c": round(float(df["temp_c"].min()), 1),
        "max_temp_c": round(float(df["temp_c"].max()), 1),
        "avg_temp_c": round(float(df["temp_c"].mean()), 1),
        "avg_humidity_pct": round(float(df["humidity"].mean()), 1),
        "max_rain_prob_pct": round(float(df["rain_prob_pct"].max()), 1),
        "max_wind_ms": round(float(df["wind_speed_ms"].max()), 1),
    }
