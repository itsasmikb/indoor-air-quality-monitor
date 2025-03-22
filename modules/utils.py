from datetime import datetime

# Function to generate a timestamp
def generate_timestamp():
    """Returns the current timestamp in YYYY-MM-DD HH:MM:SS format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Function to determine AQI color scale
def color_scale_for_aqi(aqi):
    """
    Returns a color based on AQI value.
    """
    if aqi <= 50:
        return "green"  # Good
    elif aqi <= 100:
        return "yellow"  # Moderate
    elif aqi <= 150:
        return "orange"  # Unhealthy for Sensitive Groups
    elif aqi <= 200:
        return "red"  # Unhealthy
    elif aqi <= 300:
        return "purple"  # Very Unhealthy
    else:
        return "maroon"  # Hazardous
 
