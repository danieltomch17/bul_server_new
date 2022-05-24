from django.urls import path
from .views import get_all_friends_by_user_team, remove_friend_by_team_id, send_chat_message , get_all_private_messages_user_get , get_all_private_messages_user_sent, update_msg_viewed, add_friend, accept_friend_request, get_all_friend_requests

urlpatterns = [
    path('get_all_friends_by_user_team/', get_all_friends_by_user_team, name = 'get_all_friends_by_user_team'),
    path('remove_friend_by_team_id/', remove_friend_by_team_id, name = 'remove_friend_by_team_id'),
    path('send_chat_message/', send_chat_message, name = 'send_chat_message'),
    path('get_all_private_messages_user_get/', get_all_private_messages_user_get, name = 'get_all_private_messages_user_get'),
    path('get_all_private_messages_user_sent/', get_all_private_messages_user_sent, name = 'get_all_private_messages_user_sent'),
    path('update_msg_viewed/', update_msg_viewed, name = 'update_msg_viewed'),
    path('add_friend/', add_friend, name = 'add_friend'),
    path('accept_friend_request/', accept_friend_request, name = 'accept_friend_request'),
    path('get_all_friend_requests/', get_all_friend_requests, name = 'get_all_friend_requests'),
]