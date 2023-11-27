# Generated by Django 4.1.4 on 2023-01-02 08:56

from django.db import migrations, models
import employee.validators


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_alter_employee_employee_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employee_email',
            field=models.EmailField(max_length=254, null=True, unique=True, validators=[employee.validators.email_validator]),
        ),
    ]
