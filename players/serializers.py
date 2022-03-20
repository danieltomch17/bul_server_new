from rest_framework import serializers 
from players.models import Player
 
 
class PlayerSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Player
        fields = ('player_name', 'team_id')