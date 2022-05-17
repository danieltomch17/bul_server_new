# Generated by Django 3.2.6 on 2022-04-14 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
        ('teams', '0001_initial'),
        ('bul_calendar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.game')),
                ('team_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_a_set', to='teams.team')),
                ('team_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_b_set', to='teams.team')),
            ],
        ),
        migrations.DeleteModel(
            name='Card',
        ),
    ]
