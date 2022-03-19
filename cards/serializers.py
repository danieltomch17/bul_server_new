from rest_framework import serializers 
from cards.models import Card
 
 
class CardSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Card
        fields = ('player_name', 'team_id')