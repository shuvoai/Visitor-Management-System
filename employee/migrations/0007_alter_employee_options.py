# Generated by Django 4.1.7 on 2023-03-02 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_alter_employee_employee_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['employee_name'], 'permissions': [('custom_can_add_employee', 'can  add employee'), ('custom_can_update_employee', 'can  update employee'), ('custom_can_delete_employee', 'can  delete employee')], 'verbose_name': 'Employee'},
        ),
    ]
