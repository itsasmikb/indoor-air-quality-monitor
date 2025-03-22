import os
import csv
from datetime import datetime

# File to store sensor data
DATA_FILE = "sensor_data.csv"

# Function to save sensor readings to a CSV file
def save_sensor_data(sensor_data, timestamp, aqi):
    # Check if file exists, if not, create with headers
    file_exists = os.path.isfile(DATA_FILE)
    
    with open(DATA_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write header if the file is new
        if not file_exists:
            writer.writerow(["Timestamp", "PM2.5", "PM10", "CO2", "AQI"])

        # Write sensor data
        writer.writerow([timestamp, sensor_data["PM2.5"], sensor_data["PM10"], sensor_data["CO2"], aqi])

# Function to load historical data
def load_historical_data():
    data = []
    
    if not os.path.isfile(DATA_FILE):
        return {"error": "No data available"}

    with open(DATA_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            data.append({
                "Timestamp": row["Timestamp"],
                "PM2.5": float(row["PM2.5"]),
                "PM10": float(row["PM10"]),
                "CO2": float(row["CO2"]),
                "AQI": float(row["AQI"])
            })
    
    return data
 
