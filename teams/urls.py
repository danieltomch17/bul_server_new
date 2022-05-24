from django.conf.urls import url
from django.urls import path
from teams import views

urlpatterns = [
    path('get_team_by_token', views.get_team_by_token, name = 'get_team_by_token'),
    path('get_team_by_id/<int:pk>', views.get_team_by_id, name = 'get_team_by_id'),
]


