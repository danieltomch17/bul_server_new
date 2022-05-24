from rest_framework import serializers 
from leagues.models import LeagueEntry

class LeagueEntrySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = LeagueEntry
        fields = ('team', 'wins', 'losses', 'ties')
