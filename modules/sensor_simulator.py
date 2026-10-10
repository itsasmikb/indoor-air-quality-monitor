"""Deterministic-shape, random demo readings; these are not real sensor data."""
from __future__ import annotations

import random


def simulate_sensor_readings() -> dict[str, float]:
    return {
        "PM2.5": round(random.uniform(2, 85), 1),
        "PM10": round(random.uniform(5, 150), 1),
        "CO2": round(random.uniform(420, 1450), 0),
    }
