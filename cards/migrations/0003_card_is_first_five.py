# Generated by Django 3.2.6 on 2022-04-22 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20220422_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='is_first_five',
            field=models.BooleanField(default=False),
        ),
    ]