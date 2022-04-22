from django.shortcuts import render
from django.http.response import JsonResponse

from cards.serializers import CardSerializer

from cards.models import Card

from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from players.views import get_random_player
from teams.models import Team

# Create your views here.
@api_view(['GET'])
def card_get_all(request):
    if request.method == 'GET':
        uid = request.user.id
        teams = Team.objects.filter(user_id__id = uid)
        team = teams.first()
        print(team)
        cards = Card.objects.filter(team_id__team_id = team.team_id)
        cards_serializer = CardSerializer(cards, many=True)

        return JsonResponse(cards_serializer.data, safe=False)

# internal functions

def create_random_card(team):
    player = get_random_player()
    print(player)

    
    card = Card.objects.create(
        team_id = team,
        player_name = player.get("player_name"),
        pic = player.get("pic"),
        height = player.get("height"),
        position = player.get("position"),
        games = player.get("games"),
        pts = player.get("pts"),
        p21 = player.get("p21"),
        p22 = player.get("p22"),
        p31 = player.get("p31"),
        p32 = player.get("p32"),
        p11 = player.get("p11"),
        p12 = player.get("p12"),
        p2 = player.get("p2"),
        p3 = player.get("p3"),
        p1 = player.get("p1"),
        defensive_reb = player.get("defensive_reb"),
        offensive_reb = player.get("offensive_reb"),
        total_reb = player.get("total_reb"),
        fouls_against = player.get("fouls_against"),
        fouls_for = player.get("fouls_for"),
        steals = player.get("steals"),
        turnovers = player.get("turnovers"),
        assists = player.get("assists"),
        blocks_for = player.get("blocks_for"),
        blocks_against = player.get("blocks_against"),
        VAL = player.get("VAL"),
        plusminus = player.get("plusminus"),
        dunks = player.get("dunks"),
    )

    return card
    
