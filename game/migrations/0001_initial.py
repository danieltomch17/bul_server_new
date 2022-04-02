# Generated by Django 3.2.6 on 2022-04-02 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cards', '0001_initial'),
        ('teams', '0004_rename_name_team_team_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=256)),
                ('points', models.CharField(max_length=2)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.card')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('results', models.CharField(max_length=50)),
                ('steps', models.ManyToManyField(to='game.Step')),
                ('team_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_a_game_set', to='teams.team')),
                ('team_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_b_game_set', to='teams.team')),
            ],
        ),
    ]