"""bul_server_new URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'users/', include('accounts.urls')),
    url(r'teams/', include('teams.urls')),
    url(r'players/', include('players.urls')),
    url('calendar/', include('bul_calendar.urls')),
    url('friends/', include('friends.urls')),
    url('game/', include('game.urls')),
    url('cards/', include('cards.urls')),
    url('leagues/', include('leagues.urls')),
]
