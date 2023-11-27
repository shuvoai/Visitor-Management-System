# Generated by Django 4.1.4 on 2023-01-02 09:34

import department.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0002_alter_department_department_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department_description',
            field=models.TextField(max_length=400, validators=[department.validators.name_validator]),
        ),
    ]