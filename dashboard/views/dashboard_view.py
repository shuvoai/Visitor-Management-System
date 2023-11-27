import datetime
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
import json
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from dashboard.models import Visitors
from dashboard.forms import DateForm
from django.db.models import Sum
from django.db.models import Count
from department.models import Department
from employee.models import Employee
from visitingpurpose.models import VisitingPurpose
from datetime import date, timedelta
import urllib
import datetime
from django.utils import timezone
# paginator test codes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from visitormanagement.serializers import VisitorDetailSerializer, VisitorMinimalSerializer

# Create your views here.


class DashboardView(LoginRequiredMixin, View):
    form_class = DateForm
    # login_url = 'accounts/login/'
    template_name = 'dashboard/visitorstat.html'

    def get(self, request):
        form = self.form_class()
        number_of_visitors = Visitors.get_total_visitors(self)
        visitor_change = Visitors.get_visitor_change_percentage(self)
        previous_month = Visitors.get_previous_month(self)
        visitors_per_month = Visitors.get_visitors_per_month(self)

        allvisitors = Visitors.objects.all()
        selected_department = ''
        selected_employee = ''
        selected_visiting_reason = ''
        filter_date = ''
        req_date = ''

        """if 'date' in request.GET and request.GET['date'] != "":
            req_date = request.GET['date']
            from_date = datetime.datetime.strptime(str(request.GET['date']).split(' - ')[0], "%m/%d/%Y")
            to_date = datetime.datetime.strptime(str(request.GET['date']).split(' - ')[1], "%m/%d/%Y")
            filter_date = "%s to %s" % (from_date.strftime("%d %b %Y"), to_date.strftime("%d %b %Y"))
            allvisitors = allvisitors.filter(visitor_date__gte=from_date, visitor_date__lte=to_date).order_by('-visitor_date')"""

        if 'date' in request.GET and request.GET['date'] != "":
            req_date = request.GET['date']
            from_date = datetime.datetime.strptime(
                str(request.GET['date']).split(' - ')[0], "%m/%d/%Y").date()
            to_date = datetime.datetime.strptime(
                str(request.GET['date']).split(' - ')[1], "%m/%d/%Y").date()
            filter_date = "%s to %s" % (from_date.strftime(
                "%d %b %Y"), to_date.strftime("%d %b %Y"))
            current_date = timezone.localtime(timezone.now()).date()
            to_date = to_date + datetime.timedelta(days=1)
            allvisitors = allvisitors.filter(visitor_date__range=(
                from_date, to_date)).order_by('-visitor_date')
            if current_date >= from_date and current_date <= to_date:
                today_visitors = allvisitors.filter(visitor_date=current_date)
            else:
                today_visitors = []

        if 'department' in request.GET and request.GET['department'] != "":
            selected_department = request.GET['department']
            allvisitors = allvisitors.filter(
                to_which_department__department_name=selected_department)

        if 'employee' in request.GET and request.GET['employee'] != "":
            selected_employee = request.GET['employee']
            allvisitors = allvisitors.filter(
                to_employee__employee_name=selected_employee)

        if 'visiting_reason' in request.GET and request.GET['visiting_reason'] != "":
            selected_visiting_reason = request.GET['visiting_reason']
            allvisitors = allvisitors.filter(
                visitor_purpose__purpose_name=selected_visiting_reason)

        department_list = Department.objects.all().values('department_name')
        employee_list = Employee.objects.all().values("employee_name")
        visiting_reason_list = VisitingPurpose.objects.all().values("purpose_name")
        # paginating the view class
        visitor_paginator = Paginator(allvisitors, 5)
        visitor_paginator.orphans = 3
        visitor_paginator.ELLIPSIS = "..."
        # visitor_paginator.get_elided_page_range(number, *, on_each_side=3, on_ends=2)
        page_number = request.GET.get('page', 1)
        # page_object = request.GET.get('page_obj')

        if page_number == "...":
            page_number = 1

        page_range = visitor_paginator.get_elided_page_range(
            page_number, on_each_side=3, on_ends=2)

        page_obj = visitor_paginator.get_page(page_number)
        income_amount_sum_list = Visitors.objects.values("to_which_department__department_name").annotate(
            count=Count("to_which_department")).order_by('to_which_department')
        context = {
            "page_number": page_number,
            "page_range": page_range,
            "page_obj": page_obj,
            "allvisitors": allvisitors,
            "date_form": form,
            'income_amount_sum_list': income_amount_sum_list,
            "number_of_visitors": number_of_visitors,
            "visitor_change": visitor_change,
            "previous_month": previous_month,
            "visitors_per_month": visitors_per_month,

            'department_list': json.dumps(list(department_list)),
            'employee_list': json.dumps(list(employee_list)),
            'visiting_reason_list': json.dumps(list(visiting_reason_list)),

            'selected_department': selected_department,
            'selected_employee': selected_employee,
            'selected_visiting_reason': selected_visiting_reason,
            'filter_date': filter_date,
            'req_date': req_date

        }

        return render(request, self.template_name, context)

    def post(self, request):

        form = self.form_class(request.POST)
        if form.is_valid():
            date_satrt = form.cleaned_data["date_start"]
            date_end = form.cleaned_data["date_end"]
            allvisitors = Visitors.objects.filter(
                visitor_date__range=(date_satrt, date_end))
            number_of_visitors = allvisitors.count()
            visitor_paginator = Paginator(allvisitors, 5)
            visitor_paginator.orphans = 3
            visitor_paginator.ELLIPSIS = "..."
            # visitor_paginator.get_elided_page_range(number, *, on_each_side=3, on_ends=2)
            page_number = request.GET.get('page', 1)

            if page_number == "...":
                page_number = 1

            page_range = visitor_paginator.get_elided_page_range(
                page_number, on_each_side=4, on_ends=2)
            page_obj = visitor_paginator.get_page(page_number)

            return render(request, self.template_name, {"page_range": page_range, "page_obj": page_obj, "allvisitors": allvisitors, "number_of_visitors": number_of_visitors})
            # return redirect('dashboard')


class VisitorData(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            if request.method == 'POST':
                dataList = Visitors.objects.all().order_by('-visitor_date')
                search_value = request.POST['search[value]'].strip()
                startLimit = int(request.POST['start'])
                endLimit = startLimit + int(request.POST['length'])
                data_array = []
                totalLength = Visitors.objects.count()

                filter_date = ''
                req_date = ''
                """if 'date' in request.GET and request.GET['date'] != "":
                    from_date = datetime.datetime.strptime(str(request.GET['date']).split(' - ')[0], "%m/%d/%Y")
                    to_date = datetime.datetime.strptime(str(request.GET['date']).split(' - ')[1], "%m/%d/%Y")
                    dataList = dataList.filter(visitor_date__gte=from_date, visitor_date__lte=to_date).order_by('-visitor_date')"""

                if 'date' in request.GET and request.GET['date'] != "":
                    req_date = request.GET['date']
                    from_date = datetime.datetime.strptime(
                        str(request.GET['date']).split(' - ')[0], "%m/%d/%Y").date()
                    to_date = datetime.datetime.strptime(
                        str(request.GET['date']).split(' - ')[1], "%m/%d/%Y").date()
                    filter_date = "%s to %s" % (from_date.strftime(
                        "%d %b %Y"), to_date.strftime("%d %b %Y"))
                    current_date = timezone.localtime(timezone.now()).date()
                    to_date = to_date + datetime.timedelta(days=1)
                    dataList = dataList.filter(visitor_date__range=(
                        from_date, to_date)).order_by('-visitor_date')
                    if current_date >= from_date and current_date <= to_date:
                        today_visitors = dataList.filter(
                            visitor_date=current_date)
                    else:
                        today_visitors = []

                if 'department' in request.GET and request.GET['department'] != "":
                    dataList = dataList.filter(
                        to_which_department__department_name=request.GET['department'])
                if 'employee' in request.GET and request.GET['employee'] != "":
                    dataList = dataList.filter(
                        to_employee__employee_name=request.GET['employee'])
                if 'visiting_reason' in request.GET and request.GET['visiting_reason'] != "":
                    dataList = dataList.filter(
                        visitor_purpose__purpose_name=request.GET['visiting_reason'])

                if search_value != '':
                    # Querying dataset
                    dataList = dataList.filter(Q(visitor_name__contains=search_value) | Q(visitor_address__contains=search_value) | Q(visitor_phone_number__contains=search_value) | Q(
                        visitor_email__contains=search_value) | Q(to_which_department__department_name__contains=search_value) | Q(visitor_purpose__purpose_name__contains=search_value) | Q(
                        to_employee__employee_name__contains=search_value) | Q(visitor_date__contains=search_value)).order_by(
                        '-visitor_date')
                    dataFilter = dataList[startLimit:endLimit]
                    filterLength = dataList.count()
                else:
                    dataFilter = dataList[startLimit:endLimit]
                    filterLength = dataList.count()

                i = 0
                for key, item in enumerate(dataFilter):
                    for field in Visitors._meta.fields:
                        value = getattr(item, field.name)
                        if value is None:
                            setattr(item, field.name, "")

                    visiting_date = "<p class='text-sm' >" + \
                        item.visitor_date.astimezone().strftime("%b %d, %Y %I:%M:%S%p") + "</p>"
                    visitor_name = "<p class='text-sm' >" + item.visitor_name + "</p>"
                    visitor_number = "<p class='text-sm' >" + \
                        "0" + \
                        str(item.visitor_phone_number.national_number) + "</p>"

                    visiting_person = "<p class='text-sm' >" + \
                        item.to_employee.employee_name + "</p>"
                    organization = "<p class='text-sm' >" + \
                        item.visitor_organization + "</p>"
                    purpose = "<p class='text-sm' >" + \
                        item.visitor_purpose.purpose_name + "</p>"

                    def get_status_icon(status):
                        status_icons = {
                            Visitors.VisitorStatusChoices.ARRIVED: '<i class="fas fa-check-circle" style="color: green;"></i>',
                            Visitors.VisitorStatusChoices.ON_SITE: '<i class="fas fa-building" style="color: blue;"></i>',
                            Visitors.VisitorStatusChoices.WAITING_APPROVAL: '<i class="fas fa-clock" style="color: orange;"></i>',
                            Visitors.VisitorStatusChoices.DEPARTED: '<i class="fas fa-door-closed" style="color: red;"></i>',
                        }
                        return status_icons.get(status, '')

                    visitor_status = "<div id='visitor-status" + \
                        str(item.pk) + "' style='display: flex; align-items: center; background-color: #e0e0e0; border-radius: 20px; padding: 4px 8px;'>"
                    visitor_status += get_status_icon(item.visitor_status)
                    visitor_status += "<span style='font-size: 0.6rem; margin-left: 3px;'>" + \
                        item.visitor_status + "</span>"
                    visitor_status += "</div>"

                    action = f"""<a href="javascript:void(0);" onclick="visitor_details(event, '{item.id}')"
                    style="display: inline-block;   padding: 2px 2px; border-radius: 20px; text-decoration: none; color: #fff;">
                    <i class="fas fa-info-circle" style="font-size: 1rem; margin-left: 3px; color: blue;"></i>
                    </a>"""
                    if item.visitor_status == Visitors.VisitorStatusChoices.ON_SITE:
                        action += f"""<a id="checkout_button" href="javascript:void(0);" onclick="visitor_checkout(
                            event, '{item.id}')" style="display: inline-block;
                            padding: 2px 2px; border-radius: 20px; text-decoration: none; color: #fff;">
                        <i class="fas fa-door-open" style="font-size: 1rem; margin-left: 3px; color: red;"></i>
                        </a>"""

                    row_array = [visiting_date,
                                 visitor_name, visitor_number, organization, purpose, visiting_person, visitor_status, action]
                    i += 1
                    data_array.append(row_array)

                response = {
                    "draw": request.POST['draw'],
                    "recordsTotal": totalLength,
                    "recordsFiltered": filterLength,
                    "data": data_array,
                }
                return JsonResponse(response)


class VisitorDetails(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        visitor_instance = Visitors.objects.get(pk=request.GET['id'])
        serializer = VisitorMinimalSerializer(visitor_instance)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
