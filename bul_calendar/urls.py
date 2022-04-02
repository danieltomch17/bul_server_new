from django.urls import path
from .views import get_all_event_by_team_id , get_all_events_today , get_todays_event_by_team_id

urlpatterns = [
    path('get_all_event_by_team_id/<int:pk>', get_all_event_by_team_id, name = 'get_all_event_by_team_id'),
    path('get_todays_event_by_team_id/<int:pk>', get_todays_event_by_team_id, name = 'get_todays_event_by_team_id'),
    path('get_all_events_today/', get_all_events_today)
]