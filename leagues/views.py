from hashlib import new
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view

from leagues.models import League, LeagueEntry
from leagues.serializers import LeagueEntrySerializer
from teams.models import Team

@api_view(['GET'])
def create_new_league(request, league_name):
    League.objects.create(name = league_name)

    return HttpResponse(status=200)


@api_view(['GET'])
def get_league_statistics(request):
    uid = request.user.id
    user_league = Team.objects.filter(user_id__id = uid).first().league
    print(user_league)
    league_statistics = LeagueEntry.objects.filter(league__id = user_league.id).order_by('-wins','-ties','-losses')
    print(league_statistics)

    league_entry_serializer = LeagueEntrySerializer(league_statistics, many=True)

    return JsonResponse(league_entry_serializer.data, safe=False)
    