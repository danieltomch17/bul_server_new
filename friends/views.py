from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from .models import Friends
from teams.models import Team
from .serializers import FriendsSerializer
from datetime import date, timedelta

@api_view(['GET'])
def get_all_friends_by_user_team(request, pk):
    print("here")
    if request.method == 'GET':
        friends = Friends.objects.filter(team_a__pk=pk)
        print(friends)
        friends_serializer = FriendsSerializer(friends, many=True)
        return JsonResponse(friends_serializer.data, safe=False)
