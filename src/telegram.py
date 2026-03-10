from datetime import date as date_type

import httpx

from weather import WeatherData


def _uv_label(uv: float) -> str:
    if uv <= 2:
        return "Low"
    if uv <= 5:
        return "Moderate"
    if uv <= 7:
        return "High"
    if uv <= 10:
        return "Very High"
    return "Extreme"


def _aqi_label(aqi: int) -> str:
    if aqi <= 20:
        return "Good"
    if aqi <= 40:
        return "Fair"
    if aqi <= 60:
        return "Moderate"
    if aqi <= 80:
        return "Poor"
    if aqi <= 100:
        return "Very Poor"
    return "Extremely Poor"


def format_message(data: WeatherData) -> str:
    d = date_type.fromisoformat(data["date"])
    date_str = f"{d.day} {d.strftime('%B %Y')}"
    day_str = d.strftime("%A")

    lines = [
        f"\u2600\ufe0f Weather \u2014 {day_str}, {date_str}",
        "",
        "\U0001f321 Temperature",
        f"  Min {round(data['temp_min'])}\u00b0C \u00b7 Avg {round(data['temp_avg'])}\u00b0C \u00b7 Max {round(data['temp_max'])}\u00b0C",
        f"  Feels like: {round(data['feels_min'])}\u00b0C \u2192 {round(data['feels_max'])}\u00b0C",
        "",
        f"\U0001f327 Rain: {data['precip_probability']}% chance \u00b7 {data['precip_sum']:.1f}mm",
        f"\U0001f4a8 Wind: {round(data['wind_speed_max'])} km/h",
        f"\U0001f4a7 Humidity: {data['humidity_avg']}%",
        "",
        f"\U0001f506 UV Index: {data['uv_index_max']:.0f} ({_uv_label(data['uv_index_max'])})",
        f"\U0001f305 Sunrise: {data['sunrise']} \u00b7 Sunset: {data['sunset']}",
        "",
        f"\U0001f32b Air Quality: {data['aqi']} \u2013 {_aqi_label(data['aqi'])}",
        f"   PM2.5: {data['pm2_5']:.1f} \u00b5g/m\u00b3 \u00b7 PM10: {data['pm10']:.1f} \u00b5g/m\u00b3",
    ]
    return "\n".join(lines)


async def send_message(token: str, chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(url, json=payload)
    resp.raise_for_status()
