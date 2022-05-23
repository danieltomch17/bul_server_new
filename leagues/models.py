from django.db import models

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=50)
    is_full  = models.BooleanField(default=False)
    num_of_teams = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

class LeagueEntry(models.Model):
    is_active = models.BooleanField(default=True)
    league = models.ForeignKey(League, on_delete=models.DO_NOTHING)
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE)
    wins = models.PositiveSmallIntegerField(default=0)
    losses = models.PositiveSmallIntegerField(default=0)
    ties = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "{} : {} : wins - {} | losses - {} | ties - {}, Is active : {}".format(self.league.name, self.team.team_name, self.wins, self.losses, self.ties, self.is_active)