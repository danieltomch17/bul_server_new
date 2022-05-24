from django.urls import path
from django.conf.urls import url
from game import views

urlpatterns = [
    path('start_game/<int:home_id>/<int:away_id>/<str:date>', views.start_game, name='start_game'),
    path('get_logs/<int:from_id>', views.get_logs, name = 'get_logs'),
    path('get_game_history', views.get_game_history, name = 'get_game_history'),
    path('done_game', views.done_game)
]