# Generated by Django 3.2.6 on 2022-04-30 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friends',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]