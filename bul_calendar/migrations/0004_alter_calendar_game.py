# Generated by Django 3.2.6 on 2022-04-02 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
        ('bul_calendar', '0003_alter_calendar_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='game',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.game'),
        ),
    ]