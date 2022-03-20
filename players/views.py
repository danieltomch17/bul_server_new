from django.shortcuts import render
from django.http.response import JsonResponse

from players.serializers import PlayerSerializer

from players.models import Player

from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def card_get_all(request):
    if request.method == 'GET':
        players = Player.objects.all()
        players_serializer = PlayerSerializer(players, many=True)

        return JsonResponse(players_serializer.data, safe=False)