from flask import Flask, render_template, jsonify, request
from modules.sensor_simulator import simulate_sensor_readings
from modules.aqi_calculator import calculate_aqi
from modules.data_handler import save_sensor_data, load_historical_data
from modules.utils import generate_timestamp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/sensor_data', methods=['GET', 'POST'])
def sensor_data():
    if request.method == 'POST':
        # Receive data from Arduino (via POST)
        sensor_data = request.json
        timestamp = generate_timestamp()
        aqi, aqi_category, recommendations = calculate_aqi(sensor_data)
        save_sensor_data(sensor_data, timestamp, aqi)
        return jsonify({"message": "Data saved successfully"}), 200

    # Simulate sensor data (for testing)
    sensor_data = simulate_sensor_readings()
    timestamp = generate_timestamp()
    aqi, aqi_category, recommendations = calculate_aqi(sensor_data)
    return jsonify({
        "timestamp": timestamp,
        "sensor_data": sensor_data,
        "aqi": aqi,
        "aqi_category": aqi_category,
        "recommendations": recommendations
    })

@app.route('/api/historical_data')
def historical_data():
    data = load_historical_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)