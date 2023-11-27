from django.contrib import admin

# Register your models here.
from .models import VisitingPurpose


@admin.register(VisitingPurpose)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["pk", "purpose_name"]
