from django.conf.urls import url
from players import views

urlpatterns = [
    url(r'get', views.player_get_all),
]