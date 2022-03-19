from django.conf.urls import url
from cards import views

urlpatterns = [
    url(r'get', views.card_get_all),
]