# Generated by Django 4.1.4 on 2023-01-01 06:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('visitor_token', '0001_initial'),
        ('visitormanagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitortoken',
            name='token_for',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='visitormanagement.visitors'),
        ),
    ]
