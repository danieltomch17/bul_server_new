from rest_framework import serializers 
from leagues.models import LeagueEntry
from teams.serializers import TeamSerializer
class LeagueEntrySerializer(serializers.ModelSerializer):
    team =  TeamSerializer()
    class Meta:
        model = LeagueEntry
        fields = ('team', 'wins', 'losses', 'ties')
