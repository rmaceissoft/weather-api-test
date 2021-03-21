# -*- coding: utf-8 -*-
from django.conf import settings

from datetime import datetime, timedelta
import requests


def deg_to_compass(num):
    """
    convert degrees to commpass direction
    """
    val = int((num/22.5)+.5)
    compass_directions = [
        "north",
        "north-northeast",
        "northeast",
        "east-northeast",
        "east",
        "east-southeast",
        "southeast",
        "south-southeast",
        "south",
        "south-southwest",
        "southwest",
        "west-southwest",
        "west",
        "west-northwest",
        "northwest",
        "north-northwest"
    ]
    return compass_directions[(val % 16)]


def wind_speed_to_beaufort_scale(value):
    """
    convert wind speed (m/s) to beaufort scale
    """
    beaufort_scale = [
        "Calm",
        "Light air",
        "Light breeze",
        "Gentle breeze",
        "Moderate breeze",
        "Fresh breeze",
        "Strong breeze",
        "High wind",
        "Fresh Gale",
        "Strong Gale",
        "Storm",
        "Violent storm",
        "Hurricane force"
    ]

    # Beaufort scale in m/s
    if value < 0.5:
        str_value = beaufort_scale[0]
    elif 0.5 <= value < 1.5:
        str_value = beaufort_scale[1]
    elif 1.5 <= value < 3.3:
        str_value = beaufort_scale[2]
    elif 3.3 <= value < 5.5:
        str_value = beaufort_scale[3]
    elif 5.5 <= value < 7.9:
        str_value = beaufort_scale[4]
    elif 7.9 <= value < 10.7:
        str_value = beaufort_scale[5]
    elif 10.7 <= value < 13.8:
        str_value = beaufort_scale[6]
    elif 13.8 <= value < 17.1:
        str_value = beaufort_scale[7]
    elif 17.1 <= value < 20.7:
        str_value = beaufort_scale[8]
    elif 20.7 <= value < 24.4:
        str_value = beaufort_scale[9]
    elif 24.4 <= value < 28.4:
        str_value = beaufort_scale[10]
    elif 28.4 <= value < 32.6:
        str_value = beaufort_scale[11]
    elif value >= 32.6:
        str_value = beaufort_scale[12]
    return str_value


def cloudiness_percent_to_okta(value):
    """
    convert cloudiness in percent to the corresponding okta value
    https://en.wikipedia.org/wiki/Okta
    """
    oktas = {
        0: "Sky clear",
        1: "Few clouds",
        2: "Few clouds",
        3: "Scattered clouds",
        4: "Scattered clouds",
        5: "Broken clouds",
        6: "Broken clouds",
        7: "Broken clouds",
        8: "Overcast"
    }

    if value == 0:
        str_value = oktas[0]
    elif 0 < value < 18.75:
        str_value = oktas[1]
    elif 18.75 <= value < 31.25:
        str_value = oktas[2]
    elif 31.25 <= value < 43.75:
        str_value = oktas[3]
    elif 43.75 <= value < 56.25:
        str_value = oktas[4]
    elif 56.25 <= value < 68.75:
        str_value = oktas[5]
    elif 68.75 <= value < 81.25:
        str_value = oktas[6]
    elif 81.25 <= value < 100:
        str_value = oktas[7]
    elif value == 100:
        str_value = oktas[8]
    return str_value


class WeatherInfo:

    def __init__(self, units, json):
        self._units = units
        self._json = json

    @property
    def location_name(self):
        country = self._json["sys"]["country"]
        city = self._json["name"]
        return f"{city}, {country}"

    @property
    def temperature(self):
        value = self._json["main"]["temp"]
        unit = "ºC" if self._units == "metric" else "ºF"
        return f"{value} {unit}"

    @property
    def wind(self):
        """
        output example: Gentle breeze, 3.6 m/s, west - northwest
        """
        _speed = self._json["wind"]["speed"]
        _compass_direction = deg_to_compass(self._json["wind"]["deg"])
        _beaufort_scale = wind_speed_to_beaufort_scale(_speed)
        return f"{_beaufort_scale}, {_speed} m/s, {_compass_direction}"

    @property
    def cloudiness(self):
        value = self._json["clouds"]["all"]
        return cloudiness_percent_to_okta(value)

    @property
    def pressure(self):
        value = self._json["main"]["pressure"]
        return f"{value} hpa"

    @property
    def humidity(self):
        value = self._json["main"]["humidity"]
        return f"{value}%"

    @property
    def sunrise(self):
        value = self._json["sys"]["sunrise"]
        dt = datetime.fromtimestamp(value)
        return dt + timedelta(seconds=self._json["timezone"])

    @property
    def sunset(self):
        value = self._json["sys"]["sunset"]
        offset = timedelta(seconds=self._json["timezone"])
        return datetime.fromtimestamp(value) + offset

    @property
    def geo_coordinates(self):
        _lat = self._json["coord"]["lat"]
        _lon = self._json["coord"]["lon"]
        return f"[{_lat}, {_lon}]"

    @property
    def requested_time(self):
        offset = timedelta(seconds=self._json["timezone"])
        return datetime.fromtimestamp(self._json["dt"]) + offset


class OpenWeatherMapError(Exception):
    pass


class OpenWeatherMapClient:

    def __init__(self, api_key=None, units=None):
        self.api_key = api_key or settings.OPEN_WEATHER_MAP_API_KEY
        self.base_url = "https://api.openweathermap.org"
        self.units = units

    def _build_url(self, path):
        return f"{self.base_url}/data/2.5/{path}"

    def _make_request(self, path, params=None):
        url = self._build_url(path)
        if params is None:
            params = {}
        params["appid"] = self.api_key
        if self.units:
            params["units"] = self.units
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            raise OpenWeatherMapError(
                f"Open Weather Map error response: status code = {resp.status_code}")
        return WeatherInfo(self.units, resp.json())

    def get_weather_by_city(self, city):
        return self._make_request("weather", params={'q': city})
