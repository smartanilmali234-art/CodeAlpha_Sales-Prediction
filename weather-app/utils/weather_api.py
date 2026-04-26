import requests
import pandas as pd
from config import API_KEY, CURRENT_WEATHER_URL, FORECAST_URL


GEO_URL = "https://api.openweathermap.org/geo/1.0/direct"
REVERSE_GEO_URL = "https://api.openweathermap.org/geo/1.0/reverse"


def search_cities(query):
    if not query.strip():
        return []

    params = {
        "q": query,
        "limit": 8,
        "appid": API_KEY
    }

    response = requests.get(GEO_URL, params=params, timeout=10)

    if response.status_code != 200:
        return []

    cities = []
    for item in response.json():
        name = item.get("name", "")
        state = item.get("state", "")
        country = item.get("country", "")
        lat = item.get("lat")
        lon = item.get("lon")

        label = f"{name}, {state}, {country}" if state else f"{name}, {country}"

        cities.append({
            "label": label,
            "lat": lat,
            "lon": lon
        })

    return cities


def get_city_by_coordinates(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "limit": 1,
        "appid": API_KEY
    }

    response = requests.get(REVERSE_GEO_URL, params=params, timeout=10)

    if response.status_code != 200 or not response.json():
        return None

    data = response.json()[0]

    return {
        "label": f"{data.get('name')}, {data.get('country')}",
        "lat": lat,
        "lon": lon
    }


def get_current_weather_by_coords(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(CURRENT_WEATHER_URL, params=params, timeout=10)

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "city": data.get("name", "Unknown"),
        "country": data.get("sys", {}).get("country", ""),
        "temperature": data.get("main", {}).get("temp", "N/A"),
        "feels_like": data.get("main", {}).get("feels_like", "N/A"),
        "humidity": data.get("main", {}).get("humidity", "N/A"),
        "pressure": data.get("main", {}).get("pressure", "N/A"),
        "wind": data.get("wind", {}).get("speed", "N/A"),
        "condition": data.get("weather", [{}])[0].get("description", "N/A"),
        "icon": data.get("weather", [{}])[0].get("icon", "01d"),
        "visibility": round(data.get("visibility", 0) / 1000, 1) if data.get("visibility") else "N/A",
        "clouds": data.get("clouds", {}).get("all", "N/A")
    }


def get_5_day_forecast_by_coords(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(FORECAST_URL, params=params, timeout=10)

    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()
    rows = []

    for item in data["list"]:
        rows.append({
            "datetime": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "temp_min": item["main"]["temp_min"],
            "temp_max": item["main"]["temp_max"],
            "humidity": item["main"]["humidity"],
            "wind": item["wind"]["speed"],
            "condition": item["weather"][0]["description"],
            "icon": item["weather"][0]["icon"]
        })

    return pd.DataFrame(rows)