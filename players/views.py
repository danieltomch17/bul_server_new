from django.shortcuts import render
from django.http.response import JsonResponse

from players.serializers import PlayerSerializer

from players.models import Player

from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

import requests
from players.consts import PLAYERS_STATS_URL, PLAYERS_URL

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def player_get_all(request):
    if request.method == 'GET':
        players = Player.objects.all()
        players_serializer = PlayerSerializer(players, many=True)

        return JsonResponse(players_serializer.data, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def update_players_db_from_api(request):
    team_id = 0
    team_uid = 0
    cYear = 2021

    Player.objects.all().delete()

    # create PARAMS for request
    PARAMS = {
        'team_id':team_id,
        'team_uid':team_uid,
        'cYear':cYear
    }
    
    # get players from api
    res = requests.get(url=PLAYERS_URL, params=PARAMS)
    json_res = res.json()
    
    for elem in json_res["players"]:
        # get player stats
        print(elem["name_eng"])
        STATS_PARAMS = {
            'player_id':elem["player_id"],
            'cYear':elem["year_id"],
            'isAverages':'true',
            'isPlayOff':'false'
        }

        stats_res = requests.get(url=PLAYERS_STATS_URL, params=STATS_PARAMS)

        try:
            player_stats = stats_res.json()["player"][0]
        except:
            print('could not convert player stats to json')
            continue

        # save player info and stats to DB
        Player.objects.create(
            player_name=elem["name_eng"],
            pic=elem["pic"],
            height=elem["Height"],
            position=elem["position_eng"],
            games=player_stats["games"],
            pts=player_stats["pts"],
            p21=player_stats["p21"],
            p22=player_stats["p22"],
            p31=player_stats["p31"],
            p32=player_stats["p32"],
            p11=player_stats["p11"],
            p12=player_stats["p12"],
            p2=player_stats["p2"],
            p3=player_stats["p3"],
            p1=player_stats["p1"],
            defensive_reb=player_stats["defensive_reb"],
            offensive_reb=player_stats["offensive_reb"],
            total_reb=player_stats["total_reb"],
            fouls_against=player_stats["fouls_against"],
            fouls_for=player_stats["fouls_for"],
            steals=player_stats["steals"],
            turnovers=player_stats["tournovers"],
            assists=player_stats["assists"],
            blocks_for=player_stats["blocks_for"],
            blocks_against=player_stats["block_against"],
            VAL=player_stats["VAL"],
            plusminus=player_stats["plusminus"],
            dunks=player_stats["dunk"],
        )
        
    return JsonResponse(json_res)