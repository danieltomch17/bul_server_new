from rest_framework import serializers 
from players.models import Player
 
 
class PlayerSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Player
        fields = (
            'player_name',
            'pic',
            'height',
            'position',
            'games',
            'pts',
            'p21',
            'p22',
            'p31',
            'p32',
            'p11',
            'p12',
            'p2',
            'p3',
            'p1',
            'defensive_reb',
            'offensive_reb',
            'total_reb',
            'fouls_against',
            'fouls_for',
            'steals',
            'turnovers',
            'assists',
            'blocks_for',
            'blocks_against',
            'VAL',
            'plusminus',
            'dunks'
        
        )