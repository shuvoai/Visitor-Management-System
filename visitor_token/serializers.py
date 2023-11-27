from rest_framework import serializers
from .models import VisitorToken


class VisitorTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorToken
        fields = ["pk", "token_for", "token"]
