from re import L
from django import dispatch
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_delete
from django.dispatch import receiver

from leagues.models import League

# Create your models here.
class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.CharField(max_length=500)
    league = models.ForeignKey(League, on_delete=models.DO_NOTHING)
    cash = models.CharField(max_length=50, default=10000)
    real_cash = models.CharField(max_length=50, default=0)
    def __str__(self):
        return '({}) {}'.format(self.pk, self.team_name)

@receiver(post_delete, sender=Team, dispatch_uid='team_delete_update_league')
def update_league_on_team_delete(sender, instance, using, **kwargs):
    league_to_update_queryset = League.objects.filter(id  = instance.league.id)
    league_to_update = league_to_update_queryset.first()
    print(league_to_update)
    league_to_update_queryset.update(num_of_teams=league_to_update.num_of_teams-1)