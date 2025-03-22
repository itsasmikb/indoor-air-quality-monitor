<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Indoor Air Quality Monitor</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <style>
        #alert-box {
            padding: 10px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 5px;
            margin: 20px 0;
        }
        .good {
            background-color: #d4edda;
            color: #155724;
        }
        .moderate {
            background-color: #fff3cd;
            color: #856404;
        }
        .unhealthy {
            background-color: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <h1>Indoor Air Quality Monitor</h1>

    <!-- AQI Alert Box -->
    <div id="alert-box" class="good">
        Checking air quality...
    </div>

    <!-- Include JavaScript -->
    <script src="{{ url_for('static', filename='alert.js') }}"></script>
</body>
</html>



