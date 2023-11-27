# Generated by Django 4.1.4 on 2023-01-02 09:39

import department.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0003_alter_department_department_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department_description',
            field=models.TextField(max_length=400, validators=[department.validators.department_details_validator, department.validators.length_validator]),
        ),
    ]