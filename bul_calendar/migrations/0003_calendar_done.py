# Generated by Django 3.2.6 on 2022-05-24 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bul_calendar', '0002_calendar_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
