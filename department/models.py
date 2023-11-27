from django.db import models

# Create your models here.
from department.validators import name_validator, department_details_validator, length_validator


class DepartmentManager(models.Manager):
    def get_by_natural_key(self, department_name):
        return self.get(department_name=department_name)


class Department(models.Model):
    department_name = models.CharField(
        max_length=200, unique=True, validators=[name_validator])
    department_description = models.TextField(
        max_length=400, validators=[department_details_validator, length_validator])

    objects = DepartmentManager()

    def __str__(self):
        return self.department_name

    class Meta:
        ordering = ["-department_name"]
        verbose_name = "Department details"
        permissions = [
            ("custom_can_view_department", "can  view department"),
            ("custom_can_add_department", "can  add department"),
            ("custom_can_update_department", "can  update department"),
            ("custom_can_delete_department", "can  delete department"),
        ]
