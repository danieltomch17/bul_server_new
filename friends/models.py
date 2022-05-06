from django.db import models
from teams.models import Team

class Friends(models.Model):
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='friends_team_a')
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE , related_name='friends_team_b')
    accepted = models.BooleanField(default=False)