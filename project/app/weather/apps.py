from django.apps import AppConfig


class Config(AppConfig):
    name = "app.weather"
    label = "app_weather"
    verbose_name = "Weather"

    def ready(self):
        pass
