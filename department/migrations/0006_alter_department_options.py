# Generated by Django 4.1.7 on 2023-03-03 05:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0005_alter_department_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ['-department_name'], 'permissions': [('custom_can_view_department', 'can  view department'), ('custom_can_add_department', 'can  add department'), ('custom_can_update_department', 'can  update department'), ('custom_can_delete_department', 'can  delete department')], 'verbose_name': 'Department details'},
        ),
    ]
