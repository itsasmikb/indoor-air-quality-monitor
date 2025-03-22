<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Indoor Air Quality Monitor</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>Indoor Air Quality Monitor</h1>

    <!-- AQI Alert Box -->
    <div id="alert-box" style="padding: 10px; font-size: 20px; font-weight: bold;">
        Checking air quality...
    </div>

    <!-- Include JavaScript -->
    <script src="{{ url_for('static', filename='alert.js') }}"></script>
</body>
</html>



