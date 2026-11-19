import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"
REPORTS_DIR = BASE_DIR / "reports"
IMAGES_DIR = BASE_DIR / "images"

for directory in [DATA_DIR, OUTPUTS_DIR, REPORTS_DIR, IMAGES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

SAMPLE_DATA_PATH = DATA_DIR / "sample_weather.json"
DB_PATH = DATA_DIR / "weather_cache.db"
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()

DEFAULT_THRESHOLDS = {
    "temp_c": float(os.getenv("TEMP_ALERT_THRESHOLD_C", 35.0)),
    "humidity_pct": float(os.getenv("HUMIDITY_ALERT_THRESHOLD_PCT", 80.0)),
    "rain_prob_pct": float(os.getenv("RAIN_PROB_ALERT_THRESHOLD_PCT", 60.0)),
    "wind_ms": float(os.getenv("WIND_ALERT_THRESHOLD_MS", 12.0)),
    "aqi": int(os.getenv("AQI_ALERT_THRESHOLD", 150)),
}
