from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


from .managers import CustomUserManager
from employee.validators import email_validator


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        permissions = (
            ("can_delete_instance", "can delete"),
            ("can_read_instance", "can read"),
            ("can_update_instance", "can update"),
            ("can_create_instance", "can create"),
            ("custom_can_view_permissions", "can  view permissions"),
        )
