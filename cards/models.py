from django.db import models

from teams.models import Team

# Create your models here.
class Card(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE, default=0)
    is_first_five = models.BooleanField(default=False)
    
    # player info
    player_name = models.CharField(max_length=50, default=0)
    pic = models.CharField(max_length=50, default=0)
    height = models.CharField(max_length=50, default=0)
    position = models.CharField(max_length=50, default=0)

     # player stats
    games = models.PositiveSmallIntegerField(default=0)
    pts = models.FloatField(default=0)
    p21 = models.FloatField(default=0) # avg successfull 2-point shots
    p22 = models.FloatField(default=0) # avg 2-point shots
    p31 = models.FloatField(default=0) # avg successfull 3-point shots
    p32 = models.FloatField(default=0) # avg 3-point shots
    p11 = models.FloatField(default=0) # avg successfull 1-point shots
    p12 = models.FloatField(default=0) # avg 1-point shots
    p2 = models.FloatField(default=0) # avg success rate for 2-point shots
    p3 = models.FloatField(default=0) # avg success rate for 3-point shots
    p1 = models.FloatField(default=0) # avg success rate for 1-point shots
    defensive_reb = models.FloatField(default=0)
    offensive_reb = models.FloatField(default=0)
    total_reb = models.FloatField(default=0)
    fouls_against = models.FloatField(default=0)
    fouls_for = models.FloatField(default=0)
    steals = models.FloatField(default=0)
    turnovers = models.FloatField(default=0)
    assists = models.FloatField(default=0)
    blocks_for = models.FloatField(default=0)
    blocks_against = models.FloatField(default=0)
    VAL = models.FloatField(default=0)
    plusminus = models.FloatField(default=0)
    dunks = models.FloatField(default=0)

    def __str__(self):
        return self.player_name