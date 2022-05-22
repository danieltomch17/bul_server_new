from django.urls import path
from django.conf.urls import url

from leagues import views

urlpatterns = [
    path('create_new_league/<str:league_name>', views.create_new_league, name = 'create_new_league'),
]