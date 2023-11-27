from django.apps import AppConfig


class OtpSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'otp_system'

    def ready(self):
        import otp_system.signals
