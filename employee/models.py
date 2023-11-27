from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from department.models import Department
from employee.validators import name_validaotr, length_validator, string_validator, field_required_validator, email_validator, validate_phone_number


class Employee(models.Model):
    employee_name = models.CharField(
        max_length=200,
        validators=[name_validaotr, length_validator,
                    string_validator, field_required_validator]
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )
    employee_email = models.EmailField(
        max_length=254,
        unique=True, null=True,
        validators=[email_validator]
    )

    phone_number = models.CharField(
        verbose_name=_('Employee phone number'),
        max_length=15,
        null=True,
        blank=True,
        help_text=_("Employee phone number"),
        validators=[validate_phone_number]
    )

    def __str__(self):
        return self.employee_name

    class Meta:
        ordering = ["employee_name"]
        verbose_name = "Employee"
        permissions = [
            ("custom_can_view_employee", "can  view employee"),
            ("custom_can_add_employee", "can  add employee"),
            ("custom_can_update_employee", "can  update employee"),
            ("custom_can_delete_employee", "can  delete employee"),
        ]
