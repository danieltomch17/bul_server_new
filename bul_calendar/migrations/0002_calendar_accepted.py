# Generated by Django 3.2.6 on 2022-05-24 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bul_calendar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
