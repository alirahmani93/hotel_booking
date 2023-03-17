import logging

from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.common'

    def ready(self):
        from .models import Configuration
        try:
            Configuration.load()
        except:
            logging.log(level=logging.INFO, msg="config not loaded")
