from django.shortcuts import render
from django.http.response import JsonResponse

from cards.serializers import CardSerializer, CardPackSerializer

from cards.models import Card, CardPack

from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from players.views import get_random_player
from teams.models import Team


@api_view(['GET'])
def card_get_all(request):
    if request.method == 'GET':
        uid = request.user.id
        teams = Team.objects.filter(user_id__id = uid)
        team = teams.first()
        cards = Card.objects.filter(team_id__team_id = team.team_id)
        cards_serializer = CardSerializer(cards, many=True)

        return JsonResponse(cards_serializer.data, safe=False)

@api_view(['GET'])
def card_get_five_open(request):
    if request.method == 'GET':
        uid = request.user.id
        teams = Team.objects.filter(user_id__id = uid)
        team = teams.first()
        cards = Card.objects.filter(team_id__team_id = team.team_id , is_first_five=True)
        cards_serializer = CardSerializer(cards, many=True)

        return JsonResponse(cards_serializer.data, safe=False)



@api_view(['POST'])
def set_opening_team(request):
    if request.method == 'POST':
        uid = request.user.id
        teams = Team.objects.filter(user_id__id = uid)
        team = teams.first()
        cards = request.data.get('cards', [])
        cards_to_false = Card.objects.filter(team_id__team_id = team.team_id)
        for card in cards_to_false :
            card_from_db = Card.objects.filter(team_id__team_id = team.team_id, player_name=card)[0]
            card_from_db.is_first_five = False
            card_from_db.save()
        for card_to_five in cards :
            card = Card.objects.filter(team_id__team_id = team.team_id , player_name=card_to_five['player_name'])[0]
            card.is_first_five = True
            card.save()
        cards_serializer = CardSerializer(cards_to_false, many=True)

        return JsonResponse(cards_serializer.data, safe=False)

@api_view(['GET'])
def buy_pack_of_card(request):
    if request.method == 'GET':
        uid = request.user.id
        team = Team.objects.filter(user_id__id = uid)
        create_random_card(team)
        team = teams.first()
        cards = Card.objects.filter(team_id__team_id = team.team_id)
        cards_serializer = CardSerializer(cards, many=True)

        return JsonResponse(cards_serializer.data, safe=False)

@api_view(['GET'])
def get_all_card_packs(request):
    if request.method == 'GET':
        cards_pack = CardPack.objects.all()
        cards_serializer = CardPackSerializer(cards_pack, many=True)
        return JsonResponse(cards_serializer.data, safe=False)

@api_view(['POST'])
def buy_card_pack(request):
    if request.method == 'POST':
        uid = request.user.id
        team = Team.objects.filter(user_id__id = uid)
        pack_id = request.data.get('pack_id')
        cards_pack = CardPack.objects.filter(id=pack_id)
        print(cards_pack[0].price)
        print(team[0].cash)
        if(team[0].cash < cards_pack[0].price):
            return JsonResponse("Not enough Cash", safe=False)
        else:
            cards = []
            for i in range(5):
                card = create_random_card(team[0])
                card.save()
                cards.append(card)
            team[0].cash = int(team[0].cash) - int(cards_pack[0].price)
            team[0].save()
            cards_serializer = CardSerializer(cards, many=True)
            return JsonResponse(cards_serializer.data, safe=False)
# internal functions

def create_random_card(team):
        player = get_random_player()
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
    
