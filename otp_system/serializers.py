from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class ValidateOtpSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)

    def validate_otp_code(self, data):
        if len(data) != 6:
            raise serializers.ValidationError(
                _('Otp code must be exactly six digit.')
            )
        return data
