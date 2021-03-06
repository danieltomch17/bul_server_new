# Generated by Django 3.2.6 on 2022-05-23 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardPack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pack_name', models.CharField(default='', max_length=50)),
                ('price', models.CharField(default=0, max_length=50)),
                ('pack_type', models.CharField(default='Normal', max_length=50)),
                ('pack_image', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_first_five', models.BooleanField(default=False)),
                ('player_name', models.CharField(default=0, max_length=50)),
                ('pic', models.CharField(default=0, max_length=50)),
                ('height', models.CharField(default=0, max_length=50)),
                ('position', models.CharField(default=0, max_length=50)),
                ('games', models.PositiveSmallIntegerField(default=0)),
                ('pts', models.FloatField(default=0)),
                ('p21', models.FloatField(default=0)),
                ('p22', models.FloatField(default=0)),
                ('p31', models.FloatField(default=0)),
                ('p32', models.FloatField(default=0)),
                ('p11', models.FloatField(default=0)),
                ('p12', models.FloatField(default=0)),
                ('p2', models.FloatField(default=0)),
                ('p3', models.FloatField(default=0)),
                ('p1', models.FloatField(default=0)),
                ('defensive_reb', models.FloatField(default=0)),
                ('offensive_reb', models.FloatField(default=0)),
                ('total_reb', models.FloatField(default=0)),
                ('fouls_against', models.FloatField(default=0)),
                ('fouls_for', models.FloatField(default=0)),
                ('steals', models.FloatField(default=0)),
                ('turnovers', models.FloatField(default=0)),
                ('assists', models.FloatField(default=0)),
                ('blocks_for', models.FloatField(default=0)),
                ('blocks_against', models.FloatField(default=0)),
                ('VAL', models.FloatField(default=0)),
                ('plusminus', models.FloatField(default=0)),
                ('dunks', models.FloatField(default=0)),
                ('team_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='teams.team')),
            ],
        ),
    ]
