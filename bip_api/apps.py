from django.apps import AppConfig


class BipApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bip_api'

    def ready(self):
       import bip_api.signals