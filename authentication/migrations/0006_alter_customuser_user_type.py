# Generated by Django 4.1.4 on 2023-01-09 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'maintainers'), (2, 'app users')], default=2, null=True),
        ),
    ]