from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages

from department.forms import DepartmentForm, DepartmentUpdateForm
from department.models import Department
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.db.models import Q
# Create your views here.
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from sweetify.views import SweetifySuccessMixin
import sweetify
from django.urls import reverse
from django.contrib.auth.decorators import login_required


class DepartmentView(PermissionRequiredMixin, LoginRequiredMixin, SweetifySuccessMixin, View):
    permission_required = "department.custom_can_view_department"
    form_class = DepartmentForm
    initial = {'key': 'value'}
    template_name = 'department/department_crud.html'
    department_update_form = DepartmentUpdateForm()

    def get(self, request, *args, **kwargs):
        alldepartment = Department.objects.all()
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'departmentform': form, "alldepartment": alldepartment, "department_update_form": self.department_update_form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            department_name = form.cleaned_data["department_name"]
            department_description = form.cleaned_data["department_description"]
            newdepartment = Department(
                department_name=department_name, department_description=department_description)
            newdepartment.save()
            sweetify.success(request, 'New department added successfully!')
            return redirect('departmentview')

        return render(request, self.template_name, {'departmentform': form})


class DepartmentDataTable(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            if request.method == 'POST':
                dataList = Department.objects.all().order_by('department_name')
                search_value = request.POST['search[value]'].strip()
                startLimit = int(request.POST['start'])
                endLimit = startLimit + int(request.POST['length'])
                data_array = []
                totalLength = Department.objects.count()

                if search_value != '':
                    # Querying dataset
                    dataList = dataList.filter(Q(department_name__contains=search_value) | Q(
                        department_description__contains=search_value)).order_by('-department_name')
                    dataFilter = dataList[startLimit:endLimit]
                    filterLength = dataList.count()
                else:
                    dataFilter = dataList[startLimit:endLimit]
                    filterLength = dataList.count()

                i = 0
                for key, item in enumerate(dataFilter):
                    for field in Department._meta.fields:
                        value = getattr(item, field.name)
                        if value is None:
                            setattr(item, field.name, "")

                    action = ''
                    update_url = reverse(
                        'departmentupdatetview', args=[item.id])
                    delete_url = reverse('department.delete', kwargs={
                                         'department_id': item.id})
                    formatted_department_name = "<p class='text-sm text-center' >" + \
                        item.department_name + "</p>"
                    formatted_department_description = "<p class='text-sm text-center' >" + \
                        str(item.department_description) + "</p>"
                    action += f"""<a class="btn btn-info btn-sm" href="{update_url}">Update</a>"""
                    action += f"""<a class="m-2 btn btn-danger btn-sm" href="javascript:void(0);"onclick="deleteConfirmation('{delete_url}')">Delete</a>"""
                    row_array = [str(key + 1), formatted_department_name,
                                 formatted_department_description, action]
                    i += 1
                    data_array.append(row_array)

                response = {
                    "draw": request.POST['draw'],
                    "recordsTotal": totalLength,
                    "recordsFiltered": filterLength,
                    "data": data_array,
                }
                return JsonResponse(response)


class DepartmentUpdateView(PermissionRequiredMixin, LoginRequiredMixin, SweetifySuccessMixin, UpdateView):
    # permission_required =  "department.change_department"
    permission_required = "department.custom_can_update_department"
    model = Department
    form_class = DepartmentUpdateForm
    # fields = ['department_name','department_description']
    template_name = "department/department_update.html"
    success_message = 'Department successfully updated!'
    success_url = "/department/"


class DepartmentDeleteView(PermissionRequiredMixin, LoginRequiredMixin, SweetifySuccessMixin, DeleteView):
    permission_required = 'department.custom_can_delete_department'
    model = Department
    template_name = "department/department_crud.html"
    success_message = 'Department  Deleted!'
    success_url = "/department/"


@login_required
def departmentDelete(request, department_id):
    department_instance = Department.objects.get(pk=department_id)
    department_instance.delete()
    return HttpResponseRedirect(reverse("departmentview"))
