from rest_framework import serializers 
from cards.models import Card
 
 
class CardSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Card
        fields = ('player_name',
                'team_id',
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