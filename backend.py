from flask import Flask, jsonify, request
import json
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MONTH_NAMES = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    city_id = request.json.get('city_id')
    url = f"https://worldweather.wmo.int/en/json/{city_id}_en.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        city_data = data.get("city", {})
        
        city_info = extract_city_info(city_data)
        forecast_info = extract_forecast_info(city_data.get("forecast", {}))
        climate_info = extract_climate_info(city_data.get("climate", {}))

        return jsonify({
            "city_info": city_info,
            "forecast_info": forecast_info,
            "climate_info": climate_info
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

def extract_city_info(city_data):
    city_info = {
        "name": city_data.get("cityName", ""),
        "coordinates": (city_data.get("cityLatitude", ""), city_data.get("cityLongitude", "")),
        "timezone": city_data.get("timeZone", "")
    }
    return city_info

def extract_forecast_info(forecast_data):
    forecast_info = []
    for forecast in forecast_data.get("forecastDay", []):
        info = {
            "date": forecast.get("forecastDate", ""),
            "min_temp": forecast.get("minTemp", ""),
            "max_temp": forecast.get("maxTemp", ""),
            "weather_desc": forecast.get("weather", "")
        }
        forecast_info.append(info)
    return forecast_info

def extract_climate_info(climate_data):
    climate_info = []
    for climate in climate_data.get("climateMonth", []):
        info = {
            "month": MONTH_NAMES.get(climate.get("month", ""), ""),
            "mean_daily_min_temp": climate.get("minTemp", ""),
            "mean_daily_max_temp": climate.get("maxTemp", ""),
            "mean_total_precipitation": climate.get("rainfall", "")
        }
        climate_info.append(info)
    return climate_info

if __name__ == '__main__':
    app.run(debug=True)
