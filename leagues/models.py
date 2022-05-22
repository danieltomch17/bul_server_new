from django.db import models

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=50)
    is_full  = models.BooleanField(default=False)
    num_of_teams = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name