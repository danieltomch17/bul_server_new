from django.conf.urls import url
from players import views

urlpatterns = [
    url(r'get', views.player_get_all),
    url(r'update_players_db_from_api', views.update_players_db_from_api),
    url(r'val_min_max', views.val_min_max),   
]