from django.apps import AppConfig

class TradingConfig(AppConfig):
    name = 'binary_broker.applications.trading'
    def ready(self):
        from .signals import SIGNALS
