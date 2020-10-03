from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'binary_broker.applications.accounts'
    def ready(self):
        from .signals import SIGNALS
