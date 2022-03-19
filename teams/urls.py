from django.conf.urls import url
from teams import views

urlpatterns = [
    url(r'get', views.team_get_all),
]