from rest_framework import serializers
from .models import Visitors
from rest_framework.validators import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python
from django.utils.translation import gettext_lazy as _


class MultiRegionPhoneNumberField(PhoneNumberField):
    def to_internal_value(self, data):
        regions = ['BD', 'MY']
        for region in regions:
            try:
                phone_number = to_python(data, region=region)
                if phone_number and phone_number.is_valid():
                    return phone_number
            except Exception:
                pass
        raise ValidationError(self.error_messages["invalid"])


class DepartmentSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    department_name = serializers.CharField(max_length=200)


class PurposeSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    purpose_name = serializers.CharField(max_length=200)


class EmployeeSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    employee_name = serializers.CharField(max_length=200)


class VisitorSerializer(serializers.ModelSerializer):
    visitor_phone_number = MultiRegionPhoneNumberField()

    class Meta:
        model = Visitors
        fields = ["pk", "visitor_name", "visitor_address", "visitor_phone_number", "visitor_organization",
                  "visitor_email", "to_which_department", "visitor_purpose", "to_employee", "visitor_date", ]


class VisitorDetailSerializer(serializers.ModelSerializer):
    to_which_department = DepartmentSerializer()
    visitor_purpose = PurposeSerializer()
    to_employee = EmployeeSerializer()

    class Meta:
        model = Visitors
        fields = '__all__'


class VisitorMinimalSerializer(serializers.ModelSerializer):
    to_which_department = DepartmentSerializer()
    visitor_purpose = PurposeSerializer()
    checkout_time = serializers.SerializerMethodField()

    class Meta:
        model = Visitors
        fields = ["visitor_address", "visitor_organization",
                  "visitor_email", "to_which_department", "visitor_purpose", "checkout_time"]

    def get_checkout_time(self, obj):
        if obj.checkout_time:
            return obj.checkout_time.astimezone().strftime("%b %d, %Y %I:%M:%S%p")


class VisitorPartialUpdateSerializer(serializers.ModelSerializer):
    def validate_checkout_time(self, value):
        if not value:
            raise serializers.ValidationError(
                _('Checkout time must has to be provided')
            )
        return value

    def validate(self, data):
        if data.get('checkout_time') < self.instance.visitor_date:
            raise serializers.ValidationError(
                _('vistior check-out time cannot be lesser than check-in time')
            )
        return data

    class Meta:
        model = Visitors
        fields = ['pk', 'visitor_date', 'visitor_name',
                  'visitor_phone_number', 'visitor_organization', 'checkout_time']
        read_only_fields = ['pk', 'visitor_date', 'visitor_name',
                            'visitor_phone_number', 'visitor_organization']
