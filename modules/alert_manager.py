"""Rule-based context for indoor air quality alerts."""
from __future__ import annotations


def get_co2_guidance(co2_ppm: float) -> str:
    if co2_ppm < 800:
        return "CO₂ is in a typical range for many occupied spaces."
    if co2_ppm < 1000:
        return "Consider checking ventilation if this level persists."
    return "CO₂ is elevated for many occupied spaces; consider fresh-air ventilation."
