from django.contrib import admin
from .models import SMSLog


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SMSLog._meta.get_fields()]
