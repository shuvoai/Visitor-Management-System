from django.contrib.auth.models import Group
from .models import CustomUser

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from department.models import Department
from employee.models import Employee
from visitingpurpose.models import VisitingPurpose
from visitormanagement.models import Visitors

maintainers, created = Group.objects.get_or_create(name='Maintainers')
appusers, created = Group.objects.get_or_create(name='AppUsers')

permission_list_for_maintainers = [Department, Employee, VisitingPurpose, Visitors]
permission_list_for_app_users = [Visitors]


def assign_permissions_to_groups(permission_list):
    for i in permission_list:
        content_type = ContentType.objects.get_for_model(i)
        post_permission = Permission.objects.filter(content_type=content_type)
        for perm in post_permission:
            maintainers.permissions.add(perm)
            print(perm.codename)


assign_permissions_to_groups(permission_list_for_maintainers)
assign_permissions_to_groups(permission_list_for_app_users)
# breakpoint()

'''

content_type = ContentType.objects.get_for_model(Department)
post_permission = Permission.objects.filter(content_type=content_type)

for perm in post_permission:
    maintainers.permissions.add(perm)
    print(perm.codename)

content_type1 = ContentType.objects.get_for_model(Employee)
post_permission1 = Permission.objects.filter(content_type=content_type1)

for perm in post_permission1:
    maintainers.permissions.add(perm)
    print(perm.codename)


content_type2 = ContentType.objects.get_for_model(VisitingPurpose)
post_permission2 = Permission.objects.filter(content_type=content_type2)

for perm in post_permission2:
    maintainers.permissions.add(perm)
    print(perm.codename)

'''

'''
user = CustomUser.objects.get(pk=2)
user.groups.add(maintainers)
'''

'''
maintainers = Group.objects.get(name='Maintainer')
maintainers.user_set.add(user)

maintainers.permissions.add("Department.update_department_details")

'''
