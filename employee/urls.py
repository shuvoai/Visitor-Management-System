from django.urls import path

from .views import EmployeeCreate, EmployeeUpdateView, EmployeeDeleteView, EmployeeAPIView, EmployeeDataTable, employeeDelete

urlpatterns = [
    path('api/', EmployeeAPIView.as_view(), name="employeeapi"),
    path('', EmployeeCreate.as_view(), name="employeeview"),
    path('table/', EmployeeDataTable.as_view(), name='employee.table'),
    path('update/<pk>', EmployeeUpdateView.as_view(), name="employeeupdate"),
    path('delete/<pk>', EmployeeDeleteView.as_view(), name="employeedelete"),
    path('employee-delete/<int:employee_id>', employeeDelete, name='employee.delete')

]
