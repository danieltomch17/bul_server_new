from django.db import models
from teams.models import Team
from game.models import Game

class Calendar(models.Model):
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_a_set')
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE , related_name='team_b_set')
    date = models.DateField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE,blank=True, null=True)
