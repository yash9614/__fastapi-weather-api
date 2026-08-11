import httpx
from fastapi import HTTPException

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


async def get_coordinates(city: str):
    """Convert city name to latitude & longitude"""
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(GEOCODING_URL, params=params)
        data = response.json()

    if not data.get("results"):
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")

    location = data["results"][0]
    return {
        "name": location["name"],
        "country": location.get("country"),
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "timezone": location.get("timezone")
    }


async def get_current_weather(lat: float, lon: float, timezone: str = "auto"):
    """Get current weather for given coordinates"""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m",
        "timezone": timezone
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(FORECAST_URL, params=params)
        data = response.json()

    current = data.get("current", {})
    return {
        "temperature": current.get("temperature_2m"),
        "feels_like": current.get("apparent_temperature"),
        "humidity": current.get("relative_humidity_2m"),
        "precipitation": current.get("precipitation"),
        "wind_speed": current.get("wind_speed_10m"),
        "wind_direction": current.get("wind_direction_10m"),
        "weather_code": current.get("weather_code"),
        "time": current.get("time")
    }


async def get_forecast(lat: float, lon: float, timezone: str = "auto"):
    """Get 7-day daily forecast"""
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
        "timezone": timezone,
        "forecast_days": 7
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(FORECAST_URL, params=params)
        data = response.json()

    daily = data.get("daily", {})
    forecast = []

    for i in range(len(daily.get("time", []))):
        forecast.append({
            "date": daily["time"][i],
            "temp_max": daily["temperature_2m_max"][i],
            "temp_min": daily["temperature_2m_min"][i],
            "precipitation": daily["precipitation_sum"][i],
            "wind_speed_max": daily["wind_speed_10m_max"][i],
            "weather_code": daily["weather_code"][i]
        })

    return forecast