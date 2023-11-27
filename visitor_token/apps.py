from django.apps import AppConfig


class VisitorTokenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'visitor_token'

    def ready(self):
        import visitor_token.signals
