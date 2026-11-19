import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from src.config import OUTPUTS_DIR


def generate_forecast_chart(city: str, forecast_df: pd.DataFrame) -> str:
    if forecast_df.empty:
        return ""

    labels = [ts[5:16] if len(ts) >= 16 else ts for ts in forecast_df["timestamp"]]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    fig.suptitle(f"Weather Forecast Trend — {city}", fontsize=14, fontweight="bold")

    ax1.plot(labels, forecast_df["temp_c"], marker="o", color="#E63946", linewidth=2.5, label="Temp (°C)")
    ax1.fill_between(labels, forecast_df["temp_c"], color="#E63946", alpha=0.15)
    ax1.set_ylabel("Temperature (°C)", fontweight="bold", color="#E63946")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper right")

    for i, val in enumerate(forecast_df["temp_c"]):
        ax1.annotate(f"{val:.1f}°", (labels[i], val), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)

    ax2.bar(labels, forecast_df["rain_prob_pct"], color="#457B9D", alpha=0.75, width=0.5, label="Rain Prob (%)")
    ax2.plot(labels, forecast_df["humidity"], marker="s", color="#2A9D8F", linewidth=2, label="Humidity (%)")
    ax2.set_ylabel("Percentage (%)", fontweight="bold", color="#1D3557")
    ax2.set_ylim(0, 105)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="upper right")

    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    safe_city = city.lower().replace(" ", "_")
    chart_path = OUTPUTS_DIR / f"{safe_city}_forecast_chart.png"
    plt.savefig(chart_path, dpi=150)
    plt.close(fig)
    return str(chart_path)
