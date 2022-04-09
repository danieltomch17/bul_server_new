from django.db import models

# Create your models here.
class Player(models.Model):

    # player info
    player_name = models.CharField(max_length=50)
    pic = models.CharField(max_length=50)
    height = models.CharField(max_length=50)
    position = models.CharField(max_length=50)

    # player stats
    games = models.PositiveSmallIntegerField()
    pts = models.FloatField()
    p21 = models.FloatField() # avg successfull 2-point shots
    p22 = models.FloatField() # avg 2-point shots
    p31 = models.FloatField() # avg successfull 3-point shots
    p32 = models.FloatField() # avg 3-point shots
    p11 = models.FloatField() # avg successfull 1-point shots
    p12 = models.FloatField() # avg 1-point shots
    p2 = models.FloatField() # avg success rate for 2-point shots
    p3 = models.FloatField() # avg success rate for 3-point shots
    p1 = models.FloatField() # avg success rate for 1-point shots
    defensive_reb = models.FloatField()
    offensive_reb = models.FloatField()
    total_reb = models.FloatField()
    fouls_against = models.FloatField()
    fouls_for = models.FloatField()
    steals = models.FloatField()
    turnovers = models.FloatField()
    assists = models.FloatField()
    blocks_for = models.FloatField()
    blocks_against = models.FloatField()
    VAL = models.FloatField()
    plusminus = models.FloatField()
    dunks = models.FloatField()

    def __str__(self):
        return self.player_name