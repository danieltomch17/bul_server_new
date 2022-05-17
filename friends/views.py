from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from .models import Friends, Chat
from teams.models import Team
from .serializers import FriendsSerializer, ChatSerializer
from datetime import date, timedelta


#working
@api_view(['GET'])
def get_all_friends_by_user_team(request, pk):
    if request.method == 'GET':
        user = request.user.id
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
        

@api_view(['POST'])
def send_chat_message(request):
    if request.method == 'POST':
        uid = request.user.id
        to_team_id = request.data.get('user_id', -1)
        team_send_to = Team.objects.filter(team_id=to_team_id)[0]
        current_team =  Team.objects.filter(user_id__id = uid)[0]
        subject = request.data.get('subject', '')
        message = request.data.get('message', '')
        if(to_team_id != -1):
            create_chat = Chat.objects.create(team_a =current_team , team_b = team_send_to, subject= subject, message=message)
            return JsonResponse("Done", safe=False)
        else:
             return JsonResponse("error")
        

@api_view(['GET'])
def get_all_private_messages_user_get(request):
    if request.method == 'GET':
        uid = request.user.id
        team = Team.objects.filter(user_id__id = uid)[0]
        chats = Chat.objects.filter(team_b__team_id=team.team_id) 
        chat_serializer = ChatSerializer(chats, many=True)
        return JsonResponse(chat_serializer.data, safe=False)


@api_view(['GET'])
def get_all_private_messages_user_sent(request):
    if request.method == 'GET':
        uid = request.user.id
        team = Team.objects.filter(user_id__id = uid)[0]
        chats = Chat.objects.filter(team_a__team_id=team.team_id) 
        chat_serializer = ChatSerializer(chats, many=True)
        return JsonResponse(chat_serializer.data, safe=False)

@api_view(['POST'])
def update_msg_viewed(request):
    if request.method == 'POST':
        uid = request.user.id
        chat_id = request.data.get('chat_id',-1)
        if(chat_id == -1):
             return JsonResponse("error")
        team = Team.objects.filter(user_id__id = uid)[0]
        print(team)
        chat = Chat.objects.filter(team_b__team_id=team.team_id, id=chat_id)[0]
        chat.viewed = True
        chat.save()
        return JsonResponse("Done", safe=False)