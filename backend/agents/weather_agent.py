import requests
from config import OPENWEATHER_API_KEY
from models import WeatherResult


async def weather_agent(destination: str, days: int) -> WeatherResult:
    fallback = WeatherResult(
        condition="Data unavailable",
        average_temp_celsius=25.0,
        humidity_percent=70,
        travel_tip=f"Check local weather before travelling to {destination}."
    )

    try:
        # Check if API key exists
        if not OPENWEATHER_API_KEY:
            return fallback

        # Get coordinates for destination
        geo_url = "http://api.openweathermap.org/geo/1.0/direct"
        geo_params = {
            "q": destination,
            "limit": 1,
            "appid": OPENWEATHER_API_KEY
        }

        geo_response = requests.get(geo_url, params=geo_params, timeout=10)
        geo_data = geo_response.json()

        # Return fallback if city not found
        if not geo_data or len(geo_data) == 0:
            return fallback

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

        # Get weather forecast
        weather_url = "http://api.openweathermap.org/data/2.5/forecast"
        weather_params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "cnt": min(days * 8, 40)
        }

        weather_response = requests.get(weather_url, params=weather_params, timeout=10)
        weather_data = weather_response.json()

        forecasts = weather_data.get("list", [])

        if not forecasts:
            return fallback

        # Calculate averages
        temps = [f["main"]["temp"] for f in forecasts]
        humidities = [f["main"]["humidity"] for f in forecasts]
        conditions = [f["weather"][0]["main"] for f in forecasts]

        avg_temp = round(sum(temps) / len(temps), 1)
        avg_humidity = int(sum(humidities) / len(humidities))
        most_common_condition = max(set(conditions), key=conditions.count)

        tips = {
            "Rain": "Pack a waterproof jacket and umbrella.",
            "Clear": "Perfect weather — carry sunscreen and stay hydrated.",
            "Clouds": "Mild weather, great for walking tours.",
            "Thunderstorm": "Have indoor backup plans ready.",
            "Snow": "Pack warm layers.",
            "Drizzle": "A compact umbrella will be handy."
        }

        tip = tips.get(most_common_condition, "Check local forecasts before each day.")

        return WeatherResult(
            condition=most_common_condition,
            average_temp_celsius=avg_temp,
            humidity_percent=avg_humidity,
            travel_tip=tip
        )

    except Exception as e:
        print(f"Weather agent error: {e}")
        return fallback