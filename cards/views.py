from django.shortcuts import render
from django.http.response import JsonResponse

from cards.serializers import CardSerializer

from cards.models import Card

from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def card_get_all(request):
    if request.method == 'GET':
        cards = Card.objects.all()
        cards_serializer = CardSerializer(cards, many=True)

        return JsonResponse(cards_serializer.data, safe=False)