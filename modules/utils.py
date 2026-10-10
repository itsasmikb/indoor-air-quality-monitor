"""Shared validation helpers."""
from __future__ import annotations

from math import isfinite


def validate_sensor_payload(payload: object) -> tuple[dict[str, float] | None, str | None]:
    if not isinstance(payload, dict):
        return None, "Request body must be a JSON object."
    values = {}
    for field in ("PM2.5", "PM10", "CO2"):
        if field not in payload:
            return None, f"Missing required field: {field}"
        try:
            value = float(payload[field])
        except (TypeError, ValueError):
            return None, f"{field} must be a numeric value."
        if not isfinite(value) or value < 0:
            return None, f"{field} must be a finite, non-negative value."
        values[field] = value
    return values, None
