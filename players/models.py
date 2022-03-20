from django.db import models

# Create your models here.
class Player(models.Model):
    player_name = models.CharField(max_length=50)
    rating = models.FloatField()

    def __str__(self):
        return self.player_name