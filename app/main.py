from fastapi import FastAPI, Query
from app.weather import get_coordinates, get_current_weather, get_forecast

app = FastAPI(
    title="FastAPI Weather API",
    description="Simple weather API powered by Open-Meteo (no API key required)",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI Weather API 🌤️",
        "docs": "/docs",
        "endpoints": {
            "current_by_city": "/weather/{city}",
            "current_by_coords": "/weather?lat=...&lon=...",
            "forecast": "/forecast/{city}"
        }
    }


@app.get("/weather/{city}")
async def weather_by_city(city: str):
    """Get current weather by city name"""
    location = await get_coordinates(city)
    weather = await get_current_weather(
        location["latitude"],
        location["longitude"],
        location.get("timezone", "auto")
    )

    return {
        "location": location,
        "current": weather
    }


@app.get("/weather")
async def weather_by_coords(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """Get current weather by latitude & longitude"""
    weather = await get_current_weather(lat, lon)
    return {
        "coordinates": {"latitude": lat, "longitude": lon},
        "current": weather
    }


@app.get("/forecast/{city}")
async def forecast_by_city(city: str):
    """Get 7-day forecast by city name"""
    location = await get_coordinates(city)
    forecast = await get_forecast(
        location["latitude"],
        location["longitude"],
        location.get("timezone", "auto")
    )

    return {
        "location": location,
        "forecast": forecast
    }