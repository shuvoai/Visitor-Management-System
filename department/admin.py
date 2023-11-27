from django.contrib import admin

# Register your models here.
from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["pk", "department_name", "department_description"]
