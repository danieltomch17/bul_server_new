from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.response import Response

from rest_framework import status

from accounts.serializers import UserSerializer

from django.contrib.auth.models import User
from cards.models import Card
from cards.views import create_random_card
from leagues.models import League, LeagueEntry
from teams.models import Team

from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

@api_view(['POST'])
def user_create(request):
    if request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():

            # create the user
            user = user_serializer.save()
            if user:
                
                # get a league with available spot
                league_id = League.objects.filter(is_full = False).first().id
                join_league_queryset = League.objects.filter(id = league_id)
                join_league = join_league_queryset.first()
                
                # create a team for the user
                new_team = Team.objects.create(user_id = user, team_name = request.data['team_name'], league = join_league)
                
                # update league info
                league_num_of_teams = join_league.num_of_teams + 1
                join_league_queryset.update(num_of_teams = league_num_of_teams)
                if league_num_of_teams == 8 : join_league_queryset.update(is_full = True)

                # create league entry for the team
                LeagueEntry.objects.create(league=join_league, team=new_team)

                # generate 5 random cards
                for i in range(5):
                    # need to create 5 random cards
                    card = create_random_card(new_team)
                    card.is_first_five = True
                    card.save()
                
                return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_get_all(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)

        return JsonResponse(users_serializer.data, safe=False)


@api_view(['DELETE'])
def user_delete(request):
    try:
        user = User.objects.get(username=request.data['username']) 
    except User.DoesNotExist: 
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'User was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

### class based views :
"""
# Create your views here.
class UserCreate(APIView):
    ""#" 
    Creates the user. 
    ""#"

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCreate(APIView):
    ""#" 
    Deletes the user. 
    ""#"

    permission_classes = [IsAuthenticated]
"""