from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from .models import Friends
from teams.models import Team
from .serializers import FriendsSerializer
from datetime import date, timedelta

#working
@api_view(['GET'])
def get_all_friends_by_user_team(request, pk):
    if request.method == 'GET':
        user = request.user.id
        print(user)
        friends = Friends.objects.filter(team_a__user_id__id=user)
        friends_serializer = FriendsSerializer(friends, many=True)
        return JsonResponse(friends_serializer.data, safe=False)

#working
@api_view(['POST'])
def remove_friend_by_team_id(request):
    if request.method == 'POST':
        user_id_player_who_ask_to_remove = request.user.id
        remove_user_id = request.data.get('userId', -1)
        if(remove_user_id != -1):
            friends = Friends.objects.filter(team_a__user_id__id=user_id_player_who_ask_to_remove, team_b__user_id__id=remove_user_id).delete()
            friends = Friends.objects.filter(team_a__user_id__id=remove_user_id , team_b__user_id__id=user_id_player_who_ask_to_remove).delete()
            friends_after_delete = Friends.objects.filter(team_a__user_id__id=user_id_player_who_ask_to_remove)
            friends_serializer = FriendsSerializer(friends_after_delete, many=True)
            return JsonResponse(friends_serializer.data, safe=False)
        else:
             return JsonResponse("error")
        
