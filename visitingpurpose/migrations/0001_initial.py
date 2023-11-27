# Generated by Django 4.1.4 on 2023-01-01 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VisitingPurpose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose_name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'purpose name',
                'ordering': ['-purpose_name'],
                'permissions': (('change_name', 'can change name of product'),),
            },
        ),
    ]
