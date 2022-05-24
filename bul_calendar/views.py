from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from .models import Calendar
from teams.models import Team
from .serializers import EventSerializer
from datetime import date, timedelta
from datetime import datetime, timedelta
from django.db.models import Q

@api_view(['GET'])
def get_all_event_by_team_id(request, pk):
    if request.method == 'GET':
        events = Calendar.objects.filter(team_a__pk=pk)
        event_serializer = EventSerializer(events, many=True)
        return JsonResponse(event_serializer.data, safe=False)

@api_view(['GET'])
def get_all_events_today(request):
    if request.method == 'GET':
        startdate = date.today()
        events = Calendar.objects.filter(date__range=[startdate, startdate])
        event_serializer = EventSerializer(events, many=True)
        return JsonResponse(event_serializer.data, safe=False)

@api_view(['GET'])
def get_todays_event_by_team_id(request):
    if request.method == 'GET':
        uid = request.user.id
        teams = Team.objects.filter(user_id__id = uid)
        team = teams.first()
        today = date.today()
        events = list(Calendar.objects.filter(Q(team_a__pk=team.team_id) | Q(team_b__pk=team.team_id)).filter(date__gte=today, done=False))
        if(len(events) > 0):
            event_serializer = EventSerializer(events, many=True)
            return JsonResponse(event_serializer.data[0], safe=False)
        return JsonResponse(None, safe=False)

@api_view(['POST'])
def invite_game(request):
    if request.method == 'POST':
        uid = request.user.id
        to_team_id = request.data.get('team_id', -1)
        team_send_to = Team.objects.filter(user_id__id=to_team_id)[0]
        current_team =  Team.objects.filter(user_id__id = uid)[0]
        now_plus_10 = datetime.now() + timedelta(minutes = 10)
        create_event = Calendar.objects.create(team_a =current_team , team_b = team_send_to, date= now_plus_10 , accepted= False)
        return JsonResponse("Done", safe=False)

@api_view(['POST'])
def accept_game_request(request):
    if request.method == 'POST':
        uid = request.user.id
        to_team_id = request.data.get('team_id', -1)
        team_send_to = Team.objects.filter(team_id=to_team_id)[0]
        current_team =  Team.objects.filter(user_id__id = uid)[0]
        if(to_team_id != -1 and current_team != team_send_to):
            change_Calendar_request_to_true = Calendar.objects.filter(team_a=team_send_to , team_b = current_team).update(accepted=True)
            change_Calendar_request_to_true = Calendar.objects.filter(team_a=team_send_to , team_b = current_team)[0]
            return JsonResponse("Done", safe=False)
        else:
             return JsonResponse("error")

@api_view(['GET'])
def get_all_game_requests(request):
    if request.method == 'GET':
        user = request.user.id
        calendar = Calendar.objects.filter(team_b__user_id__id=user , accepted=False)

        event_serializer = EventSerializer(calendar, many=True)
        return JsonResponse(event_serializer.data, safe=False)

@api_view(['POST'])
def update_event_to_done(request):
    if request.method == 'POST':
        uid = request.user.id
        to_team_id = request.data.get('team_id', -1)
        date = request.data.get('date', -1)
        team_send_to = Team.objects.filter(team_id=to_team_id)[0]
        current_team =  Team.objects.filter(user_id__id = uid)[0]
        if(to_team_id != -1 and current_team != team_send_to):
            change_Calendar_request_to_true = Calendar.objects.filter(team_a=team_send_to ,date=date,  team_b = current_team).update(done=True)
            return JsonResponse("Done", safe=False)
        else:
             return JsonResponse("error")