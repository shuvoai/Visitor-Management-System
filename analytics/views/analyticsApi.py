from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from dashboard.models import Visitors
from django.db.models import Count
from django.utils import timezone
from analytics.serializers import ResonWiseVisitorChartSerializers, NumberofVisitorsPerMonthSerializers, DepartmentWiseVisitorChartSerializers


class ResonWiseVisitorChart(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        today = timezone.now()
        if 'period' in request.GET and request.GET['period'] != "":
            visitors = Visitors.objects.all()
            if request.GET['period'] == 'today':
                today = timezone.now().date()
                visitors = visitors.filter(visitor_date__date=today)
                visitor_by_purpose = visitors.values("visitor_purpose__purpose_name").annotate(
                    count=Count("visitor_purpose")).order_by('visitor_purpose')
                results = ResonWiseVisitorChartSerializers(
                    visitor_by_purpose, many=True).data
                return Response(results, status=status.HTTP_200_OK)
            elif request.GET['period'] == 'this_month':
                today = timezone.now()
                visitors = visitors.filter(
                    visitor_date__month=today.month, visitor_date__year=today.year)
                visitor_by_purpose = visitors.values("visitor_purpose__purpose_name").annotate(
                    count=Count("visitor_purpose")).order_by('visitor_purpose')
                results = ResonWiseVisitorChartSerializers(
                    visitor_by_purpose, many=True).data
                return Response(results, status=status.HTTP_200_OK)
            elif request.GET['period'] == 'this_year':
                today = timezone.now()
                visitors = visitors.filter(visitor_date__year=today.year)
                visitor_by_purpose = visitors.values("visitor_purpose__purpose_name").annotate(
                    count=Count("visitor_purpose")).order_by('visitor_purpose')
                results = ResonWiseVisitorChartSerializers(
                    visitor_by_purpose, many=True).data
                return Response(results, status=status.HTTP_200_OK)

        visitor_by_purpose = Visitors.objects.filter(visitor_date__month=today.month).values("visitor_purpose__purpose_name").annotate(
            count=Count("visitor_purpose")).order_by('visitor_purpose')
        results = ResonWiseVisitorChartSerializers(
            visitor_by_purpose, many=True).data
        return Response(results, status=status.HTTP_200_OK)


class DepartmentWiseVisitorChart(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        today = timezone.now()
        if 'period' in request.GET and request.GET['period'] != "":
            visitors = Visitors.objects.all()
            if request.GET['period'] == 'today':
                today = timezone.now().date()
                visitors = visitors.filter(visitor_date__date=today)
                visitor_by_purpose = visitors.values("to_which_department__department_name").annotate(
                    count=Count("to_which_department")).order_by('to_which_department__department_name')
                results = DepartmentWiseVisitorChartSerializers(
                    visitor_by_purpose, many=True).data
                return Response(results, status=status.HTTP_200_OK)
            elif request.GET['period'] == 'this_month':
                today = timezone.now()
                visitors = visitors.filter(
                    visitor_date__month=today.month, visitor_date__year=today.year)
                visitor_by_purpose = visitors.values("to_which_department__department_name").annotate(
                    count=Count("to_which_department")).order_by('to_which_department__department_name')
                results = DepartmentWiseVisitorChartSerializers(
                    visitor_by_purpose, many=True).data
                return Response(results, status=status.HTTP_200_OK)
            elif request.GET['period'] == 'this_year':
                today = timezone.now()
                visitors = visitors.filter(visitor_date__year=today.year)
                visitor_by_purpose = visitors.values("to_which_department__department_name").annotate(
                    count=Count("to_which_department")).order_by('to_which_department__department_name')
                results = DepartmentWiseVisitorChartSerializers(
                    visitor_by_purpose, many=True).data
                return Response(results, status=status.HTTP_200_OK)
        visitor_by_department = Visitors.objects.filter(visitor_date__month=today.month).values(
            "to_which_department__department_name").annotate(count=Count("to_which_department")).order_by('to_which_department')
        results = DepartmentWiseVisitorChartSerializers(
            visitor_by_department, many=True
        ).data
        return Response(results, status=status.HTTP_200_OK)


class NumberofVisitorsPerMonth(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        # visitors = Visitors.objects.all().annotate(count=Count("pk"))
        if 'period' in request.GET and request.GET['period'] != "":
            visitors = Visitors.objects.all()
            if request.GET['period'] == 'today':
                today = timezone.now().date()
                visitors = visitors.filter(
                    visitor_date__date=today).annotate(count=Count("pk"))
            elif request.GET['period'] == 'this_month':
                today = timezone.now()
                visitors = visitors.filter(
                    visitor_date__month=today.month, visitor_date__year=today.year).annotate(count=Count("pk"))
            elif request.GET['period'] == 'this_year':
                today = timezone.now()
                visitors = visitors.filter(
                    visitor_date__year=today.year).annotate(count=Count("pk"))
        serializer = NumberofVisitorsPerMonthSerializers(visitors)
        results = serializer.data
        return Response(results, status=status.HTTP_200_OK)
