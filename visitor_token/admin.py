from django.contrib import admin

# Register your models here.
from .models import VisitorToken


@admin.register(VisitorToken)
class VisitorTokenAdmin(admin.ModelAdmin):
    list_display = ["pk", "token", "token_for"]
