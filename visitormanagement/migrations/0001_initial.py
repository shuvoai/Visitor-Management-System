# Generated by Django 4.1.4 on 2023-01-01 06:34

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
        ('department', '__first__'),
        ('visitingpurpose', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitor_name', models.CharField(max_length=180)),
                ('visitor_address', models.CharField(max_length=400)),
                ('visitor_phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('visitor_email', models.EmailField(max_length=254)),
                ('visitor_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation date')),
                ('to_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
                ('to_which_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.department')),
                ('visitor_purpose', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visitingpurpose.visitingpurpose')),
            ],
            options={
                'verbose_name': 'Visitor data',
                'ordering': ['-visitor_date'],
                'permissions': [('can_add_visitor_form', 'can add visitor form')],
            },
        ),
    ]
