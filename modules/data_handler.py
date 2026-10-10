"""Local CSV persistence for sensor readings."""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "sensor_readings.csv"
FIELDS = ("timestamp", "PM2.5", "PM10", "CO2", "AQI", "category")


def generate_timestamp() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def save_sensor_data(sensor_data: dict, timestamp: str, aqi: int, category: str) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    exists = DATA_FILE.exists() and DATA_FILE.stat().st_size > 0
    with DATA_FILE.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": timestamp,
            "PM2.5": sensor_data["PM2.5"],
            "PM10": sensor_data["PM10"],
            "CO2": sensor_data["CO2"],
            "AQI": aqi,
            "category": category,
        })


def load_historical_data(limit: int = 100) -> list[dict]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    result = []
    for row in rows[-max(1, min(int(limit), 1000)):]:
        try:
            result.append({
                "timestamp": row["timestamp"],
                "PM2.5": float(row["PM2.5"]),
                "PM10": float(row["PM10"]),
                "CO2": float(row["CO2"]),
                "AQI": int(float(row["AQI"])),
                "category": row.get("category", ""),
            })
        except (KeyError, TypeError, ValueError):
            continue
    return result
