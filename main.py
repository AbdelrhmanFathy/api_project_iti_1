import os
import requests
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()
API_KEY = os.getenv("API_KEY")


@dataclass
class WeatherInfo:
    temperature: float
    temperature_unit: str
    wind_speed: float
    wind_speed_unit: str


def get_city_lat_and_lon(address: str) -> tuple[float, float]:
    url = "https://py4e-data.dr-chuck.net/opengeo"

    params = {"q": address.strip()}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    features = data.get("features")
    if not features:
        raise ValueError(f"address not found: {address!r}")

    props = features[0]["properties"]
    return props["lat"], props["lon"]


def fetch_weather(lat: float, lon: float) -> WeatherInfo:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m",
        "appid": API_KEY
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    current = data["current"]
    units = data["current_units"]

    return WeatherInfo(
        temperature=current["temperature_2m"],
        temperature_unit=units["temperature_2m"],
        wind_speed=current["wind_speed_10m"],
        wind_speed_unit=units["wind_speed_10m"],
    )


address = input("Enter location: ")
lat, lon = get_city_lat_and_lon(address)
weather_info = fetch_weather(lat, lon)
print(
    f"Current Temperature: {weather_info.temperature} {weather_info.temperature_unit}"
)
print(f"Current Wind speed: {weather_info.wind_speed} {weather_info.wind_speed_unit}")
