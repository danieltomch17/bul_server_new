# Generated by Django 3.2.6 on 2022-03-19 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_name',
            field=models.CharField(default='no name', max_length=50),
            preserve_default=False,
        ),
    ]
