from rest_framework import serializers 
from teams.models import Team
 
 
class TeamSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Team
        fields = ('team_name', 'user_id', 'logo' , 'team_id')


class TeamLocalSerializer(serializers.ModelSerializer):
    #Serilazation for the current player.
    class Meta:
        model = Team
        fields = ('team_name', 'user_id', 'logo' , 'team_id' , 'cash', 'real_cash')
