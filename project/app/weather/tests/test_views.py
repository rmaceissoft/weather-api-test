from django.urls import reverse

from app.weather.utils import WeatherInfo, OpenWeatherMapClient


def test_weather_api_miss_params(client):
    url = reverse("weather-api")
    response = client.get(url)
    assert response.status_code == 400


def test_weather_api_invalid_city(client):
    url = reverse("weather-api")
    response = client.get(f"{url}?city=ghost")
    assert response.status_code == 400


def test_weather_api_success(client, mocker):

    def mock_get_weather_by_city(self, city):
        return WeatherInfo("metric", {
            "coord": {"lon": -74.0817, "lat": 4.6097},
            "weather": [{"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04d"}],
            "base": "stations",
            "main": {
                "temp": 17.03, "feels_like": 16.67, "temp_min": 17.03, "temp_max": 17.03,
                "pressure": 1014, "humidity": 69, "sea_level": 1014, "grnd_level": 754
            },
            "visibility": 10000,
            "wind": {"speed": 1.1, "deg": 152, "gust": 2.06},
            "clouds": {"all": 70},
            "dt": 1616341854,
            "sys": {"country": "CO", "sunrise": 1616324395, "sunset": 1616368010},
            "timezone": -18000,
            "id": 3688689,
            "name": "Bogotá",
            "cod": 200
        })

    mocker.patch(
        "app.weather.utils.OpenWeatherMapClient.get_weather_by_city",
        mock_get_weather_by_city)

    url = reverse("weather-api")
    response = client.get(f"{url}?city=Lima&country=pe")

    assert response.status_code == 200
    assert response["content-type"] == "application/json"
    json_response = response.json()
    assert "location_name" in json_response
    assert "temperature" in json_response
    assert "wind" in json_response
    assert "cloudiness" in json_response
    assert "pressure" in json_response
    assert "humidity" in json_response
    assert "sunrise" in json_response
    assert "sunset" in json_response
    assert "geo_coordinates" in json_response
    assert "requested_time" in json_response
