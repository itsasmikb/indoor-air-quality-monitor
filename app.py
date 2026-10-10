"""Flask API and dashboard for the indoor air quality demo."""
from __future__ import annotations

import os
from flask import Flask, jsonify, render_template, request

from modules.aqi_calculator import calculate_aqi
from modules.data_handler import generate_timestamp, load_historical_data, save_sensor_data
from modules.sensor_simulator import simulate_sensor_readings
from modules.utils import validate_sensor_payload

app = Flask(__name__)


def enrich_reading(sensor_data: dict, timestamp: str | None = None) -> dict:
    score, category, recommendations = calculate_aqi(sensor_data)
    return {
        "timestamp": timestamp or generate_timestamp(),
        "sensor_data": sensor_data,
        "aqi": score,
        "aqi_category": category,
        "recommendations": recommendations,
        "is_simulated": True,
    }


@app.get("/")
def home():
    return render_template("index.html")


@app.route("/api/sensor_data", methods=["GET", "POST"])
def sensor_data():
    if request.method == "GET":
        reading = enrich_reading(simulate_sensor_readings())
        reading["is_simulated"] = True
        return jsonify(reading)

    values, error = validate_sensor_payload(request.get_json(silent=True))
    if error:
        return jsonify({"error": error}), 400
    try:
        reading = enrich_reading(values)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    save_sensor_data(values, reading["timestamp"], reading["aqi"], reading["aqi_category"])
    reading["is_simulated"] = False
    return jsonify(reading), 201


@app.get("/api/historical_data")
def historical_data():
    try:
        limit = int(request.args.get("limit", "100"))
    except ValueError:
        return jsonify({"error": "limit must be an integer."}), 400
    return jsonify(load_historical_data(limit))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
    )
