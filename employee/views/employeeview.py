from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from employee.models import Employee
from employee.forms import EmployeeCreateForm, EmployeeUpdateForm
import sweetify
from department.models import Department
from sweetify.views import SweetifySuccessMixin
from django.http import JsonResponse
from django.db.models import Q
import json
from django.urls import reverse
# Create your views here.


class EmployeeCreate(PermissionRequiredMixin, LoginRequiredMixin, SweetifySuccessMixin, View):
    permission_required = "employee.custom_can_view_employee"
    form_class = EmployeeCreateForm
    initial = {'key': 'value'}
    template_name = 'employee/employee_crud.html'
    employee_update_form = EmployeeUpdateForm()

    def get(self, request, *args, **kwargs):
        allemployee = Employee.objects.all()
        form = self.form_class(initial=self.initial)
        department_list = Department.objects.all().values('department_name')

        selected_department = ''
        if 'department' in request.GET and request.GET['department'] != "":
            selected_department = request.GET['department']

        context = {
            'employeeform': form,
            "allemployee": allemployee,
            'department_list': json.dumps(list(department_list)),
            "employee_update_form": self.employee_update_form,
            'selected_department': selected_department,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            employee_name = form.cleaned_data["employee_name"]
            department = form.cleaned_data["department"]
            employee_email = form.cleaned_data["employee_email"]
            phone_number = form.cleaned_data["phone_number"]
            new_employee = Employee(
                employee_name=employee_name,
                department=department,
                employee_email=employee_email,
                phone_number=phone_number
            )
            new_employee.save()
            sweetify.success(request, 'New Employee added successfully!')
            return redirect('employeeview')
        return render(request, self.template_name, {'employeeform': form})


class EmployeeUpdateView(PermissionRequiredMixin, LoginRequiredMixin, SweetifySuccessMixin, UpdateView):
    permission_required = 'employee.custom_can_update_employee'
    model = Employee
    form_class = EmployeeUpdateForm
    template_name = "employee/employee_update.html"
    success_message = 'Employee successfully updated!'
    success_url = "/employee/"


class EmployeeDeleteView(PermissionRequiredMixin, LoginRequiredMixin, SweetifySuccessMixin, DeleteView):
    permission_required = 'employee.custom_can_delete_employee'
    model = Employee
    template_name = "employee/employee_crud.html"
    success_message = 'Employee  Deleted!'
    success_url = "/employee/"


class EmployeeDataTable(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            if request.method == 'POST':
                dataList = Employee.objects.all().order_by('employee_name')
                search_value = request.POST['search[value]'].strip()
                startLimit = int(request.POST['start'])
                endLimit = startLimit + int(request.POST['length'])
                data_array = []
                totalLength = Employee.objects.count()

                if 'department' in request.GET and request.GET['department'] != "":
                    dataList = dataList.filter(
                        department__department_name=request.GET['department'])

                if search_value != '':
                    # Querying dataset
                    dataList = dataList.filter(Q(employee_name__contains=search_value) | Q(
                        department__department_name__contains=search_value) | Q(employee_email__contains=search_value)).order_by('-employee_name')
                    dataFilter = dataList[startLimit:endLimit]
                    filterLength = dataList.count()
                else:
                    dataFilter = dataList[startLimit:endLimit]
                    filterLength = dataList.count()

                i = 0
                for key, item in enumerate(dataFilter):
                    for field in Employee._meta.fields:
                        value = getattr(item, field.name)
                        if value is None:
                            setattr(item, field.name, "")

                    action = ''
                    update_url = reverse('employeeupdate', args=[item.id])
                    delete_url = reverse('employee.delete', kwargs={
                                         'employee_id': item.id})
                    formatted_employee_name = "<b class='text-sm' >" + item.employee_name + "</b>"
                    formatted_department = "<p class='text-sm' >" + \
                        str(item.department) + "</p>"
                    formatted_employee_email = "<p class='text-sm' >" + item.employee_email + "</p>"
                    phone_number = "<p class='text-sm' >" + item.phone_number + "</p>"
                    action += f"""<a class="btn btn-info btn-sm" href="{update_url}">Update</a>"""
                    action += f"""<a class="m-2 btn btn-danger btn-sm" href="javascript:void(0);"onclick="deleteConfirmation('{delete_url}')">Delete</a>"""
                    row_array = [formatted_employee_name, formatted_department,
                                 formatted_employee_email, phone_number, action]
                    i += 1
                    data_array.append(row_array)

                response = {
                    "draw": request.POST['draw'],
                    "recordsTotal": totalLength,
                    "recordsFiltered": filterLength,
                    "data": data_array,
                }
                return JsonResponse(response)


@login_required
def employeeDelete(request, employee_id):
    employee_instance = Employee.objects.get(pk=employee_id)
    employee_instance.delete()
    return HttpResponseRedirect(reverse("employeeview"))
