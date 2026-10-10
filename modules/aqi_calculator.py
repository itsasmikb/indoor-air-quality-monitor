"""Indicative particulate AQI estimate using EPA-style breakpoint bands.

This function is educational: instant sensor readings are not equivalent to
regulatory AQI, which uses prescribed averaging periods and validated data.
"""
from __future__ import annotations

from math import floor, isfinite

# (concentration low, concentration high, AQI low, AQI high)
# PM2.5 concentrations in µg/m³; PM10 concentrations in µg/m³.
PM25_BREAKPOINTS = (
    (0.0, 9.0, 0, 50),
    (9.1, 35.4, 51, 100),
    (35.5, 55.4, 101, 150),
    (55.5, 125.4, 151, 200),
    (125.5, 225.4, 201, 300),
    (225.5, 325.4, 301, 400),
    (325.5, 500.4, 401, 500),
)
PM10_BREAKPOINTS = (
    (0.0, 54.0, 0, 50),
    (55.0, 154.0, 51, 100),
    (155.0, 254.0, 101, 150),
    (255.0, 354.0, 151, 200),
    (355.0, 424.0, 201, 300),
    (425.0, 504.0, 301, 400),
    (505.0, 604.0, 401, 500),
)


def _sub_index(concentration: float, breakpoints: tuple[tuple[float, float, int, int], ...]) -> int:
    if not isfinite(concentration) or concentration < 0:
        raise ValueError("Particulate concentration must be a finite non-negative number.")
    concentration = min(concentration, breakpoints[-1][1])
    for c_low, c_high, i_low, i_high in breakpoints:
        if c_low <= concentration <= c_high:
            value = (i_high - i_low) / (c_high - c_low) * (concentration - c_low) + i_low
            return int(floor(value + 0.5))
    # Small gaps between official bands are assigned to the next band's lower bound.
    for index in range(1, len(breakpoints)):
        previous_high = breakpoints[index - 1][1]
        current_low, _, i_low, _ = breakpoints[index]
        if previous_high < concentration < current_low:
            return i_low
    return 500


def aqi_category(aqi: int) -> str:
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Moderate"
    if aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    if aqi <= 200:
        return "Unhealthy"
    if aqi <= 300:
        return "Very Unhealthy"
    return "Hazardous"


def calculate_aqi(sensor_data: dict) -> tuple[int, str, list[str]]:
    """Return max particulate sub-index, category, and practical guidance."""
    try:
        pm25 = float(sensor_data["PM2.5"])
        pm10 = float(sensor_data["PM10"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("PM2.5 and PM10 readings are required numeric values.") from exc

    score = max(_sub_index(pm25, PM25_BREAKPOINTS), _sub_index(pm10, PM10_BREAKPOINTS))
    category = aqi_category(score)
    if score <= 50:
        guidance = ["Particulate levels are relatively low in this estimate.", "Keep normal ventilation and continue monitoring."]
    elif score <= 100:
        guidance = ["Sensitive people may prefer to reduce prolonged exposure if symptoms occur.", "Check likely indoor particle sources such as cooking, smoke, or dust."]
    elif score <= 150:
        guidance = ["Sensitive groups should reduce prolonged exertion in this environment.", "Improve filtration or ventilation when outdoor air is cleaner."]
    elif score <= 200:
        guidance = ["Reduce exposure and address likely indoor particle sources.", "Use suitable particle filtration and reassess the reading."]
    else:
        guidance = ["Treat this reading as a prompt to reduce exposure and investigate the source.", "Verify with a calibrated monitor before making consequential decisions."]

    co2 = sensor_data.get("CO2")
    try:
        co2_value = float(co2) if co2 is not None else None
    except (TypeError, ValueError):
        co2_value = None
    if co2_value is not None and isfinite(co2_value) and co2_value >= 1000:
        guidance.append("CO₂ is elevated for many occupied indoor spaces; consider fresh-air ventilation and check occupancy.")
    return score, category, guidance
