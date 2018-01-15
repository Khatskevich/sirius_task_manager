from django.apps import AppConfig


class ApplicationConfig(AppConfig):
    name = 'core'

    def ready(self):
        from . import handlers
