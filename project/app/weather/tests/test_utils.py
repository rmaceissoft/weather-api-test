import pytest

from app.weather.utils import deg_to_compass, wind_speed_to_beaufort_scale, cloudiness_percent_to_okta


@pytest.mark.parametrize("degree_input,expected_compass", [
    (0, "north"),
    (21.5, "north-northeast"),
    (48.75, "northeast"),
    (65, "east-northeast"),
    (90, "east"),
    (111, "east-southeast"),
    (125, "southeast"),
    (155, "south-southeast"),
    (181, "south"),
    (205, "south-southwest"),
    (221, "southwest"),
    (241, "west-southwest"),
    (260, "west"),
    (292, "west-northwest"),
    (305, "northwest"),
    (335, "north-northwest"),
])
def test_deg_to_compass(degree_input, expected_compass):
    assert deg_to_compass(degree_input) == expected_compass


@pytest.mark.parametrize("speed_input,expected_beaufort_scale", [
    (0.3, "Calm"),
    (0.8, "Light air"),
    (2, "Light breeze"),
    (4.1, "Gentle breeze"),
    (5.5, "Moderate breeze"),
    (8, "Fresh breeze"),
    (11.5, "Strong breeze"),
    (15, "High wind"),
    (17.1, "Fresh Gale"),
    (21, "Strong Gale"),
    (26.5, "Storm"),
    (31.6, "Violent storm"),
    (33, "Hurricane force"),
])
def test_wind_speed_to_beaufort_scale(speed_input, expected_beaufort_scale):
    assert wind_speed_to_beaufort_scale(speed_input) == expected_beaufort_scale


@pytest.mark.parametrize("percent_input,expected_okta", [
    (0, "Sky clear"),
    (2, "Few clouds"),
    (20, "Few clouds"),
    (35, "Scattered clouds"),
    (50, "Scattered clouds"),
    (60, "Broken clouds"),
    (80, "Broken clouds"),
    (95, "Broken clouds"),
    (100, "Overcast"),
])
def test_cloudiness_percent_to_okta(percent_input, expected_okta):
    assert cloudiness_percent_to_okta(percent_input) == expected_okta
