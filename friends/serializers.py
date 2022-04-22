from rest_framework import serializers 
from .models import Friends
from teams.serializers import TeamSerializer
 
class FriendsSerializer(serializers.ModelSerializer):
    team_b = TeamSerializer()
    class Meta:
        model = Friends
        fields = ('team_b',)