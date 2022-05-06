from django.urls import path
from .views import get_all_friends_by_user_team, remove_friend_by_team_id

urlpatterns = [
    path('get_all_friends_by_user_team/<int:pk>', get_all_friends_by_user_team, name = 'get_all_friends_by_user_team'),
    path('remove_friend_by_team_id/', remove_friend_by_team_id, name = 'remove_friend_by_team_id'),
]