from django.shortcuts import render
from django.http.response import JsonResponse

from teams.serializers import TeamSerializer

from teams.models import Team

from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes




# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_get_all(request):
    if request.method == 'GET':
        teams = Team.objects.all()
        teams_serializer = TeamSerializer(teams, many=True)
        return JsonResponse(teams_serializer.data, safe=False)