from __future__ import annotations

import app as app_module
from modules.aqi_calculator import calculate_aqi, aqi_category
from modules.utils import validate_sensor_payload


def test_aqi_categories():
    assert aqi_category(0) == "Good"
    assert aqi_category(75) == "Moderate"
    assert aqi_category(125) == "Unhealthy for Sensitive Groups"
    assert aqi_category(175) == "Unhealthy"
    assert aqi_category(250) == "Very Unhealthy"
    assert aqi_category(450) == "Hazardous"


def test_calculate_aqi_uses_worse_particulate_subindex():
    score, category, guidance = calculate_aqi({"PM2.5": 5, "PM10": 180, "CO2": 1200})
    assert score > 100
    assert category == "Unhealthy for Sensitive Groups"
    assert any("CO₂" in item for item in guidance)


def test_invalid_concentration_rejected():
    try:
        calculate_aqi({"PM2.5": -1, "PM10": 10})
    except ValueError:
        pass
    else:
        raise AssertionError("Negative concentration should be rejected")


def test_payload_validation():
    values, error = validate_sensor_payload({"PM2.5": 12, "PM10": 24, "CO2": 700})
    assert error is None
    assert values == {"PM2.5": 12.0, "PM10": 24.0, "CO2": 700.0}
    values, error = validate_sensor_payload({"PM2.5": -1, "PM10": 24, "CO2": 700})
    assert values is None and error


def test_api_validation_and_dashboard(monkeypatch, tmp_path):
    monkeypatch.setattr(app_module, "save_sensor_data", lambda *args: None)
    monkeypatch.setattr(app_module, "load_historical_data", lambda limit=100: [])
    client = app_module.app.test_client()
    assert client.get("/").status_code == 200
    assert client.get("/api/sensor_data").status_code == 200
    bad = client.post("/api/sensor_data", json={"PM2.5": -1, "PM10": 20, "CO2": 500})
    assert bad.status_code == 400
    good = client.post("/api/sensor_data", json={"PM2.5": 8, "PM10": 20, "CO2": 500})
    assert good.status_code == 201
    assert client.get("/api/historical_data?limit=10").json == []
