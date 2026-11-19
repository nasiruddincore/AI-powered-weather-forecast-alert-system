# 🌦️ Weather Forecast & Automated Risk Alert Application

An industry-oriented Python application that ingests real-time and forecasted meteorological data, evaluates severe weather thresholds (Heat, Rain/Storm, High Humidity, Gale Winds, and Air Quality), serves JSON endpoints via **FastAPI**, and renders interactive charts and maps in a **Streamlit** dashboard.

---

## 📌 Problem Statement & Industry Relevance
Manual weather monitoring is reactive and error-prone. Organizations across **logistics, agriculture, aviation, construction, and event management** require automated systems that continuously evaluate forecast metrics and trigger actionable risk advisories before disruptions occur.

## ✨ Key Features
- **Multi-Source Ingestion:** Seamlessly switches between **OpenWeatherMap API**, **Open-Meteo Free API** (zero-key), and an offline **Virtual Simulation Mode**.
- **Automated Risk Rule Engine:** Evaluates current and 24-hour forecast peaks against customizable thresholds for Temperature, Rain Probability, Humidity, Wind Speed, and US AQI.
- **FastAPI REST Backend:** Exposes `/weather/{city}`, `/logs`, and `/health` endpoints with interactive Swagger UI docs.
- **Interactive Streamlit Dashboard:** Displays KPI cards, severity-coded alert banners, multi-metric trend charts, and geospatial city maps.
- **SQLite Caching & Automated Reporting:** Logs historical queries into SQLite and exports downloadable `.csv` forecast tables, `.txt` audit reports, and `.png` Matplotlib charts.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Backend API:** FastAPI, Uvicorn, Pydantic
- **Frontend Dashboard:** Streamlit
- **Data Processing & Visualization:** Pandas, Matplotlib
- **Database & Storage:** SQLite3, JSON, CSV
- **HTTP & Config:** Requests, Python-Dotenv

## 📂 Project Structure
```text
Weather-Forecast-Alert-Application/
├── data/               # Offline simulation JSON & SQLite cache
├── src/                # Modular ingestion, processing, alert, API & chart modules
├── outputs/            # Generated Matplotlib PNG trend charts
├── reports/            # Generated CSV forecast & TXT alert reports
├── images/             # Application screenshots
├── dashboard.py        # Streamlit web dashboard
├── main.py             # CLI runner
├── requirements.txt    # Dependencies
├── .env.example        # Environment configuration template
└── README.md           # Documentation