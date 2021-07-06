from django.apps import AppConfig
from django.db.models.signals import post_save


class DashboardConfig(AppConfig):
    name = 'dashboard'

    def ready(self):
        import dashboard.signals
