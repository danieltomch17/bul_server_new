from rest_framework import serializers 
from teams.models import Team
 
 
class TeamSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Team
        fields = ('team_name', 'user_id', 'logo')
