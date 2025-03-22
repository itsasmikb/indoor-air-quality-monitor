import random

def simulate_sensor_readings():
    """
    Simulates sensor readings for air quality.
    Returns a dictionary with random values for PM2.5, PM10, and CO2.
    """
    sensor_data = {
        "PM2.5": round(random.uniform(5, 100), 2),
        "PM10": round(random.uniform(10, 200), 2),
        "CO2": round(random.uniform(300, 800), 2)
    }
    return sensor_data
