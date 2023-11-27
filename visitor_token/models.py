from django.db import models
from visitormanagement.models import Visitors
# Create your models here.
from datetime import datetime, timezone


class VisitorToken(models.Model):
    token_for = models.OneToOneField(Visitors, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)

    class Meta:
        permissions = [
            ("custom_can_download_visitor_token", "can download visitor token"),

        ]
