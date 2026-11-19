The AI powered weather-forecast-alert-system is an intelligent meteorological monitoring and decision-support application designed to ingest real-time and forecasted weather data, evaluate environmental risk thresholds, and deliver proactive alerts across multiple interfaces. Built with Python, FastAPI, Streamlit, Pandas, Matplotlib, and SQLite, the system seamlessly bridges OpenWeatherMap, Open-Meteo's zero-key live API, and a deterministic offline simulation engine (data/sample_weather.json) so users can test, demonstrate, and analyze severe weather scenarios—including heatwaves, heavy rain and storms, high humidity, strong winds, and poor air quality—without relying on expensive hardware or uninterrupted network access.

Beyond basic weather lookup, this project transforms raw meteorological time-series into actionable operational intelligence for travelers, farmers, logistics planners, event organizers, and everyday users. By pairing a threshold-based alert rule engine with SQLite historical caching, FastAPI REST endpoints, downloadable CSV and TXT audit reports, and a colorful interactive Streamlit dashboard featuring area charts and a 3D PyDeck geospatial city map, the application demonstrates end-to-end software engineering, API integration, data processing, and data visualization in a clean, GitHub-ready portfolio repository.


✨ Key Features
Multi-Source Weather Ingestion: Supports OpenWeatherMap API, Open-Meteo Free Live API (no API key required), and an offline Virtual Simulation Mode (Mumbai, Delhi, London, Tokyo).
Automated Risk Alert Engine: Evaluates current and 24-hour forecast peaks against customizable thresholds for Temperature (°C), Rain Probability (%), Humidity (%), Wind Speed (m/s), and Air Quality Index (AQI) with CRITICAL, WARNING, and INFO severity levels.
Colorful Interactive Streamlit Dashboard: Features gradient KPI cards, severity-coded alert banners, multi-metric area charts, an interactive PyDeck geospatial city map, SQLite query logs, and one-click report downloads.
FastAPI REST Backend: Exposes /health, /weather/{city}, and /logs endpoints with interactive Swagger documentation.
Automated Charts & Reports: Generates high-resolution Matplotlib PNG charts in outputs/ and timestamped .csv and .txt reports in reports/.


🛠️ Tech Stack
Language: Python 3.10+
Backend API: FastAPI, Uvicorn, Pydantic
Frontend Dashboard: Streamlit, PyDeck
Data Processing & Visualization: Pandas, Matplotlib
Database & Configuration: SQLite3, Requests, Python-Dotenv


📂 Project Folder Structure
Weather-Forecast-Alert-Application/
├── data/
│   ├── sample_weather.json
│   └── weather_cache.db
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── weather_fetcher.py
│   ├── data_processor.py
│   ├── alert_engine.py
│   ├── visualizer.py
│   ├── report_generator.py
│   └── api.py
├── outputs/
├── reports/
├── images/
├── docs/
├── dashboard.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md


💻 PowerShell Setup & Execution Commands
1. Navigate to Project Folder & Set Up Virtual Environment
cd "F:\IIT DELHI-1\IIP Projects - Python\Weather-Forecast-Alert-Application\Weather-Forecast-Alert-Application"
python -m venv venv
.\venv\Scripts\Activate.ps1
2. Install Dependencies (Using python -m for Application Control Compatibility)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
3. Configure Environment Variables Safely
Copy-Item .env.example .env
notepad .env
4. Run CLI in Virtual Simulation Mode (Offline)
python main.py --city Mumbai --mode simulation
python main.py --city Delhi --mode simulation
python main.py --city London --mode simulation
5. Run CLI in Live Weather Mode
python main.py --city "New York" --mode live
6. Launch the Colorful Streamlit Dashboard
python -m streamlit run dashboard.py
7. Launch the FastAPI Backend Server
python -m uvicorn src.api:app --host 127.0.0.1 --port 8000
8. Fallback Commands (If Deactivating an F:\ Virtual Environment)
deactivate
cd "F:\IIT DELHI-1\IIP Projects - Python\Weather-Forecast-Alert-Application\Weather-Forecast-Alert-Application"
python main.py --city Mumbai --mode simulation
python -m streamlit run dashboard.py
9. Git & GitHub Upload Commands
git init
git status
git add .
git commit -m "feat: add AI powered weather-forecast-alert-system dashboard, API, and CLI"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/weather-forecast-alert-system.git
git push -u origin main


📊 Sample Output & Artifacts
Terminal / TXT Report: Displays current temperature, feels-like temperature, humidity, wind speed, rain probability, US AQI, 24-hour forecast summary, active risk alerts, and recommended actions.
CSV Report: Saved under reports/<city>_forecast_<timestamp>.csv with hourly/interval forecast records.
Charts & Map: Saved under outputs/<city>_forecast_chart.png and rendered interactively inside dashboard.py.


📸 Screenshots Checklist
images/01_folder_structure.png
images/02_cli_simulation.png
images/03_dashboard_alerts.png
images/04_dashboard_charts_map.png
images/05_matplotlib_chart.png
images/06_generated_reports.png
images/07_fastapi_swagger.png


🎓 Learning Outcomes
Consuming REST APIs with timeout and error handling (requests) alongside graceful offline simulation fallback.
Parsing nested JSON payloads into structured Pandas DataFrames and caching observations in SQLite.
Building configurable threshold-based alert rules for weather and air quality risks.
Serving APIs with FastAPI and creating colorful interactive dashboards and maps with Streamlit and PyDeck.

@'
# AI powered weather-forecast-alert-system

**Repository Name:** `weather-forecast-alert-system`

---

## 📌 Extended Project Description

The **AI powered weather-forecast-alert-system** is an intelligent meteorological monitoring and decision-support application designed to ingest real-time and forecasted weather data, evaluate environmental risk thresholds, and deliver proactive alerts across multiple interfaces. Built with Python, FastAPI, Streamlit, Pandas, Matplotlib, and SQLite, the system seamlessly bridges OpenWeatherMap, Open-Meteo's zero-key live API, and a deterministic offline simulation engine (`data/sample_weather.json`) so users can test, demonstrate, and analyze severe weather scenarios—including heatwaves, heavy rain and storms, high humidity, strong winds, and poor air quality—without relying on expensive hardware or uninterrupted network access.

Beyond basic weather lookup, this project transforms raw meteorological time-series into actionable operational intelligence for travelers, farmers, logistics planners, event organizers, and everyday users. By pairing a threshold-based alert rule engine with SQLite historical caching, FastAPI REST endpoints, downloadable CSV and TXT audit reports, and a colorful interactive Streamlit dashboard featuring area charts and a 3D PyDeck geospatial city map, the application demonstrates end-to-end software engineering, API integration, data processing, and data visualization in a clean, GitHub-ready portfolio repository.

---

## ✨ Key Features
- **Multi-Source Weather Ingestion:** Supports OpenWeatherMap API, Open-Meteo Free Live API (no API key required), and an offline Virtual Simulation Mode (`Mumbai`, `Delhi`, `London`, `Tokyo`).
- **Automated Risk Alert Engine:** Evaluates current and 24-hour forecast peaks against customizable thresholds for Temperature (`°C`), Rain Probability (`%`), Humidity (`%`), Wind Speed (`m/s`), and Air Quality Index (`AQI`) with `CRITICAL`, `WARNING`, and `INFO` severity levels.
- **Colorful Interactive Streamlit Dashboard:** Features gradient KPI cards, severity-coded alert banners, multi-metric area charts, an interactive PyDeck geospatial city map, SQLite query logs, and one-click report downloads.
- **FastAPI REST Backend:** Exposes `/health`, `/weather/{city}`, and `/logs` endpoints with interactive Swagger documentation.
- **Automated Charts & Reports:** Generates high-resolution Matplotlib PNG charts in `outputs/` and timestamped `.csv` and `.txt` reports in `reports/`.

---

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Backend API:** FastAPI, Uvicorn, Pydantic
- **Frontend Dashboard:** Streamlit, PyDeck
- **Data Processing & Visualization:** Pandas, Matplotlib
- **Database & Configuration:** SQLite3, Requests, Python-Dotenv

---

## 📂 Project Folder Structure

```text
Weather-Forecast-Alert-Application/
├── data/
│   ├── sample_weather.json
│   └── weather_cache.db
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── weather_fetcher.py
│   ├── data_processor.py
│   ├── alert_engine.py
│   ├── visualizer.py
│   ├── report_generator.py
│   └── api.py
├── outputs/
├── reports/
├── images/
├── docs/
├── dashboard.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

💻 PowerShell Setup & Execution Commands
1. Navigate to Project Folder & Set Up Virtual Environment
PowerShell

cd "F:\IIT DELHI-1\IIP Projects - Python\Weather-Forecast-Alert-Application\Weather-Forecast-Alert-Application"
python -m venv venv
.\venv\Scripts\Activate.ps1

2. Install Dependencies (Using python -m for Application Control Compatibility)
PowerShell

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

3. Configure Environment Variables Safely
PowerShell

Copy-Item .env.example .env
notepad .env

4. Run CLI in Virtual Simulation Mode (Offline)
PowerShell

python main.py --city Mumbai --mode simulation
python main.py --city Delhi --mode simulation
python main.py --city London --mode simulation

5. Run CLI in Live Weather Mode
PowerShell

python main.py --city "New York" --mode live

6. Launch the Colorful Streamlit Dashboard
PowerShell

python -m streamlit run dashboard.py

7. Launch the FastAPI Backend Server
PowerShell

python -m uvicorn src.api:app --host 127.0.0.1 --port 8000

8. Fallback Commands (If Deactivating an F:\ Virtual Environment)
PowerShell

deactivate
cd "F:\IIT DELHI-1\IIP Projects - Python\Weather-Forecast-Alert-Application\Weather-Forecast-Alert-Application"
python main.py --city Mumbai --mode simulation
python -m streamlit run dashboard.py

9. Git & GitHub Upload Commands
PowerShell

git init
git status
git add .
git commit -m "feat: add AI powered weather-forecast-alert-system dashboard, API, and CLI"
git branch -M main
git remote add origin [https://github.com/](https://github.com/)<YOUR_USERNAME>/weather-forecast-alert-system.git
git push -u origin main

📊 Sample Output & Artifacts

    Terminal / TXT Report: Displays current temperature, feels-like temperature, humidity, wind speed, rain probability, US AQI, 24-hour forecast summary, active risk alerts, and recommended actions.

    CSV Report: Saved under reports/<city>_forecast_<timestamp>.csv with hourly/interval forecast records.

    Charts & Map: Saved under outputs/<city>_forecast_chart.png and rendered interactively inside dashboard.py.

📸 Screenshots Checklist

    images/01_folder_structure.png

    images/02_cli_simulation.png

    images/03_dashboard_alerts.png

    images/04_dashboard_charts_map.png

    images/05_matplotlib_chart.png

    images/06_generated_reports.png

    images/07_fastapi_swagger.png

🎓 Learning Outcomes

    Consuming REST APIs with timeout and error handling (requests) alongside graceful offline simulation fallback.

    Parsing nested JSON payloads into structured Pandas DataFrames and caching observations in SQLite.

    Building configurable threshold-based alert rules for weather and air quality risks.

    Serving APIs with FastAPI and creating colorful interactive dashboards and maps with Streamlit and PyDeck.
    '@ | Set-Content -Encoding UTF8 README.md
