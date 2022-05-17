from rest_framework import serializers 
from .models import Friends, Chat
from teams.serializers import TeamSerializer
from accounts.serializers import UserSerializer

class FriendsSerializer(serializers.ModelSerializer):
    team_b = TeamSerializer()
    class Meta:
        model = Friends
        fields = ('team_b',)

class ChatSerializer(serializers.ModelSerializer):
    team_a = TeamSerializer()
    team_b = TeamSerializer()
    class Meta:
        model = Chat
        fields = ('team_a', 'team_b', 'viewed', 'subject', 'message' , 'id')        