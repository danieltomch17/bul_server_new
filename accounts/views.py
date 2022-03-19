from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.response import Response

from rest_framework import status

from accounts.serializers import UserSerializer

from django.contrib.auth.models import User
from cards.models import Card
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
                
                # create a team for the user
                team = Team.objects.create(user_id = user, team_name = request.data['team_name'])

                # generate 5 random cards
                for i in range(5):
                    card = Card.objects.create(team_id = team, player_name = 'Salim Suliman')
                
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