from django.urls import path
from .views import get_all_event_by_team_id , get_all_events_today , get_todays_event_by_team_id, invite_game, accept_game_request, get_all_game_requests, update_event_to_done

urlpatterns = [
    path('get_all_event_by_team_id/<int:pk>', get_all_event_by_team_id, name = 'get_all_event_by_team_id'),
    path('get_todays_event_by_team_id/', get_todays_event_by_team_id, name = 'get_todays_event_by_team_id'),
    path('get_all_events_today/', get_all_events_today),
    path('invite_game/', invite_game),
    path('accept_game_request/', accept_game_request),
    path('get_all_game_requests/', get_all_game_requests),
    path('update_event_to_done/', update_event_to_done),
]