import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"