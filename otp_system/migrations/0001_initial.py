# Generated by Django 4.1.7 on 2023-08-21 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('visitormanagement', '0006_visitors_checkout_time_visitors_visitor_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('otp_code', models.CharField(help_text='OTP code after hashing', max_length=64, unique=True, verbose_name='OTP code')),
                ('visitors', models.OneToOneField(help_text='The visitor associated with this OTP.', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='visitor_otp', serialize=False, to='visitormanagement.visitors', verbose_name='visitor')),
                ('is_varified', models.BooleanField(blank=True, default=False, null=True, verbose_name='OTP verification status')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp of OTP creation', verbose_name='created at')),
                ('send_at', models.DateTimeField(blank=True, help_text='The timestamp of the OTP send to the visitor phone', null=True, verbose_name='send at')),
                ('valid_till', models.DateTimeField(blank=True, help_text='The OTP will be valid until this timestamp', null=True, verbose_name='valid till')),
                ('verified_at', models.DateTimeField(blank=True, help_text='The OTP verified at.', null=True, verbose_name='verified at')),
            ],
        ),
    ]
