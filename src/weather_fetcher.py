import json
from datetime import datetime
import requests
from src.config import OPENWEATHER_API_KEY, SAMPLE_DATA_PATH


class WeatherFetchError(Exception):
    pass


def fetch_simulated_weather(city: str) -> dict:
    if not SAMPLE_DATA_PATH.exists():
        raise WeatherFetchError(f"Sample dataset not found at {SAMPLE_DATA_PATH}")

    with open(SAMPLE_DATA_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    city_map = {k.lower(): v for k, v in dataset.items()}
    key = city.strip().lower()

    if key not in city_map:
        available = ", ".join(dataset.keys())
        raise WeatherFetchError(f"City '{city}' not found in simulation dataset. Available: {available}")

    payload = city_map[key].copy()
    payload["source"] = "Virtual Simulation (sample_weather.json)"
    return payload


def fetch_open_meteo_live(city: str) -> dict:
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    try:
        geo_res = requests.get(geo_url, params={"name": city, "count": 1, "format": "json"}, timeout=10)
        geo_res.raise_for_status()
        geo_data = geo_res.json()
    except requests.RequestException as exc:
        raise WeatherFetchError(f"Geocoding request failed: {exc}") from exc

    results = geo_data.get("results")
    if not results:
        raise WeatherFetchError(f"City '{city}' could not be located via geocoding.")

    loc = results[0]
    lat, lon = loc["latitude"], loc["longitude"]
    resolved_name = loc.get("name", city)
    country = loc.get("country_code", "")

    forecast_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
        "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,wind_speed_10m",
        "wind_speed_unit": "ms",
        "forecast_days": 2,
        "timezone": "auto",
    }

    try:
        w_res = requests.get(forecast_url, params=params, timeout=10)
        w_res.raise_for_status()
        w_data = w_res.json()
    except requests.RequestException as exc:
        raise WeatherFetchError(f"Open-Meteo weather fetch failed: {exc}") from exc

    aqi_val = 50
    try:
        aqi_res = requests.get(
            "https://air-quality-api.open-meteo.com/v1/air-quality",
            params={"latitude": lat, "longitude": lon, "current": "us_aqi"},
            timeout=6,
        )
        if aqi_res.status_code == 200:
            aqi_val = aqi_res.json().get("current", {}).get("us_aqi") or 50
    except requests.RequestException:
        pass

    curr = w_data.get("current", {})
    hourly = w_data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    hums = hourly.get("relative_humidity_2m", [])
    probs = hourly.get("precipitation_probability", [])
    winds = hourly.get("wind_speed_10m", [])

    forecast_list = []
    for idx in range(0, min(24, len(times)), 3):
        prob = float(probs[idx] or 0.0)
        cond = "Rain Likely" if prob >= 60 else ("Cloudy" if prob >= 30 else "Clear / Fair")
        forecast_list.append(
            {
                "timestamp": times[idx].replace("T", " "),
                "temp_c": float(temps[idx]),
                "humidity": int(hums[idx]),
                "wind_speed_ms": float(winds[idx]),
                "rain_prob_pct": prob,
                "condition": cond,
            }
        )

    curr_rain_prob = forecast_list[0]["rain_prob_pct"] if forecast_list else 0.0

    return {
        "city": resolved_name,
        "country": country,
        "lat": lat,
        "lon": lon,
        "source": "Open-Meteo Live API (No-Key)",
        "current": {
            "timestamp": curr.get("time", datetime.now().isoformat()).replace("T", " "),
            "temp_c": float(curr.get("temperature_2m", 0.0)),
            "feels_like_c": float(curr.get("apparent_temperature", 0.0)),
            "humidity": int(curr.get("relative_humidity_2m", 0)),
            "wind_speed_ms": float(curr.get("wind_speed_10m", 0.0)),
            "weather_main": "Rain" if curr_rain_prob >= 60 else "Clear",
            "weather_desc": "live meteorological observation",
            "rain_prob_pct": curr_rain_prob,
            "aqi": int(aqi_val),
        },
        "forecast": forecast_list,
    }


def fetch_openweathermap_live(city: str) -> dict:
    base_url = "https://api.openweathermap.org/data/2.5"
    try:
        curr_res = requests.get(
            f"{base_url}/weather",
            params={"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"},
            timeout=10,
        )
        if curr_res.status_code == 401:
            raise WeatherFetchError("Invalid OpenWeatherMap API Key (HTTP 401).")
        if curr_res.status_code == 404:
            raise WeatherFetchError(f"City '{city}' not found on OpenWeatherMap (HTTP 404).")
        curr_res.raise_for_status()
        curr_data = curr_res.json()

        fore_res = requests.get(
            f"{base_url}/forecast",
            params={"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric", "cnt": 8},
            timeout=10,
        )
        fore_res.raise_for_status()
        fore_data = fore_res.json()
    except requests.RequestException as exc:
        raise WeatherFetchError(f"Network error contacting OpenWeatherMap: {exc}") from exc

    coord = curr_data.get("coord", {})
    lat, lon = coord.get("lat", 0.0), coord.get("lon", 0.0)

    aqi_val = 50
    try:
        aqi_res = requests.get(
            f"{base_url}/air_pollution",
            params={"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY},
            timeout=6,
        )
        if aqi_res.status_code == 200:
            owm_aqi = aqi_res.json().get("list", [{}])[0].get("main", {}).get("aqi", 1)
            aqi_map = {1: 35, 2: 75, 3: 125, 4: 175, 5: 250}
            aqi_val = aqi_map.get(owm_aqi, 50)
    except requests.RequestException:
        pass

    forecast_list = []
    for item in fore_data.get("list", []):
        forecast_list.append(
            {
                "timestamp": item.get("dt_txt", ""),
                "temp_c": float(item["main"]["temp"]),
                "humidity": int(item["main"]["humidity"]),
                "wind_speed_ms": float(item["wind"]["speed"]),
                "rain_prob_pct": round(float(item.get("pop", 0.0)) * 100, 1),
                "condition": item["weather"][0]["description"].title(),
            }
        )

    first_pop = forecast_list[0]["rain_prob_pct"] if forecast_list else 0.0

    return {
        "city": curr_data.get("name", city),
        "country": curr_data.get("sys", {}).get("country", ""),
        "lat": lat,
        "lon": lon,
        "source": "OpenWeatherMap Live API",
        "current": {
            "timestamp": datetime.fromtimestamp(curr_data["dt"]).strftime("%Y-%m-%d %H:%M:%S"),
            "temp_c": float(curr_data["main"]["temp"]),
            "feels_like_c": float(curr_data["main"]["feels_like"]),
            "humidity": int(curr_data["main"]["humidity"]),
            "wind_speed_ms": float(curr_data["wind"]["speed"]),
            "weather_main": curr_data["weather"][0]["main"],
            "weather_desc": curr_data["weather"][0]["description"],
            "rain_prob_pct": first_pop,
            "aqi": aqi_val,
        },
        "forecast": forecast_list,
    }


def get_weather_data(city: str, mode: str = "auto") -> dict:
    mode = mode.lower().strip()
    if mode == "simulation":
        return fetch_simulated_weather(city)
    if mode == "live":
        if OPENWEATHER_API_KEY and OPENWEATHER_API_KEY != "your_openweathermap_api_key_here":
            return fetch_openweathermap_live(city)
        return fetch_open_meteo_live(city)
    try:
        if OPENWEATHER_API_KEY and OPENWEATHER_API_KEY != "your_openweathermap_api_key_here":
            return fetch_openweathermap_live(city)
        return fetch_open_meteo_live(city)
    except WeatherFetchError:
        return fetch_simulated_weather(city)
