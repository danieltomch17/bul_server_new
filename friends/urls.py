from django.urls import path
from .views import get_all_friends_by_user_team

urlpatterns = [
    path('get_all_friends_by_user_team/<int:pk>', get_all_friends_by_user_team, name = 'get_all_friends_by_user_team'),
]