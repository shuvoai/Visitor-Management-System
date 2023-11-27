from rest_framework import serializers
from visitormanagement.models import Visitors


class ResonWiseVisitorChartSerializers(serializers.Serializer):
    visitor_purpose__purpose_name = serializers.CharField()
    count = serializers.IntegerField()


class DepartmentWiseVisitorChartSerializers(serializers.Serializer):
    to_which_department__department_name = serializers.CharField()
    count = serializers.IntegerField()


class NumberofVisitorsPerMonthSerializers(serializers.Serializer):
    count = serializers.IntegerField()
