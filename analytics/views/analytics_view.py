import datetime
import xlsxwriter
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from dashboard.models import Visitors
from dashboard.forms import DateForm
from django.db.models import Sum
from django.db.models import Count

from visitor_token.models import VisitorToken
from visitor_token.service import generate_qr_code
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from urllib.parse import urlencode
import djqscsv
from djqscsv import render_to_csv_response
from department.models import Department
from employee.models import Employee
from visitingpurpose.models import VisitingPurpose


class AnalyticsView(LoginRequiredMixin, View):
    form_class = DateForm
    login_url = 'accounts/login/'
    template_name = 'analytics/analytics.html'
    queryset = Visitors.objects.all()

    def get(self, request):
        form = self.form_class()
        visitors_on_site = Visitors.objects.visitors_on_site().count()
        number_of_visitors = Visitors.get_total_visitors(self)
        visitor_change = Visitors.get_visitor_change_percentage(self)
        previous_month = Visitors.get_previous_month(self)
        visitors_per_month = Visitors.get_visitors_per_month(self)
        allvisitors = Visitors.objects.all()
        visitor_paginator = Paginator(allvisitors, 5)
        visitor_paginator.orphans = 3
        # visitor_paginator.get_elided_page_range(number, *, on_each_side=3, on_ends=2)
        page_number = request.GET.get('page', 1)

        visitor_paginator.ELLIPSIS = "..."
        if page_number == "...":
            page_number = 1

        page_range = visitor_paginator.get_elided_page_range(
            page_number, on_each_side=3, on_ends=1)
        page_obj = visitor_paginator.get_page(page_number)

        income_amount_sum_list = Visitors.objects.values("to_which_department__department_name").annotate(
            count=Count("to_which_department")).order_by('to_which_department')

        return render(
            request,
            self.template_name,
            {
                "page_range": page_range,
                "page_obj": page_obj,
                "allvisitors": allvisitors,
                "date_form": form,
                'income_amount_sum_list': income_amount_sum_list,
                "number_of_visitors": number_of_visitors,
                "visitor_change": visitor_change,
                "previous_month": previous_month,
                "visitors_per_month": visitors_per_month,
                "visitors_on_site": visitors_on_site
            }
        )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            date_satrt = form.cleaned_data["date_start"]
            date_end = form.cleaned_data["date_end"]
            allvisitors = Visitors.objects.filter(
                visitor_date__range=(date_satrt, date_end))
            visitor_change = Visitors.get_visitor_change_percentage(self)
            previous_month = Visitors.get_previous_month(self)
            visitor_paginator = Paginator(allvisitors, 5)
            visitor_paginator.orphans = 3
            # visitor_paginator.get_elided_page_range(number, *, on_each_side=3, on_ends=2)
            page_number = request.GET.get('page', 1)
            page_range = visitor_paginator.get_elided_page_range(
                page_number, on_each_side=4, on_ends=2)
            visitor_paginator.ELLIPSIS = "..."
            page_obj = visitor_paginator.get_page(page_number)

            return render(request, self.template_name,
                          {"page_obj": page_obj, "page_range": page_range, "allvisitors": allvisitors, "date_form": form, "visitor_change": visitor_change, "previous_month": previous_month})
            # return redirect('analyticsview')


class Visitor_details_by_date_search(LoginRequiredMixin, View):
    form_class = DateForm
    login_url = 'accounts/login/'
    template_name = 'analytics/search_by_date.html'
    queryset = Visitors.objects.all()

    def get(self, request):
        form = self.form_class(request.GET)
        date_start = request.session.get("date_start")
        date_end = request.session.get("date_end")
        if form.is_valid():
            date_start = form.cleaned_data["date_start"]
            date_end = form.cleaned_data["date_end"]
            request.session["date_start"] = str(date_start)
            request.session["date_end"] = str(date_end)
        self.queryset = self.queryset.filter(
            visitor_date__range=(date_start, date_end))
        number_of_visitors = self.queryset.count()
        visitor_paginator = Paginator(self.queryset, 5)
        visitor_paginator.orphans = 3
        visitor_paginator.ELLIPSIS = "..."
        page_number = request.GET.get('page', 1)

        if page_number == "...":
            page_number = 1

        page_range = visitor_paginator.get_elided_page_range(
            page_number, on_each_side=3, on_ends=2)

        page_obj = visitor_paginator.get_page(page_number)

        return render(
            request,
            self.template_name,
            {

                "date_start": date_start,
                "date_end": date_end,
                "page_range": page_range,
                "page_obj": page_obj,
                "allvisitors": self.queryset,
                "number_of_visitors": number_of_visitors
            }
        )


class Visitor_details_by_date_search_report(LoginRequiredMixin, View):
    login_url = 'accounts/login/'
    queryset = Visitors.objects.all()

    def get(self, request, **kwargs):
        date_start = request.session.get("date_start")
        date_end = request.session.get("date_end")
        Visitor_queryset = self.queryset.filter(
            visitor_date__range=(date_start, date_end))
        Visitor_queryset_foreign_key = Visitor_queryset.values("visitor_name", "visitor_address", "visitor_phone_number",
                                                               "visitor_email", "to_which_department__department_name", "visitor_purpose__purpose_name", "to_employee__employee_name", "visitor_date")

        # test = request.GET.get('page_object','')
        return render_to_csv_response(Visitor_queryset_foreign_key)


class visitor_details_all_report(LoginRequiredMixin, View):
    login_url = 'accounts/login/'
    queryset = Visitors.objects.all()

    def get(self, request, **kwargs):
        # date_start = request.session.get("date_start")
        # date_end = request.session.get("date_end")

        Visitor_queryset_foreign_key = self.queryset.values("visitor_name", "visitor_address", "visitor_phone_number",
                                                            "visitor_email", "to_which_department__department_name", "visitor_purpose__purpose_name", "to_employee__employee_name", "visitor_date")

        # test = request.GET.get('page_object','')
        return render_to_csv_response(Visitor_queryset_foreign_key)


class VisitorDetailsExcelExport(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        dataList = Visitors.objects.all().order_by('-visitor_date')
        if 'date' in request.GET and request.GET['date'] != "":
            from_date = datetime.datetime.strptime(
                str(request.GET['date']).split(' - ')[0], "%m/%d/%Y")
            to_date = datetime.datetime.strptime(
                str(request.GET['date']).split(' - ')[1], "%m/%d/%Y")
            dataList = dataList.filter(
                visitor_date__gte=from_date, visitor_date__lte=to_date).order_by('-visitor_date')
        if 'department' in request.GET and request.GET['department'] != "":
            dataList = dataList.filter(
                to_which_department__department_name=request.GET['department'])
        if 'employee' in request.GET and request.GET['employee'] != "":
            dataList = dataList.filter(
                to_employee__employee_name=request.GET['employee'])
        if 'visiting_reason' in request.GET and request.GET['visiting_reason'] != "":
            dataList = dataList.filter(
                visitor_purpose__purpose_name=request.GET['visiting_reason'])
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True, }, )
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        all_visitors = dataList.values_list()
        ch = '@'
        i = 0

        for field in Visitors._meta.get_fields()[1:]:
            i = i + 1
            x = chr(ord(ch) + i)
            field_name = field.name.replace("_", " ").title()
            # print(field_name)
            worksheet.write(x + str(1), field_name, bold)
        row = 1
        """user = get_user_model().objects.get(username = request.user.username)
        user_permission_for_response_time = user.has_perm("leads.custom_can_view_response_time")"""

        for visitor in all_visitors:
            col = 0
            j = 0
            for visitor_attribute in visitor:

                j += 1
                if j == 2:
                    visitor_date = visitor_attribute.astimezone().strftime("%b %d, %Y %I:%M:%S%p")
                    worksheet.write(row, col, visitor_date)
                    col += 1
                    # print(visitor_date)
                elif j == 8:
                    department = Department.objects.get(id=visitor_attribute)
                    worksheet.write(row, col, department.department_name)
                    col += 1
                elif j == 9:
                    employee = Employee.objects.get(id=visitor_attribute)
                    worksheet.write(row, col, employee.employee_name)
                    col += 1
                elif j == 10:
                    purpose = VisitingPurpose.objects.get(id=visitor_attribute)
                    worksheet.write(row, col, purpose.purpose_name)
                    col += 1
                else:
                    worksheet.write(row, col, visitor_attribute)
                    col += 1
                """elif j==7:
                    print(visitor_attribute.to_which_department.department_name)
                print(j, visitor_attribute)
            print(visitor)"""
            row += 1
        worksheet.set_column('B:I', 20)
        workbook.close()
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        filename = "aamarPay-Visitor-management-system"
        response['Content-Disposition'] = 'attachment; filename=' + \
            filename + ".xlsx"
        output.close()
        return response
