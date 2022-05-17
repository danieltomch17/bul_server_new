from django.urls import path
from django.conf.urls import url
from game import views

urlpatterns = [
    url(r'start_game', views.start_game),
    path('get_logs/<int:from_id>', views.get_logs, name = 'get_logs'),
]