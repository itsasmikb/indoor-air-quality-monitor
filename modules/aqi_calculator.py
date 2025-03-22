def calculate_aqi(sensor_data):
    """
    Calculate AQI based on PM2.5 and PM10 values.
    Returns AQI value, category, and recommendations.
    """
    pm25 = sensor_data["PM2.5"]
    pm10 = sensor_data["PM10"]

    # Simplified AQI calculation (example thresholds)
    if pm25 <= 50 and pm10 <= 50:
        aqi = max(pm25, pm10)
        category = "Good"
        recommendations = "Air quality is satisfactory."
    elif pm25 <= 100 and pm10 <= 100:
        aqi = max(pm25, pm10)
        category = "Moderate"
        recommendations = "Sensitive groups should reduce outdoor activities."
    else:
        aqi = max(pm25, pm10)
        category = "Unhealthy"
        recommendations = "Everyone should limit outdoor activities."

    return aqi, category, recommendations

