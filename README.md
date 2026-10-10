# Indoor Air Quality Monitor

A small Flask application for monitoring **simulated or user-supplied indoor sensor readings**. It presents PM2.5, PM10, CO₂, an indicative particulate AQI estimate, health-oriented guidance, and a local history log.

> **Measurement note:** This is a learning/demo application, not a certified air-quality instrument. The AQI estimate applies EPA-style particulate breakpoints to instantaneous readings; official AQI reporting normally relies on prescribed averaging periods and validated instruments. Do not use this display for emergency or regulatory decisions.

## Features

- Responsive dashboard with PM2.5, PM10, CO₂, and indicative AQI cards.
- Simulated readings for a no-hardware demo.
- JSON ingestion endpoint for a microcontroller or other sensor gateway.
- Timestamped CSV history and a trend view.
- Input validation and explicit API error responses.
- AQI category and CO₂ guidance kept separate so CO₂ is not incorrectly treated as a particulate AQI pollutant.

## Stack

Python 3.10+ · Flask · HTML/CSS · Vanilla JavaScript · CSV storage · pytest

## Run locally

```bash
git clone https://github.com/itsasmikb/indoor-air-quality-monitor.git
cd indoor-air-quality-monitor

python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). By default the app runs with simulated readings. The history file is created at `data/sensor_readings.csv` when readings are saved.

For a production deployment, use a WSGI server such as Gunicorn and set `FLASK_DEBUG=0`. Do not expose Flask's development server directly to the internet.

## API

### `GET /api/sensor_data`

Returns one simulated reading and its calculated particulate AQI estimate.

Example response:

```json
{
  "timestamp": "2026-10-10T09:30:00",
  "sensor_data": {"PM2.5": 12.4, "PM10": 25.1, "CO2": 720},
  "aqi": 67,
  "aqi_category": "Moderate",
  "recommendations": ["Ventilate the room if outdoor air is cleaner.", "Consider reducing indoor particle sources."]
}
```

Values above are illustrative, not a live reading.

### `POST /api/sensor_data`

Submit readings as JSON:

```json
{
  "PM2.5": 12.4,
  "PM10": 25.1,
  "CO2": 720
}
```

All three fields must be finite, non-negative numbers. The app timestamps, scores, and saves valid readings. A successful request returns HTTP 201.

### `GET /api/historical_data?limit=100`

Returns the most recent saved readings (up to 1,000) in chronological order.

## AQI approach and limitations

The app linearly interpolates PM2.5 and PM10 concentrations against commonly used US EPA AQI breakpoint bands and displays the higher sub-index as an **indicative particulate AQI estimate**. Because a single instant is not the required averaging period for official AQI, the result is intentionally labelled as an estimate. Sensor calibration, humidity, location, and averaging windows can materially affect readings.

CO₂ is displayed separately as a ventilation indicator with simple contextual guidance. It is not included in the particulate AQI calculation.

## Tests

```bash
python -m pytest
```

## Project layout

```text
app.py                    Flask routes and validation
modules/aqi_calculator.py Particulate AQI estimate + guidance
modules/data_handler.py   CSV persistence and history
modules/sensor_simulator.py
static/app.js             Dashboard fetching and trend rendering
static/style.css          Responsive interface
templates/index.html      Accessible dashboard shell
tests/                    Unit and API tests
```

## Author

Asmi Bandyopadhyay · [GitHub](https://github.com/itsasmikb)
