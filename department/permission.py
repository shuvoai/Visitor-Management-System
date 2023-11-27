from authentication.models import CustomUser
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from .models import Department
from django.contrib.auth import get_user_model
#
from visitormanagement.models import Visitors

'''
User = get_user_model()
test  = User.objects.get(id=8)
'''
'''
new_group, created = Group.objects.get_or_create(name ='system_mainatiners')


ct = ContentType.objects.get_for_model(User)
permission1 = Permission.objects.create(codename ='can_read_instance',
                                        name ='can read',
                                                content_type = ct)


permission2 = Permission.objects.create(codename ='can_update_instance',
                                        name ='can update',
                                                content_type = ct)
new_group.permissions.add(permission1)
new_group.permissions.add(permission2)
'''
'''
content_type = ContentType.objects.get_for_model(Department)
content_type1 = ContentType.objects.get_for_model(Visitors)
post_permission = Permission.objects.filter(content_type=content_type)
post_permission1 = Permission.objects.filter(content_type=content_type1)

for perm in post_permission:
    test.user_permissions.add(perm)
    print(perm.codename)


for perm in post_permission1:
    test.user_permissions.add(perm)
    print(perm.codename)

breakpoint()

'''
