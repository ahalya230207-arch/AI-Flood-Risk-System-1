from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "AI Flood Risk System Backend is Running",
        "status": "success"
    })


@app.route("/weather")
def weather():

    latitude = request.args.get("lat", "13.0827")
    longitude = request.args.get("lon", "80.2707")

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m,precipitation,rain"
        "&hourly=precipitation,rain"
        "&forecast_hours=6"
        "&timezone=auto"
    )

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    data = response.json()

    current = data["current"]
    hourly = data["hourly"]

    # Rain expected during next 6 hours
    next_6_hour_rain = sum(hourly.get("rain", []))

    # Total precipitation expected during next 6 hours
    next_6_hour_precipitation = sum(
        hourly.get("precipitation", [])
    )

    return jsonify({
        "latitude": latitude,
        "longitude": longitude,

        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "rain": current["rain"],
        "precipitation": current["precipitation"],

        "next_6_hour_rain": round(next_6_hour_rain, 2),
        "next_6_hour_precipitation": round(
            next_6_hour_precipitation, 2
        ),

        "updated": current["time"]
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
