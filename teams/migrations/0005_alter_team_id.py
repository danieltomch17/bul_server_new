# Generated by Django 3.2.6 on 2022-04-02 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_rename_name_team_team_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
