from rest_framework import serializers 
from .models import Calendar
from teams.serializers import TeamSerializer
 
class EventSerializer(serializers.ModelSerializer):
    team_a = TeamSerializer()
    team_b = TeamSerializer()
    class Meta:
        model = Calendar
        fields = ('team_a', 'team_b' , 'date' , 'game')