from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.CharField(max_length=500)

    def __str__(self):
        return self.team_name