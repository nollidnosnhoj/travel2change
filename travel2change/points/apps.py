from django.apps import AppConfig


class PointsConfig(AppConfig):
    name = 'points'

    def ready(self):
        from . import signals  # noqa
