import datetime as dt
import requests
from location import get_location

base_url = "https://api.openweathermap.org/data/2.5/weather?"
API_key = "db57de08d3ce76c64da6fa12394b1a2d"


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_weather():
    try:
        city_name = get_location()
        url = f"{base_url}appid={API_key}&q={city_name}"
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()

        temp_kelvin = data['main']['temp']
        temp_in_celsius = kelvin_to_celsius(temp_kelvin)
        feels_like_kelvin = data['main']['feels_like']
        feels_like_in_celsius = kelvin_to_celsius(feels_like_kelvin)
        description = data['weather'][0]['description']

        timezone_offset = data['timezone']
        sunrise_timestamp = data['sys']['sunrise'] + timezone_offset
        sunset_timestamp = data['sys']['sunset'] + timezone_offset

        sunrise = dt.datetime.fromtimestamp(sunrise_timestamp, dt.timezone.utc)
        sunset = dt.datetime.fromtimestamp(sunset_timestamp, dt.timezone.utc)

        print(f"Temperature: {temp_in_celsius:.2f}°C")
        print(f"Feels like: {feels_like_in_celsius:.2f}°C")
        print(f"Description: {description.capitalize()}")
        print(f"Sunrise: {sunrise.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Sunset: {sunset.strftime('%Y-%m-%d %H:%M:%S ')}")
        exit()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
    except KeyError as e:
        print(f"Missing data in the API response: {e}")

