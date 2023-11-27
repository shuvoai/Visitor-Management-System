from django.urls import path
from .views import DepartmentView, DepartmentUpdateView, DepartmentDeleteView, DepartmentAPIView, DepartmentDataTable, departmentDelete

urlpatterns = [

    path('api/', DepartmentAPIView.as_view(), name="departmentapi"),
    #
    path('', DepartmentView.as_view(), name="departmentview"),
    path('table/', DepartmentDataTable.as_view(), name='department.table'),
    path('update/<pk>', DepartmentUpdateView.as_view(),
         name="departmentupdatetview"),
    path('delete/<pk>', DepartmentDeleteView.as_view(),
         name="departmentdeleteview"),
    path('department-delete/<int:department_id>',
         departmentDelete, name='department.delete')

]
