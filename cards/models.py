from django.db import models

from teams.models import Team

# Create your models here.
class Card(models.Model):
    player_name = models.CharField(max_length=50)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.player_name