// Function to fetch real-time air quality data
function fetchData() {
    fetch("/api/sensor_data")  // Calls the Flask API route
    .then(response => response.json())  // Convert response to JSON
    .then(data => {
        // Format and display the data
        let display = `
            <h3>Air Quality Data</h3>
            <p><strong>Timestamp:</strong> ${data.timestamp}</p>
            <p><strong>PM2.5:</strong> ${data.sensor_data["PM2.5"]} µg/m³</p>
            <p><strong>PM10:</strong> ${data.sensor_data["PM10"]} µg/m³</p>
            <p><strong>CO2:</strong> ${data.sensor_data["CO2"]} ppm</p>
            <p><strong>AQI:</strong> ${data.aqi} (${data.aqi_category})</p>
            <p><strong>Recommendations:</strong> ${data.recommendations}</p>
        `;
        document.getElementById("data").innerHTML = display;
    })
    .catch(error => {
        console.error("Error fetching data:", error);
        document.getElementById("data").innerHTML = "<p style='color: red;'>Failed to load data.</p>";
    });
}
