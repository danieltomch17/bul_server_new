from django.db import models
from cards.models import Card
from teams.models import Team

# Create your models here.
class Step(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    description =  models.CharField(max_length=256)
    points =  models.CharField(max_length=2)

class Game(models.Model):
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_a_game_set')
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE , related_name='team_b_game_set')
    date = models.DateField()
    results =  models.CharField(max_length=50)
    steps = models.ManyToManyField(Step)

