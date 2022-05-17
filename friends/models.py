from django.db import models
from teams.models import Team
from django.contrib.auth.models import User

class Friends(models.Model):
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='friends_team_a')
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE , related_name='friends_team_b')
    accepted = models.BooleanField(default=False)


class Chat(models.Model):
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='chat_team_a', null=True)
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE , related_name='chat_team_b', null=True)
    viewed = models.BooleanField(default=False)
    subject = models.CharField(max_length=500)
    message = models.CharField(max_length=1024)