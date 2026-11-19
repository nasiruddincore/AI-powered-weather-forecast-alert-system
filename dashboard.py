import pandas as pd
import pydeck as pdk
import streamlit as st
from src.config import DEFAULT_THRESHOLDS
from src.weather_fetcher import get_weather_data, WeatherFetchError
from src.data_processor import (
    save_observation_to_db,
    build_forecast_dataframe,
    compute_forecast_summary,
    get_recent_logs,
)
from src.alert_engine import evaluate_weather_alerts
from src.visualizer import generate_forecast_chart
from src.report_generator import save_reports

st.set_page_config(
    page_title="Weather Forecast & Alert System",
    page_icon="🌦️",
    layout="wide",
)

# Custom Vibrant CSS Styling
st.markdown(
    """
    <style>
    /* Vibrant App Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 45%, #0f172a 100%);
        color: #f8fafc;
    }
    /* Sidebar Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #312e81 50%, #1e293b 100%);
        border-right: 1px solid rgba(129, 140, 248, 0.3);
    }
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(90deg, #2563eb 0%, #7c3aed 50%, #db2777 100%);
        padding: 24px 30px;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.35);
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #e0e7ff;
        margin-top: 6px;
        margin-bottom: 0;
    }
    /* Location Status Pill */
    .status-pill {
        background: linear-gradient(90deg, rgba(14, 165, 233, 0.22), rgba(168, 85, 247, 0.22));
        border: 1px solid rgba(56, 189, 248, 0.45);
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 22px;
        color: #e0f2fe;
        font-size: 0.95rem;
    }
    /* Colorful KPI Cards */
    .kpi-card {
        border-radius: 16px;
        padding: 18px 20px;
        color: white;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.22);
        transition: transform 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
    }
    .kpi-label {
        font-size: 0.88rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        opacity: 0.92;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        margin: 6px 0;
    }
    .kpi-sub {
        font-size: 0.82rem;
        background: rgba(255, 255, 255, 0.2);
        padding: 3px 10px;
        border-radius: 20px;
        display: inline-block;
    }
    .card-temp { background: linear-gradient(135deg, #f97316 0%, #e11d48 100%); }
    .card-hum  { background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); }
    .card-rain { background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%); }
    .card-wind { background: linear-gradient(135deg, #059669 0%, #0d9488 100%); }
    .card-aqi  { background: linear-gradient(135deg, #d97706 0%, #b45309 100%); }

    /* Section Headers */
    .section-header {
        font-size: 1.35rem;
        font-weight: 700;
        background: linear-gradient(90deg, #38bdf8, #c084fc, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 22px;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Colorful Hero Header
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-title">🌦️ Weather Forecast & Automated Risk Alert System</div>
        <div class="hero-subtitle">Real-Time Meteorological Intelligence • Smart Threshold Alerts • Colorful Geospatial Mapping & Analytics</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar Controls
st.sidebar.markdown("## ⚙️ Control Panel")
mode = st.sidebar.selectbox(
    "Data Ingestion Mode",
    options=["auto", "simulation", "live"],
    index=0,
    help="'auto' uses Live API with offline simulation fallback; 'simulation' uses sample_weather.json.",
)

if mode == "simulation":
    city = st.sidebar.selectbox("Select Simulated City", ["Mumbai", "Delhi", "London", "Tokyo"])
else:
    city = st.sidebar.text_input("Enter City Name", value="Mumbai")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚨 Alert Thresholds")
temp_thresh = st.sidebar.slider("🌡️ Max Temperature (°C)", 20.0, 50.0, float(DEFAULT_THRESHOLDS["temp_c"]), 0.5)
rain_thresh = st.sidebar.slider("🌧️ Rain Probability (%)", 10.0, 100.0, float(DEFAULT_THRESHOLDS["rain_prob_pct"]), 5.0)
hum_thresh = st.sidebar.slider("💧 Max Humidity (%)", 30.0, 100.0, float(DEFAULT_THRESHOLDS["humidity_pct"]), 5.0)
wind_thresh = st.sidebar.slider("💨 Max Wind Speed (m/s)", 2.0, 30.0, float(DEFAULT_THRESHOLDS["wind_ms"]), 0.5)
aqi_thresh = st.sidebar.slider("😷 Max Air Quality Index (AQI)", 50, 400, int(DEFAULT_THRESHOLDS["aqi"]), 10)

custom_thresholds = {
    "temp_c": temp_thresh,
    "rain_prob_pct": rain_thresh,
    "humidity_pct": hum_thresh,
    "wind_ms": wind_thresh,
    "aqi": aqi_thresh,
}

if st.sidebar.button("🔄 Refresh & Generate Reports", use_container_width=True):
    st.rerun()

# Fetch & Process Data
try:
    payload = get_weather_data(city, mode=mode)
    save_observation_to_db(payload)
    forecast_df = build_forecast_dataframe(payload)
    summary = compute_forecast_summary(forecast_df)
    alerts = evaluate_weather_alerts(payload, forecast_df, thresholds=custom_thresholds)
    chart_path = generate_forecast_chart(payload["city"], forecast_df)
    report_paths = save_reports(payload, forecast_df, summary, alerts)
except WeatherFetchError as err:
    st.error(f"❌ {err}")
    st.stop()

curr = payload["current"]

# Location Status Banner
st.markdown(
    f"""
    <div class="status-pill">
        📍 <b>Location:</b> {payload['city']}, {payload.get('country', '')} &nbsp;|&nbsp;
        🛰️ <b>Source:</b> {payload.get('source')} &nbsp;|&nbsp;
        🕒 <b>Observed:</b> {curr['timestamp']} &nbsp;|&nbsp;
        🌤️ <b>Condition:</b> {curr['weather_desc'].title()}
    </div>
    """,
    unsafe_allow_html=True,
)

# 5 Colorful Gradient KPI Cards
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(
        f"""
        <div class="kpi-card card-temp">
            <div class="kpi-label">🌡️ Temperature</div>
            <div class="kpi-value">{curr['temp_c']} °C</div>
            <div class="kpi-sub">Feels like {curr['feels_like_c']} °C</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class="kpi-card card-hum">
            <div class="kpi-label">💧 Humidity</div>
            <div class="kpi-value">{curr['humidity']} %</div>
            <div class="kpi-sub">Avg 24h: {summary['avg_humidity_pct']}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
        <div class="kpi-card card-rain">
            <div class="kpi-label">🌧️ Rain Prob</div>
            <div class="kpi-value">{curr['rain_prob_pct']} %</div>
            <div class="kpi-sub">Peak 24h: {summary['max_rain_prob_pct']}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        f"""
        <div class="kpi-card card-wind">
            <div class="kpi-label">💨 Wind Speed</div>
            <div class="kpi-value">{curr['wind_speed_ms']} m/s</div>
            <div class="kpi-sub">Peak 24h: {summary['max_wind_ms']} m/s</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c5:
    st.markdown(
        f"""
        <div class="kpi-card card-aqi">
            <div class="kpi-label">😷 Air Quality</div>
            <div class="kpi-value">AQI {curr.get('aqi', 50)}</div>
            <div class="kpi-sub">Limit: {aqi_thresh}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Automated Risk Alerts Section
st.markdown('<div class="section-header">🚨 Automated Risk Alerts & Advisories</div>', unsafe_allow_html=True)
for alert in alerts:
    sev = alert["severity"]
    text = f"**{alert['type']}** ({alert['metric_value']} vs Limit {alert['threshold']}): {alert['message']} — *{alert['action']}*"
    if sev == "CRITICAL":
        st.error(f"🔴 CRITICAL | {text}")
    elif sev == "WARNING":
        st.warning(f"🟠 WARNING | {text}")
    else:
        st.success(f"🟢 INFO | {text}")

# Colorful Chart & Vibrant Geospatial Map
st.markdown('<div class="section-header">📊 Colorful Forecast Analytics & Interactive City Map</div>', unsafe_allow_html=True)
chart_col, map_col = st.columns([1.8, 1.2])

with chart_col:
    if not forecast_df.empty:
        chart_df = forecast_df.set_index("timestamp")[["temp_c", "humidity", "rain_prob_pct"]]
        chart_df.columns = ["Temperature (°C)", "Humidity (%)", "Rain Probability (%)"]
        st.area_chart(
            chart_df,
            color=["#ff4b6e", "#00d2ff", "#a855f7"],
            height=380,
        )

with map_col:
    if payload.get("lat") is not None and payload.get("lon") is not None:
        lat_val = float(payload["lat"])
        lon_val = float(payload["lon"])
        map_data = pd.DataFrame(
            {
                "lat": [lat_val],
                "lon": [lon_val],
                "city": [payload["city"]],
                "temp": [f"{curr['temp_c']}°C"],
                "condition": [curr["weather_desc"].title()],
            }
        )

        # Outer glowing halo + bright inner beacon on a colorful Voyager basemap
        halo_layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_data,
            get_position="[lon, lat]",
            get_color="[236, 72, 153, 90]",
            get_radius=14000,
        )
        pin_layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_data,
            get_position="[lon, lat]",
            get_color="[249, 115, 22, 240]",
            get_line_color="[255, 255, 255, 255]",
            line_width_min_pixels=3,
            stroked=True,
            get_radius=5500,
            pickable=True,
        )

        view_state = pdk.ViewState(latitude=lat_val, longitude=lon_val, zoom=9.5, pitch=35)
        deck = pdk.Deck(
            map_style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
            initial_view_state=view_state,
            layers=[halo_layer, pin_layer],
            tooltip={"text": "📍 {city}\n🌡️ Temp: {temp}\n🌤️ {condition}"},
        )
        st.pydeck_chart(deck, use_container_width=True)

# Detailed Forecast Table & Download Buttons
st.markdown('<div class="section-header">📋 24-Hour Forecast Breakdown & Export Reports</div>', unsafe_allow_html=True)
st.dataframe(forecast_df, use_container_width=True)

dl_col1, dl_col2 = st.columns(2)
with dl_col1:
    with open(report_paths["csv_report"], "rb") as f_csv:
        st.download_button(
            label="📥 Download Forecast CSV Report",
            data=f_csv,
            file_name=f"{payload['city'].lower()}_forecast.csv",
            mime="text/csv",
            use_container_width=True,
        )
with dl_col2:
    with open(report_paths["txt_report"], "rb") as f_txt:
        st.download_button(
            label="📥 Download Alert Audit TXT Report",
            data=f_txt,
            file_name=f"{payload['city'].lower()}_alert_report.txt",
            mime="text/plain",
            use_container_width=True,
        )

with st.expander("🗄️ View Recent SQLite Query Cache Logs"):
    logs_df = get_recent_logs(limit=10)
    st.dataframe(logs_df, use_container_width=True)
