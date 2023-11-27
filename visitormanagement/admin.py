from django.contrib import admin

# Register your models here.
from .models import Visitors


class VisitorAdmin(admin.ModelAdmin):
    list_display = [
        "pk", "visitor_date", "visitor_name", "visitor_address",
        "visitor_organization", "visitor_phone_number", "to_which_department",
        "visitor_purpose", "to_employee", "visitor_status", "checkout_time"
    ]


admin.site.register(Visitors, VisitorAdmin)
