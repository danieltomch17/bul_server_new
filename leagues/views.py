from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.decorators import api_view

from leagues.models import League

@api_view(['GET'])
def create_new_league(request, league_name):
    League.objects.create(name = league_name)

    return HttpResponse(status=200)

# Create your views here.
