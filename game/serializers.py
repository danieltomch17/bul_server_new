from rest_framework import serializers 
from game.models import Game

class GameSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Game
        fields = ('id', 'team_a', 'team_b', 'date', 'time', 'results')
        ordering = ('date', 'time')
