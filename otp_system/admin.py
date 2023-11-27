from django.contrib import admin
from .models import Otp


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Otp._meta.get_fields()]
