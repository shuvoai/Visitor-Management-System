# Generated by Django 4.1.4 on 2023-01-02 07:24

from django.db import migrations, models
import visitingpurpose.validators


class Migration(migrations.Migration):

    dependencies = [
        ('visitingpurpose', '0002_alter_visitingpurpose_purpose_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitingpurpose',
            name='purpose_name',
            field=models.CharField(max_length=200, validators=[visitingpurpose.validators.length_validators]),
        ),
    ]