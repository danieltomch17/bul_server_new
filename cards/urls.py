
from django.conf.urls import url
from django.urls import path
from cards import views
from .views import get_all_card_packs

urlpatterns = [
    #url(r'get', views.card_get_all),
    path('get/', views.card_get_all),
    path('get_all_card_packs/', views.get_all_card_packs),
    path('set_opening_team/', views.set_opening_team),
    path('buy_card_pack/', views.buy_card_pack),
    path('card_get_five_open/', views.card_get_five_open),
]