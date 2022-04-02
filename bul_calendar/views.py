from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from .models import Calendar
from teams.models import Team
from .serializers import EventSerializer
from datetime import date, timedelta

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
def get_todays_event_by_team_id(request, pk):
    if request.method == 'GET':
        today = date.today()
        events = list(Calendar.objects.filter(team_a__pk=pk).filter(date__gte=today))
        event_serializer = EventSerializer(events, many=True)
        return JsonResponse(event_serializer.data[0], safe=False)