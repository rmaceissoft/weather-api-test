from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.cache import cache_page

from .utils import OpenWeatherMapClient, OpenWeatherMapError


@cache_page(60 * 2)
def weather(request):
    try:
        city = request.GET["city"]
        country = request.GET["country"]
    except MultiValueDictKeyError:
        return HttpResponseBadRequest()

    client = OpenWeatherMapClient(units="metric")
    try:
        weather_info = client.get_weather_by_city(f"{city}, {country}")
    except OpenWeatherMapError:
        return HttpResponseBadRequest()

    return JsonResponse({
        "location_name": weather_info.location_name,
        "temperature": weather_info.temperature,
        "wind": weather_info.wind,
        "cloudiness": weather_info.cloudiness,
        "pressure": weather_info.pressure,
        "humidity": weather_info.humidity,
        "sunrise": weather_info.sunrise.strftime("%H:%M"),
        "sunset": weather_info.sunset.strftime("%H:%M"),
        "geo_coordinates": weather_info.geo_coordinates,
        "requested_time": weather_info.requested_time.strftime("%Y-%m-%d %H:%M:%S"),
    }, json_dumps_params={"ensure_ascii": False})
