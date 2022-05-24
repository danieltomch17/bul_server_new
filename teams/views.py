from django.shortcuts import render
from django.http.response import JsonResponse

from teams.serializers import TeamSerializer, TeamLocalSerializer

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_team_by_token(request):
    if request.method == 'GET':
        uid = request.user.id
        teams = Team.objects.filter(user_id__id = uid)[0]
        teams_serializer = TeamLocalSerializer(teams)
        print(teams_serializer.data)
        return JsonResponse(teams_serializer.data, safe=False)       

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_team_by_id(request,pk):
    if request.method == 'GET':
        teams = Team.objects.filter(user_id=pk)[0]
        teams_serializer = TeamSerializer(teams)
        return JsonResponse(teams_serializer.data, safe=False)       