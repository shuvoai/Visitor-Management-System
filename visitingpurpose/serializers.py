from rest_framework import serializers
from .models import VisitingPurpose


class VisitingPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitingPurpose
        fields = ["pk", "purpose_name"]
