import asyncio
from typing import TypedDict

import httpx

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
AQI_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


class WeatherData(TypedDict):
    date: str
    temp_min: float
    temp_avg: float
    temp_max: float
    feels_min: float
    feels_max: float
    precip_probability: int
    precip_sum: float
    uv_index_max: float
    wind_speed_max: float
    sunrise: str
    sunset: str
    humidity_avg: int
    aqi: int
    pm2_5: float
    pm10: float


def _first_valid(values: list, preferred_index: int = 12) -> float:
    if values[preferred_index] is not None:
        return float(values[preferred_index])
    valid = [v for v in values if v is not None]
    return float(valid[-1]) if valid else 0.0


async def fetch_weather(latitude: float, longitude: float) -> WeatherData:
    forecast_params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": (
            "temperature_2m_min,temperature_2m_mean,temperature_2m_max,"
            "apparent_temperature_min,apparent_temperature_max,"
            "precipitation_sum,precipitation_probability_max,"
            "uv_index_max,windspeed_10m_max,sunrise,sunset"
        ),
        "hourly": "relative_humidity_2m",
        "timezone": "Europe/Lisbon",
        "forecast_days": 1,
    }
    aqi_params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "european_aqi,pm2_5,pm10",
        "timezone": "Europe/Lisbon",
        "forecast_days": 1,
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        forecast_resp, aqi_resp = await asyncio.gather(
            client.get(FORECAST_URL, params=forecast_params),
            client.get(AQI_URL, params=aqi_params),
        )

    forecast_resp.raise_for_status()
    aqi_resp.raise_for_status()

    daily = forecast_resp.json()["daily"]
    hourly = forecast_resp.json()["hourly"]
    aqi_hourly = aqi_resp.json()["hourly"]

    humidity_values = [v for v in hourly["relative_humidity_2m"] if v is not None]
    humidity_avg = round(sum(humidity_values) / len(humidity_values)) if humidity_values else 0

    aqi_values = [v for v in aqi_hourly["european_aqi"] if v is not None]
    aqi = int(max(aqi_values)) if aqi_values else 0

    return WeatherData(
        date=daily["time"][0],
        temp_min=daily["temperature_2m_min"][0],
        temp_avg=daily["temperature_2m_mean"][0],
        temp_max=daily["temperature_2m_max"][0],
        feels_min=daily["apparent_temperature_min"][0],
        feels_max=daily["apparent_temperature_max"][0],
        precip_probability=daily["precipitation_probability_max"][0] or 0,
        precip_sum=daily["precipitation_sum"][0] or 0.0,
        uv_index_max=daily["uv_index_max"][0] or 0.0,
        wind_speed_max=daily["windspeed_10m_max"][0] or 0.0,
        sunrise=daily["sunrise"][0].split("T")[1],
        sunset=daily["sunset"][0].split("T")[1],
        humidity_avg=humidity_avg,
        aqi=aqi,
        pm2_5=_first_valid(aqi_hourly["pm2_5"]),
        pm10=_first_valid(aqi_hourly["pm10"]),
    )
