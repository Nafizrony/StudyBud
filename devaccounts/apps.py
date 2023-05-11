from django.apps import AppConfig


class DevaccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'devaccounts'
    def ready(self):
        import devaccounts.signals

